import cv2
import numpy as np

# Indirizzo dello stream della telecamera
url = 'http://192.168.4.1:81/stream'

# Collegati allo stream della telecamera
cap = cv2.VideoCapture(1)

# Definisci i range di colore per il tracking della palla
lower_color = np.array([5, 100, 100])  # Esempio per arancione chiaro
upper_color = np.array([15, 255, 255])  # Esempio per arancione scuro

while cap.isOpened():
    ret, frame = cap.read()
    if ret:


        # Applica Gaussian Blur per ridurre il rumore e le variazioni di luce
        blurred_frame = cv2.GaussianBlur(frame, (11, 11), 0)

        # Converti il frame da BGR a HSV
        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Crea una maschera che isoli la palla basandosi sul colore
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Trova i contorni nella maschera
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        found_ball = False
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:  # Evita la divisione per zero
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.4 < circularity < 1.5:  # Valori vicini a 1 indicano una forma più circolare
                (x, y), radius = cv2.minEnclosingCircle(contour)
                if 10 < radius < 30:  # Aggiusta questi valori in base alla dimensione attesa della palla
                    # Palla trovata
                    found_ball = True
                    center_of_frame = frame.shape[1] / 2
                    position = "centro" if abs(x - center_of_frame) < 50 else ("sinistra" if x < center_of_frame else "destra")
                    print(f"La palla è a {position}.")
                    # Disegna il cerchio intorno alla palla rilevata
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                    break  # Rimuovi questa riga se ci possono essere più palline

        if not found_ball:
            print('Palla non trovata.')

        # Mostra il frame
        cv2.imshow('Frame con palla', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print('Errore nella cattura del frame.')
        break

cap.release()
cv2.destroyAllWindows()