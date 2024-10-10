import cv2
import queue
import time
import threading
import numpy as np
from termcolor import colored

from Shoplifting import Alert
from Shoplifting.data_pip_shoplifting import Shoplifting_Live
import os
from keras.models import model_from_json
import warnings
warnings.filterwarnings("ignore")

# Disabling TensorFlow AVX/FMA warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def get_abuse_model_and_weight_json():
    # Paths to the model and weights
    weight_abuse = r"E:\FINAL_PROJECT_DATA\2021\Silence_Vision__EDS_Demo\Event_detection\Event_weight\Abuse\weights_at_epoch_3_28_7_21_round2.h5"
    json_path = r"E:\FINAL_PROJECT_DATA\2021\Yolov5_DeepSort_Pytorch-master\EMS\model_Abuse_at_epoch_3_28_7_21_round2.json"
    
    # Loading model architecture
    with open(json_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    
    abuse_model = model_from_json(loaded_model_json)
    
    # Loading model weights
    abuse_model.load_weights(weight_abuse)
    print("Loaded EMS model and weights from disk")
    return abuse_model

# Initializing necessary objects and flags
q = queue.Queue(maxsize=3000)
frame_set = []
Frame_set_to_check = []
Frame_INDEX = 0
lock = threading.Lock()
Email_alert_flag = True  # Assuming you want email alerts

# Initialize email alert system and shoplifting detection system
email_alert = Alert.Email_Alert()
shoplifting_SYS = Shoplifting_Live()
W = 0
H = 0

# Video source path
src_main_dir_path = r"E:\FINAL_PROJECT_DATA\2021\test_shoplifting"
video_cap_ip = r"E:\FINAL_PROJECT_DATA\2021\shoplifting_video.avi"

def Receive():
    global W, H
    cap = cv2.VideoCapture(video_cap_ip)
    W = int(cap.get(3))
    H = int(cap.get(4))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[-] End of video stream or cannot fetch frame.")
            break
        q.put(frame)

def Display():
    global Frame_set_to_check, Frame_INDEX
    while True:
        if not q.empty():
            frame = q.get()
            if frame is None:
                print("[-] NoneType frame received.")
                break

            frame_set.append(frame.copy())

            # Once we collect 149 frames, trigger prediction
            if len(frame_set) == 149:
                Frame_set_to_check = frame_set.copy()
                frame_set.clear()
                Pred()
                time.sleep(1)  # Add slight delay for processing

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def Pred():
    global Frame_set_to_check, Frame_INDEX

    with lock:
        # Loading the model for shoplifting detection
        shoplifting_SYS.load_model_and_weight_gate_flow_slow_fast_RGB()
        
        Frame_set_to_check_np = np.array(Frame_set_to_check.copy())
        Frame_set = shoplifting_SYS.make_frame_set_format(Frame_set_to_check_np)
        
        reports = shoplifting_SYS.run_StealsNet_frames_check_live_demo_2_version(Frame_set, Frame_INDEX)
        Frame_INDEX += 1

        Bag, Clotes, Normal, state, event_index = reports

        # If shoplifting is detected
        if state:
            print(colored(f"Detected shoplifting event at Frame {Frame_INDEX-1}", 'green'))
            found_fall_video_path = shoplifting_SYS.save_frame_set_after_pred_live_demo(
                src_main_dir_path, Frame_set_to_check, Frame_INDEX-1, [Bag, Clotes, Normal], 0, W, H)

            if Email_alert_flag:
                file_name = os.path.basename(found_fall_video_path)
                email_alert.send_email_alert(email_alert.user_email_address3, file_name, found_fall_video_path)
        else:
            print(colored(f"Normal activity at Frame {Frame_INDEX-1}", 'red'))

        Frame_set_to_check.clear()
        time.sleep(1)

if __name__ == '__main__':
    # Start video capture and frame processing in separate threads
    threading.Thread(target=Receive).start()
    threading.Thread(target=Display).start()
