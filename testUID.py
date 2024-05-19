from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

while True:
  
  uid = reader.read()
  folder_name = str(uid)
  print(folder_name)  # Output: "12345"

GPIO.cleanup()