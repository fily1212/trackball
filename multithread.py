import cv2
import numpy as np
import threading
import json
import serial
import time

# Impostazioni per la fotocamera e il rilevamento della palla
lower_color = np.array([5, 100, 100])  # Esempio per arancione chiaro
upper_color = np.array([15, 255, 255])  # Esempio per arancione scuro

# Variabile globale per conservare la posizione della palla
global_position = "centro"

# Setup della connessione seriale con Arduino
# Cambia 'COM6' con il tuo dispositivo seriale corretto
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Dà tempo ad Arduino di resettarsi


def track_ball():
    global position
    cap = cv2.VideoCapture(1)  # Collegati allo stream della telecamera

    while cap.isOpened():
        time.sleep(0.1)  # Modifica per regolare la frequenza di campionamento
        ret, frame = cap.read()

        if ret:
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, lower_color, upper_color)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                max_contour = max(contours, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(max_contour)

                if radius > 12:
                    center_of_frame = frame.shape[1] / 2
                    position = "centro" if abs(x - center_of_frame) < 40 else (
                        "sinistra" if x < center_of_frame else "destra")
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

    cap.release()
    cv2.destroyAllWindows()


def communicate_with_arduino():
    global global_position
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)
            try:
                # Decodifica del JSON ricevuto
                jsonObj = json.loads(line)
                print("Ricevuto da Arduino:", jsonObj)

                # Costruzione del JSON di risposta basato sulla posizione attuale della palla
                response = {"comando": global_position}  # Aggiusta i campi come necessario
                response_json = json.dumps(response) + '\n'  # Aggiungi '\n' come delimitatore
                arduino.write(response_json.encode('utf-8'))

                # Reset del buffer di input per evitare accumulo di vecchi messaggi
                arduino.reset_input_buffer()

            except json.JSONDecodeError:  # Cattura specificamente gli errori di decodifica JSON
                print("Error in JSON decoding")
            except Exception as e:  # Cattura altri possibili errori
                print(f"An error occurred: {e}")

        # Puoi aggiungere una piccola pausa per ridurre il carico di lavoro
        time.sleep(0.5)  # Ajust this based on your needs


# Creazione dei thread
thread_camera = threading.Thread(target=track_ball)
thread_arduino = threading.Thread(target=communicate_with_arduino)

# Avvio dei thread
thread_camera.start()
thread_arduino.start()

