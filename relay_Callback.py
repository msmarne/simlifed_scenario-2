
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
import time

#looks for a perticular service key in the json format
cred = credentials.Certificate("serviceAccountKey.json")   
firebase_admin.initialize_app(cred)


RELAY_PIN = 16
GPIO.setmode(GPIO.BCM)

GPIO.setup(RELAY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db = firestore.client()

#set the  variables in the google cloud firebase 
db.collection('Listening_function').document('RELAY_M_A').set(   
     {
        'value':False
        }
    
    )
#call back fuction 
def button_callback(channel):
    # if the GPIO relay pin is high it will update the firebase as False
    if GPIO.input(RELAY_PIN) == GPIO.HIGH:
         
        db.collection('Listening_function').document('RELAY_M_A').update(
           {
               'value' : False
               }
           
           )
    else:
         # if the GPIO relay pin is high it will update the firebase as False
        db.collection('Listening_function').document('RELAY_M_A').update(
           {
               'value' : True
               }
           
           )
        
# waits for Relay pin(GPIO-16) to get high and call for a call back fuction(button_callback)
GPIO.add_event_detect(RELAY_PIN, GPIO.BOTH,
                      callback= button_callback,bouncetime=50 ) 

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
        
