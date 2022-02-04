import cv2
import numpy as np

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
    def space_ids(self, frame):
        for space in self.space_nums:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (space[1], space[2])
            fontScale = space[3]
            color = (210, 210, 210)
            thickness = space[4]
            frame = cv2.putText(frame, str(space[0]), org, font, 
                               fontScale, color, thickness, cv2.LINE_AA)
    
    #paste variances on imige
    def paste_var(self, frame, variances):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        frame = cv2.putText(frame, 'Color varinaces', (100, 100), font, fontScale, (0,0,0), thickness, cv2.LINE_AA)
        frame = cv2.circle(frame, (1640, 100), 15, (0,255,0), -1)
        frame = cv2.circle(frame, (1640, 150), 15, (0,0,255), -1)
        frame = cv2.putText(frame, 'Unoccupied', (1690, 110), font, fontScale, (0,255,0), thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Occupied', (1690, 160), font, fontScale, (0,0,255), thickness, cv2.LINE_AA)
        for space_id, var in variances.items():          
            org = (100, space_id*50 + 100)
            if var > 1500:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            phrase = f'{space_id}: {int(var)}'
            frame = cv2.putText(frame, phrase, org, font, 
                               fontScale, color, thickness, cv2.LINE_AA)
                       
   
    @property    
    def show_var(self):
        frame = self.read
        variances = self.var
        self.paste_var(frame, variances)
        self.space_ids(frame)
        cv2.imshow(f'frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    def save_var(self, path):
        frame = self.read
        variances = self.var
        self.paste_var(frame, variances)
        self.space_ids(frame)
        cv2.imwrite(path, frame)
   
    
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
            
        if int(not marks[0]) in marks:  
            return f'Change happened from {translator[marks[0]]} at frame {marks.index(int(not marks[0])) + start}'
        return 'No change happened for asked frame range!'
    
    def states(self, start, stop, mask, space_num = 1, variance = 1000):
        marks = []
        for i in range(start, stop):
            self.frame = i
            frame = self.read
            space = frame[mask == space_num]
            
            if np.var(space) > variance:
                marks.append(1)

            else:
                marks.append(0)
            
        translator = {0 : 'Free', 1 : 'Occupied'}
            
        if int(not marks[0]) in marks:  
            return f'Change happened from {translator[marks[0]]} at frame {marks.index(int(not marks[0])) + start}', marks
        return 'No change happened for asked frame range!', marks
            
            
    def img_texter(self, frame_num, mask, save_path, space_num = 1, variance = 1000):
        
        font = cv2.FONT_HERSHEY_SIMPLEX#font = cv2.FONT_HERSHEY_SIMPLEXS
        org = (500, 1000)
        fontScale = 3
        color = (0, 0, 255)
        thickness = 3
        
        self.frame = frame_num
        frame = self.read
        space = frame[mask == space_num]
            
        if np.var(space) > variance:
            frame = cv2.putText(frame, 'Space is occupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
        else:
            frame = cv2.putText(frame, 'Space is unoccupied', org, font, 
                                   fontScale, color, thickness, cv2.LINE_AA)
            
        cv2.imwrite(save_path, frame)
        
        
    def state(self, frame_num, mask, space_num = 1, variance = 1000):
        
        self.frame = frame_num
        frame = self.read
        space = frame[mask == space_num]
            
        if np.var(space) > variance:
            frame = print('Space is occupied')
        else:
            frame = print('Space is unoccupied')