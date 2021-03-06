import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import RPi.GPIO as GPIO
from time  import sleep
import threading


#looks for a perticular service key in the json format
cred = credentials.Certificate("serviceAccountKey.json")   
firebase_admin.initialize_app(cred)


RELAY_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(RELAY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db = firestore.client()

#create an event for notifying main thread 

callback_done  = threading.Event()

boolValue = None
class CallBack:
    @classmethod
    def button_callback(channel,demo1):
        print("ITs working")
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
            

# create callback on_snapshot fuction to capture changes

    
    

doc_ref = db.collection(u'testC').document(u'testD')

#watch the document 
if __name__== '__main__':
    cb = CallBack()
    def on_snapshot(doc_snapshot, changes ,  read_time):
        for doc in doc_snapshot:
            docDict = doc.to_dict()
            isTrue = docDict['isTrue']
            print('Recived document snapshot: {doc.id}, isTrue = {isTrue}')
            global boolValue
            boolValue = isTrue
            if boolValue == True:
                GPIO.output(4, False) 
                sleep(2) 
                GPIO.output(4, True)
              
                GPIO.add_event_detect(RELAY_PIN, GPIO.BOTH,
                      callback= cb.button_callback,bouncetime=50 ) 
        callback_done.set()
    doc_ref = db.collection(u'testC').document(u'testD')
    doc_watch = doc_ref.on_snapshot(on_snapshot)


    
                      
                      
while True:
    print(boolValue)
    sleep(0.5)
    

#set the  variables in the google cloud firebase 
db.collection('Listening_function').document('RELAY_M_A').set(   
     {
        'value':False
        }
    
    )
#call back fuction 

# waits for Relay pin(GPIO-16) to get high and call for a call back fuction(button_callback)
#GPIO.add_event_detect(RELAY_PIN, GPIO.BOTH,
 #                     callback= button_callback,bouncetime=50 ) 

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
        
