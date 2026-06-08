import requests
import time
import random

# Erstat med din VM's rigtige IP-adresse
URL = "http://100.116.xxx.xxx:5000/data" 

print("Starter datasimulering... Tryk CTRL+C for at stoppe.")

while True:
    # Generer en tilfældig måling (f.eks. mellem 15.0 og 30.0)
    falsk_sensor_vaerdi = round(random.uniform(15.0, 30.0), 1)
    
    # Lav den JSON-pakke, som app.py forventer
    data_pakke = {"value": falsk_sensor_vaerdi}
    
    try:
        # Send dataen afsted som et POST-request
        response = requests.post(URL, json=data_pakke)
        if response.status_code == 201:
            print(f"Succes! Sendte værdien {falsk_sensor_vaerdi} til databasen.")
        else:
            print(f"Fejl fra serveren: {response.status_code}")
    except Exception as e:
        print(f"Kunne ikke forbinde til Flask-serveren: {e}")
    
    # Vent 5 sekunder før næste måling sendes
    time.sleep(5)
