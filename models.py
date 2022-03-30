import cv2
import numpy as np
import json
from datetime import datetime
import pytz
import requests
from twilio.rest import Client

class Video:
    
    with open('mask.npy', 'rb') as f:
        mask = np.load(f)
        
    space_nums = [(1, 995, 760, 3, 4),(3, 1140, 760, 3, 4),(5, 838, 760, 3, 4),(7, 1284, 760, 3, 4), (9, 700, 760, 3, 4),
              (2, 1018, 350, 1, 4),(4, 1110, 350, 1, 4),(6, 924, 350, 1, 4),(8, 1194, 350, 1, 4), (10, 826, 350, 1, 4),
              (11, 1390, 760, 3, 4), (13, 540, 760, 3, 4), (14, 744, 350, 1, 4), (12, 1260, 350, 1, 4)]
    
    def __init__(self, path):
        self.path = path
        self.cap = cv2.VideoCapture(self.path)
        self.frame = 1
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.variance = 1800           
        
        print(f'Number of frames: {self.frames}')
        print(f'Image path > {self.path}')
        
    def show(self, gray = False):
        frame = self.read
        if gray == True:
            frame = self.gray
        cv2.imshow(f'frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    @property
    def read(self):
        self.cap.set(1, self.frame)
        ret, frame = self.cap.read()
        return frame
    
    @property
    def gray(self):
        frame = self.read
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray
    
    @property
    def play(self):
        if (self.cap.isOpened()== False):
            print("Error opening video stream or file")
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                cv2.imshow('Frame',frame)
                if cv2.waitKey(15) & 0xFF == ord('q'):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()

    @property
    def show_mask(self):
        frame = self.read
        frame[self.mask > 0] = np.array([200, 0, 100])
        self.space_ids(frame)
        cv2.imshow(f'frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def save_mask(self, path):
        frame = self.read
        frame[self.mask > 0] = np.array([200, 0, 100])
        self.space_ids(frame)
        cv2.imwrite(path, frame)
        
    @property    
    def ids(self):
        frame = self.read
        self.space_ids(frame)
        cv2.imshow(f'frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    @property
    def var(self):
        frame = self.read
        variances = {}
        for space_id in range(1,15):
            space = frame[self.mask == space_id]
            variances[space_id] = np.var(space)
        return variances

    # draw numbers on spaces
    def space_ids(self, frame, colors = None):
        for space in self.space_nums:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (space[1], space[2])
            fontScale = space[3]
            if colors:
                color = [(0,0,255),(0,255,0)][colors[space[0]]]
            else:
                color = (210, 210, 210)
            thickness = space[4]
            frame = cv2.putText(frame, str(space[0]), org, font, 
                               fontScale, color, thickness, cv2.LINE_AA)
    
    #paste variances on imige
    def paste_var(self, frame, variances, frame_num = 0):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        frame = cv2.putText(frame, 'Color varinaces', (100, 100), font, fontScale, (0,0,0), thickness, cv2.LINE_AA)
        frame = cv2.circle(frame, (1640, 100), 15, (0,255,0), -1)
        frame = cv2.circle(frame, (1640, 150), 15, (0,0,255), -1)
        frame = cv2.putText(frame, 'Unoccupied', (1690, 110), font, fontScale, (0,255,0), thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Occupied', (1690, 160), font, fontScale, (0,0,255), thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, str(frame_num), (1690, 1040), font, fontScale, (0,0,0), 4, cv2.LINE_AA)
        colors = {}
        for space_id, var in variances.items():          
            org = (100, space_id*50 + 100)
            if var > self.variance:
                color = (0, 0, 255)
                c = 0
            else:
                color = (0, 255, 0)
                c = 1
            phrase = f'{space_id}: {int(var)}'
            frame = cv2.putText(frame, phrase, org, font, 
                               fontScale, color, thickness, cv2.LINE_AA)
            
            
            colors[space_id] = c
        return colors
                       
   
    @property    
    def show_var(self):
        frame = self.read
        variances = self.var
        colors = self.paste_var(frame, variances)
        print(colors)
        self.space_ids(frame, colors)
        cv2.imshow(f'frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    # write frame with variances and colored numbers
    def save_var(self, path):
        frame = self.read
        variances = self.var
        colors = self.paste_var(frame, variances)
        self.space_ids(frame, colors)
        cv2.imwrite(path, frame)
    
    
    def save_video_var(self, path, start = 1, stop = None):
        if not stop:
            stop = self.frames
        size = int(self.cap.get(3)), int(self.cap.get(4))
        result = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), 1, size)
        for i in range(start, stop):
            if i%5==0:
                print(f'frame {i}/{stop}')
            self.frame = i
            frame = self.read
            variances = self.var
            colors = self.paste_var(frame, variances, i)
            self.space_ids(frame, colors)
            result.write(frame)
           
    
    # Create video with space availability text
    def texter(self, start, stop, save_path, space_num = 1):
        size = int(self.cap.get(3)), int(self.cap.get(4))
        result = cv2.VideoWriter(save_path,cv2.VideoWriter_fourcc(*'MJPG'),10, size)
        font = cv2.FONT_HERSHEY_SIMPLEX#font = cv2.FONT_HERSHEY_SIMPLEXS
        org = (500, 1000)
        fontScale = 3
        color = (0, 0, 255)
        thickness = 3
        
        marks = []
        for i in range(start, stop):
            self.frame = i
            frame = self.read
            space = frame[self.mask == space_num]
            
            if np.var(space) > self.variance:
                frame = cv2.putText(frame, 'Space is occupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
                marks.append(1)
                #print(1)
            else:
                frame = cv2.putText(frame, 'Space is unoccupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
                marks.append(0)
                #print(0)
                
            result.write(frame)
            
        translator = {0 : 'Free', 1 : 'Occupied'}
            
        if int(not marks[0]) in marks:  
            return f'Change happened from {translator[marks[0]]} at frame {marks.index(int(not marks[0])) + start}'
        return 'No change happened for asked frame range!'
    
    def states(self, start, stop, space_num = 1):
        marks = []
        for i in range(start, stop):
            self.frame = i
            frame = self.read
            space = frame[self.mask == space_num]
            
            if np.var(space) > self.variance:
                marks.append(1)

            else:
                marks.append(0)
            
        translator = {0 : 'Free', 1 : 'Occupied'}
            
        if int(not marks[0]) in marks:  
            return f'Change happened from {translator[marks[0]]} at frame {marks.index(int(not marks[0])) + start}', marks
        return 'No change happened for asked frame range!', marks
            
            
    def img_texter(self, frame_num, save_path, space_num = 1):
        
        font = cv2.FONT_HERSHEY_SIMPLEX#font = cv2.FONT_HERSHEY_SIMPLEXS
        org = (500, 1000)
        fontScale = 3
        color = (0, 0, 255)
        thickness = 3
        
        self.frame = frame_num
        frame = self.read
        space = frame[self.mask == space_num]
            
        if np.var(space) > self.variance:
            frame = cv2.putText(frame, 'Space is occupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
        else:
            frame = cv2.putText(frame, 'Space is unoccupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
            
        cv2.imwrite(save_path, frame)
        
        
    def state(self, frame_num, space_num = 1):
        
        self.frame = frame_num
        frame = self.read
        space = frame[self.mask == space_num]
            
        if np.var(space) > self.variance:
            frame = print('Space is occupied')
        else:
            frame = print('Space is unoccupied')

    def write(self, start, stop):
        for i in range(start, stop):
            self.frame = i
            frame = self.read
            variances = self.var
            with open('variances.json', 'w') as f:
                json.dump(variances, f, indent = 4)
                
        return variances

    def tracker_fake(self, ac, at, tw, tracker, start = 0, stop = None):
        print(tracker)
        local = {}
        for i in range(start, stop):
            with open('sms_maper.json', 'r') as f:
                maper = json.load(f)
            self.frame = i
            frame = self.read
            variances = self.var
            if i % 10 == 0:
                for timestamp, (tracked_parking_space, id)  in tracker.items():
                    local[tracked_parking_space] = maper[id]
            for tracked_parking_space, sms in local.items():
                #print(local, i)
                if variances[tracked_parking_space] < self.variance:
                    print(self.variance, variances[tracked_parking_space], i)
                    moment = datetime.now()
                    moment = moment.strftime("%H:%M:%S")
                    self.massage(ac, at, tw, sms, moment, tracked_parking_space)
                    return f'Vehicle has left parking space {tracked_parking_space}, at {moment}. \nFrame {i}'


    def massage(self, ac, at, tw, sms, moment, tracked_parking_space):
        client = Client(ac, at)
        my_msg = f"Vehicle has left parking space {tracked_parking_space}, at {moment}"
        message = client.messages.create(to=sms, from_=tw, body=my_msg)


    def tracker(self, ac, at, tw, admin_password, data_url, stoper_url, start = 0, stop = None):
        for frame_number in range(start, stop):
            active = {}
            if frame_number % 10 == 0:
                data = self.data(admin_password, data_url)
                for person in data['active']:
                    if person['COLLEAGUE'] and person['STATUS']:
                        active[person['ID']] = (person['SPACE'], person['PHONE'])
            self.frame = frame_number
            frame = self.read
            variances = self.var
            for id, listing in active.items():
                space = listing[0]
                phone = listing[1]
                if variances[space] < self.variance:
                    del active[id]
                    print(self.variance, variances[space], id)
                    moment = datetime.now()
                    moment = moment.strftime("%H:%M:%S")
                    self.massage(ac, at, tw, phone, moment, space)
                    self.stoper(admin_password, stoper_url, id)
                    return f'Vehicle has left parking space {space}, at {moment}. \nFrame {i}'


    def data(self, admin_password, data_url):
        url = data_url
        data = {'password':admin_password}
        r = requests.post(url, data = data)
        return r.json()

    def stoper(self, admin_password, stoper_url, id):
        url = stoper_url
        data = {'password':admin_password, 'user_id': id}
        r = requests.post(url, data = data)

            




