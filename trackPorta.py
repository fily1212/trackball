import cv2
import numpy as np
import time

# Collegati allo stream della telecamera
cap = cv2.VideoCapture(1)

# Definisci i range di colore per il tracking della palla arancione
lower_orange = np.array([5, 100, 100])  # Esempio per arancione chiaro
upper_orange = np.array([15, 255, 255])  # Esempio per arancione scuro

# Definisci i range di colore per il riconoscimento del rettangolo verde
lower_green = np.array([40, 40, 40])  # Esempio per verde chiaro
upper_green = np.array([70, 255, 255])  # Esempio per verde scuro

while cap.isOpened():
    time.sleep(0.1)
    # Leggi un frame dallo stream
    ret, frame = cap.read()

    # Controlla se il frame è stato catturato correttamente
    if ret:
        # Converti il frame da BGR a HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Maschera per l'arancione
        mask_orange = cv2.inRange(hsv_frame, lower_orange, upper_orange)

        # Maschera per il verde
        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)

        # Trova i contorni per l'arancione
        contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Trova i contorni per il verde
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Processa i contorni verdi
        for cnt in contours_green:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:  # Controlla se il contorno ha 4 lati (rettangolo)
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)  # Disegna il rettangolo verde
                x, y, w, h = cv2.boundingRect(approx)
                cv2.putText(frame, "Rettangolo verde", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                break  # Rimuovi questa riga se ci possono essere più rettangoli


        # Trova il contorno con l'area massima, assumendo che sia la palla
        if contours_orange:
            max_contour = max(contours_orange, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(max_contour)

            if radius > 12:  # Assicurati che il contorno sia abbastanza grande da essere la palla
                # Determina la posizione della palla
                center_of_frame = frame.shape[1] / 2
                position = "centro" if abs(x - center_of_frame) < 40 else ("sinistra" if x < center_of_frame else "destra")

                # Stampa la posizione della palla
                print(f"La palla è a {position}.")

                # Opzionale: visualizza il risultato
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.imshow('Frame con palla', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            print('Palla non trovata.')

    else:
        print('Errore nella cattura del frame.')
        break

# Rilascia la connessione e chiudi tutte le finestre
cap.release()
cv2.destroyAllWindows()