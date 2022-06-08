import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
from time  import sleep
import threading
from google.cloud import pubsub_v1
import json
import time


#looks for a perticular service key in the json format
cred = credentials.Certificate("serviceAccountKey.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceAccountKey.json'
firebase_admin.initialize_app(cred)

publisher=  pubsub_v1.PublisherClient()
topic_path ='projects/digital-twin-experiment/topics/RawMaterial'
RELAY_PIN_rawMaterialA = 16
RELAY_PIN_rawMaterialB = 5
RELAY_PIN_poistion15 = 6
RELAY_PIN_poistion3 = 19
RELAY_PIN_poistion1= 20
RELAY_PIN_pistonAssembly= 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(RELAY_PIN_rawMaterialA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(RELAY_PIN_poistion15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN_poistion3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN_poistion1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN_pistonAssembly, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db = firestore.client()

#create an event for notifying main thread 

callback_done  = threading.Event()

boolValue = None
class CallBack:
    @classmethod
    def button_callback_rawMaterialA(AB,CB):
        print(" working")
        # if the GPIO relay pin is high it will update the firebase as False
        if GPIO.input(RELAY_PIN_rawMaterialA) == GPIO.HIGH:
          
            topic_path =publisher.topic_path('digital-twin-experiment','RawMaterial')
            attributes ={
                "Raw_Material_Name": "A",
                "State": True
                }
            data=json.dumps(attributes).encode("utf-8")
            
            
            db.collection('Scenario-2').document('9GOwnU3Heub3NZL1eTNd').update(
               {
                   'rawMaterialA' : False
                   }
               )
            print("ITs working2")
           
            future = publisher.publish(topic_path,data)
            future.result()
        else:
            
             # if the GPIO relay pin is high it will update the firebase as False
            db.collection('Scenario-2').document('9GOwnU3Heub3NZL1eTNd').update(
               {
                   'rawMaterialA' : True
                   }
               
               )
            
               
          
           
    '''def button_callback_rawMaterialB(channel,opt):
        print("ITs working")
        # if the GPIO relay pin is high it will update the firebase as False
        if GPIO.input(RELAY_PIN_rawMaterialB) == GPIO.HIGH:
             
            db.collection('Scenario-2').document('9GOwnU3Heub3NZL1eTNd').update(
               {
                   'rawMaterialB' : False
                   }
               
               )
        else:
             # if the GPIO relay pin is high it will update the firebase as False
            db.collection('Scenario-2').document('9GOwnU3Heub3NZL1eTNd').update(
               {
                   'rawMaterialB' : True
                   }
               
               )      

# create callback on_snapshot fuction to capture changes'''
 
            

#doc_ref = db.collection(u'testC').document(u'testD')

#watch the document 
if __name__== '__main__':
    cb = CallBack()
    def on_snapshot(doc_snapshot, changes ,  read_time):
    
            for doc in doc_snapshot:
                docDict = doc.to_dict()
                startOperation = docDict['startOperation']
                print('Recived document snapshot: {doc.id}, startOperation = {startOperation}')
                global boolValue
                boolValue = startOperation
                if boolValue == True:
                    GPIO.output(26, False) 
                    sleep(2) 
                    GPIO.output(26, True)
    doc_ref = db.collection(u'Scenario-2').document(u'9GOwnU3Heub3NZL1eTNd')
    doc_watch = doc_ref.on_snapshot(on_snapshot)
    GPIO.add_event_detect(RELAY_PIN_rawMaterialA, GPIO.BOTH,callback= cb.button_callback_rawMaterialA,bouncetime=50 ) 
#GPIO.add_event_detect(RELAY_PIN_rawMaterialB, GPIO.BOTH,callback= cb.button_callback_rawMaterialB,bouncetime=50 )
    callback_done.set()
      
    


    
                      
                      
while True:
    print(boolValue)
    sleep(0.5)
    

#set the  variables in the google cloud firebase 
#db.collection('Listening_function').document('RELAY_M_A').set(   
#     {
 #       'value':False
 #       }
    
 #   )
#call back fuction 

# waits for Relay pin(GPIO-16) to get high and call for a call back fuction(button_callback)
#GPIO.add_event_detect(RELAY_PIN, GPIO.BOTH,
 #                     callback= button_callback,bouncetime=50 ) 

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
        