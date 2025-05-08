import time
import board
import adafruit_dht as afd
import RPi.GPIO as GPIO
import requests
dhtDevice = afd.DHT22(board.D18)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
THINKSPEAK_API_KEY="U6U8NABCT144JAMH"
THINKSPEAK_URL = "https://api.thingspeak.com/update?api_key=U6U8NABCT144JAMH&field1=0"
while True:
	try:
		temp_c = dhtDevice.temperature
		temp_f = temp_c*(9/5)+32
		humidity = dhtDevice.humidity
		print(f"Degrees Celsius: {temp_c : 0.1f}")
		print(f"Degrees Fahrenheit: {temp_f : 0.1f}")
		print(f"Humidity: {humidity}%\n")
	    
		
	except RuntimeError as error:
		print(error.args[0])
		time.sleep(2.0)
		continue
	except Exception as error:
		dhtDevice.exit
		raise error
		
	if temp_c>22:
		GPIO.output(23, GPIO.HIGH)
		time.sleep(1)	
		GPIO.output(23, GPIO.LOW)
		time.sleep(1)	
	else:
		GPIO.output(23, GPIO.LOW)
		time.sleep(0.2)	
		GPIO.output(23, GPIO.LOW)
		time.sleep(0.2)	
	response = requests.get(
		THINKSPEAK_URL,
		params={
			"api_key":THINKSPEAK_API_KEY,
			"field1":temp_c,
			"field2":humidity
		}
	)
	print(f"ThingSpeak Response: {response.status_code}")
		
	

