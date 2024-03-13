import serial
import json
import sys

# Setup della connessione seriale
ser = serial.Serial('COM6', 9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        try:
            # Decodifica del JSON ricevuto
            jsonObj = json.loads(line)
            print("1")
            pot = jsonObj.get('numero')
            print("value: ", pot)
            ser.reset_input_buffer()

            # Costruzione del JSON di risposta
#            response = {"comando": "muovi", "distanza": 100}
            response = {"numero":100}
            response_json = json.dumps(response) + '\n'  # Aggiungi '\n' come delimitatore

            # Invio del JSON di risposta all'Arduino
            ser.write(response_json.encode('utf-8'))

            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            jsonObj = json.loads(line)
            print("1")
            pot = jsonObj.get('numero ricevuto: ')
            print("numero ricevuto: ", pot)
            ser.reset_input_buffer()


        except json.JSONDecodeError:  # Cattura specificamente gli errori di decodifica JSON
            print("Error in JSON decoding")
        except Exception as e:  # Cattura altri possibili errori
            print(f"An error occurred: {e}")
