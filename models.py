import cv2
import numpy as np

class Video:    
    def __init__(self, path):
        self.path = path
        self.cap = cv2.VideoCapture(self.path)
        self.frame = 1
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f'Number of frames: {self.frames}')
        
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
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()
    
    # Create video with space availability text
    def texter(self, start, stop, mask, save_path, space_num = 1, variance = 1000):
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
            space = frame[mask == space_num]
            
            if np.var(space) > variance:
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
            
            
        return f'Change happened from {translator[marks[0]]} at frame {marks.index(int(not marks[0])) + start}'
            
            
                  