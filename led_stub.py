import serial
import time
import random
import json

# Configura la porta seriale
ser = serial.Serial('COM6', 9600)  # Modifica '/dev/ttyUSB0' con la tua porta seriale

def send_command():


    # Sceglie una lettera casuale tra 'f', 'b', 'r', 'l'
    cmd = random.choice(['forward', 'back', 'right', 'left'])
    # Crea il messaggio JSON
    message = json.dumps({"cmd": cmd})
    # Invia il messaggio tramite la porta seriale
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            try:
                # Decodifica del JSON ricevuto
                jsonObj = json.loads(line)
                print("1Ricevuto da Arduino:", jsonObj)
            except:
                print("Errore")
        send_command()
        time.sleep(1)  # Attende un secondo
except KeyboardInterrupt:
    print("Programma interrotto.")
finally:
    ser.close()  # Chiude la connessione seriale quando il programma termina
