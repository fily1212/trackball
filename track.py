import cv2
import numpy as np
import time

# Collegati allo stream della telecamera
cap = cv2.VideoCapture(1)

# Definisci i range di colore per il tracking della palla
# Modifica questi valori in base al colore della tua palla
lower_color = np.array([5, 100, 100])  # Esempio per arancione chiaro
upper_color = np.array([15, 255, 255])  # Esempio per arancione scuro

while cap.isOpened():
    time.sleep(0.1)
    # Leggi un frame dallo stream
    ret, frame = cap.read()

    # Controlla se il frame è stato catturato correttamente
    if ret:
        # Converti il frame da BGR a HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crea una maschera che isoli la palla basandosi sul colore
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Trova i contorni nella maschera
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Trova il contorno con l'area massima, assumendo che sia la palla
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
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