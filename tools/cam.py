import cv2
import time
import datetime
import os 
import sys
sys.path.append(os.path.dirname(__file__))
from utils import *
#cap.set(cv2.CAP_PROP_POS_FRAMES,int(frame_count/2))
#milliseconds = 1000*60
#cap.set(cv2.CAP_PROP_POS_MSEC, milliseconds)
def get_cam_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return {"fps":fps,"frame_count":frame_count}
def show_cam_prop(cap:cv2.VideoCapture):
    fps,frame_count=list(get_cam_properties(cap).values())
    duration = frame_count/fps
    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration/60)
    seconds = duration%60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
def video_saver(file_name,video_capture,fourcc=cv2.VideoWriter_fourcc("m","p","4","v")
    ,start_time=0,end_time=999999999,fps_v=None,funct=None):
    h,w=video_capture.read()[1].shape[:2]
    
    fps,frame_count=list(get_cam_properties(video_capture).values())
    duration = frame_count/fps
    end_time=min(end_time,duration)
    start_time=min(start_time,end_time)
    start_frame=int(fps*start_time)
    end_frame=int(fps*end_time)
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    if fps_v is None:
        fps_v=fps
    out=cv2.VideoWriter(file_name,fourcc,fps_v,(w,h))
    for _ in progressBar(list(range(start_frame,end_frame)), prefix = 'Progress:', suffix = 'Complete', length = 50):
        success,frame=video_capture.read()
        if not success:break
        if not funct is None:
            frameNumber=video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            frame=funct(frame,frameNumber=frameNumber,fps=fps)
        out.write(frame)
    out.release()
def conver_frames2video(file_name,
        frames,fourcc=cv2.VideoWriter_fourcc("m","p","4","v"),
    fps_v=20,funct=None):
    h,w=frames[0].shape[:2]
    out=cv2.VideoWriter(file_name,fourcc,fps_v,(w,h))
    for id,frame in enumerate(progressBar(frames, prefix = 'Progress:', suffix = 'Complete', length = 50)):
        if not funct is None:
            frame=funct(frame,frameNumber=id,fps=fps_v)
        out.write(frame)
    out.release()
#fps the number of frames per sconds
class FPS():
    def __init__(self):
        self.start_t=0
    @staticmethod
    def calculate_fps(time_passed,frames):
        return frames/time_passed
    def start(self):
        self.start_t=time.time()
    def end(self):
        starttime=self.start_t
        self.start_t=time.time()
        return (1/(time.time()-starttime))
class VIDEO_SAVER(cv2.VideoWriter):
    def __init__(self,file_name,fourcc=cv2.VideoWriter_fourcc("m","p","4","v")
         ,fps=20.0,shape=(1024,1024),frames=[]):
        time_stamp=datetime.datetime.now().strftime("%H-%M-%S")
        folder_name=datetime.datetime.now().strftime("%d-%m-%Y")
        capture_vedio=cv2.VideoWriter()
        for frame in frames:
            self.write(frame)
    def save(self):
        return super().release()
     
        