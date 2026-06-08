import requests
import time
import random


URL = "http://100.116.xxx.xxx:5000/data" 

print("Starter datasimulering... Tryk CTRL+C for at stoppe.")

while True:
    falsk_sensor_vaerdi = round(random.uniform(15.0, 30.0), 1)
    
    data_pakke = {"value": falsk_sensor_vaerdi}
    
    try:
        response = requests.post(URL, json=data_pakke)
        if response.status_code == 201:
            print(f"Succes! Sendte værdien {falsk_sensor_vaerdi} til databasen.")
        else:
            print(f"Fejl fra serveren: {response.status_code}")
    except Exception as e:
        print(f"Kunne ikke forbinde til Flask-serveren: {e}")
    
    time.sleep(5)
