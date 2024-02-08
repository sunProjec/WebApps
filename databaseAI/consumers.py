import json
from channels.generic.websocket import WebsocketConsumer
import base64
import cv2
import numpy as np
from keras.models import load_model
import cv2,os 
import numpy as np
import mediapipe as mp
from googletrans import Translator
from google_trans_new import google_translator 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
current_time = 0
model = load_model('./CNN_0-9.h5')
mphands = mp.solutions.hands
hands = mphands.Hands(max_num_hands=2)  # Set max_num_hands to 2
mp_drawing = mp.solutions.drawing_utils
result_P = "null"
confidence_P = ""
analysisframe = ''
b = os.path.dirname(os.path.abspath(__file__))
#translator =Translator(service_urls=['translate.googleapis.com'])


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type' : 'connection_established',
            'massage':'You are now connected'

        }))
        

    def receive(self, text_data):
        #text_data_json =json.loads(text_data)
        #message = text_data_json['message'] 

        #decoded_data = base64.b64decode(text_data)
        #np_data = np.fromstring(decoded_data,np.uint8)
        #img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
        
        #print('Message:',message)
                try: 
                        encoded_data = text_data.split(',')[1]
                        data = base64.b64decode(encoded_data)
                        np_arr = np.fromstring(data, np.uint8)
                        img1 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        #print(img1)
                        frame=img1
                        
                        
                        #print(frame)
                        h, w, c = frame.shape
                
                        
                        analysisframe = frame
                        framergbanalysis = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2RGB)
                        resultanalysis = hands.process(framergbanalysis)
                        hand_landmarksanalysis = resultanalysis.multi_hand_landmarks
                        if hand_landmarksanalysis and (len(hand_landmarksanalysis) == 1 or len(hand_landmarksanalysis) == 2):
                            x_max = 0
                            y_max = 0
                            x_min = w
                            y_min = h
                            for handLMsanalysis in hand_landmarksanalysis:
                                for lmanalysis in handLMsanalysis.landmark:
                                    x, y = int(lmanalysis.x * w), int(lmanalysis.y * h)
                                    if x > x_max:
                                        x_max = x
                                    if x < x_min:
                                        x_min = x
                                    if y > y_max:
                                        y_max = y
                                    if y < y_min:
                                        y_min = y
                                    # Draw dots on hand landmarks
                                    mp_drawing.draw_landmarks(analysisframe, handLMsanalysis, mphands.HAND_CONNECTIONS)
                            y_min -= 20
                            y_max += 20
                            x_min -= 20
                            x_max += 20

                            analysisframe = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2RGB) 
                            analysisframe = analysisframe[y_min:y_max, x_min:x_max]
                            #cv2.imwrite('./data/2.jpg', analysisframe)
                            analysisframe = cv2.resize(analysisframe,(32,32)) 
                            x_pre = np.array(analysisframe)
                            x_pre = x_pre.astype('float32')
                            x_pre = x_pre/255
                            x_pre = np.reshape(x_pre ,(1,32,32,3))
                            prediction = model.predict(x_pre)
                            print(prediction)

                            label = ['BOOK','STREET','FOOD','RUN','Fully','CAR','TELEVISION','LIKE','COMPUTER','GLASS']
                            #label = ['หนังสือ','ถนน','อาหาร','วิ่ง','เต็ม','รถ','ทีวี','ชอบ','คอมพิวเตอร์','แก้ว']
                            result = label[np.argmax(prediction)]
                            confidence = round(np.max(prediction) * 100, 2)
                            print("Predicted real ", result)
                            print('Confidence : ', confidence)

                            #last_prediction_time = current_time
                            result_P = result
                            confidence_P = confidence
                            # Draw result and confidence on the frame
                            cv2.putText(frame, f"Result: {result_P}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            cv2.putText(frame, f"Confidence: {confidence_P}%", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            print(result)
                
                            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            result = hands.process(framergb)
                            hand_landmarks = result.multi_hand_landmarks
                            if hand_landmarks:
                                for handLMs in hand_landmarks:
                                    x_max = 0
                                    y_max = 0
                                    x_min = w
                                    y_min = h
                                    for lm in handLMs.landmark:
                                        x, y = int(lm.x * w), int(lm.y * h)
                                        if x > x_max:
                                            x_max = x
                                        if x < x_min:
                                             x_min = x
                                        if y > y_max:
                                            y_max = y
                                        if y < y_min:
                                             y_min = y
                                    y_min -= 20
                                    y_max += 20
                                    x_min -= 20
                                    x_max += 20
                                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        
                        #try:
                            #eng = translator.translate(result_P,dest='th')
                            #print(f'{eng.text}')
                            

                        #except Exception as e:
                             #print(e)
                        #eng = translator.translate(result_P,dest='th')
                        #print(f'{eng.text}')
                        with open(b +"\\templates\\sun.txt", 'w',encoding='utf-8') as file:   
                                file.write(result_P)
                                #file.write(result_P+"\n"+eng.text)
                        _, buffer = cv2.imencode('.jpg', frame)
                        uri = base64.b64encode(buffer).decode('utf-8')
                    #f'data:image/jpg;base64,{uri}'
                        
                        #try:
                            #self.send(eng.text)
                        #except Exception as e:
                             #print(e)
                        self.send(f'data:image/jpg;base64,{uri}')
                except:
                    try:
                       self.send(text_data)
                    except Exception as e:
                         print(e)
                    
         #except:
        # just in case some process is failed
        # normally, for first connection
        # return the original data
                #self.send(text_data)
        #cv2.imshow("test", img)
                #return text_data
        #data=base64.b64decode(text_data)
        #print(data)
        #self.send(grayscale(text_data))
        #self.send(text_data=json.dumps({
         #  'type':'chat',
          #  'message':message
        #}))

   