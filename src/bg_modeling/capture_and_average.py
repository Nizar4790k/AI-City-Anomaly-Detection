import cv2
import os
import sys
import glob
import tqdm
from pathlib import Path
from natsort import natsorted
import numpy as np
import json
# video_name = sys.argv[1]

dest_dir = "Data/ori_images/"

def get_videos():
  
  
  with open('Data/dataset.json', 'r') as f:
    data = json.load(f)

  
  videos = data['videos']

  return videos  


ori_images_txt = open("ori_images.txt","w")
videos = get_videos()

print("caputure videos")
for video in tqdm.tqdm(videos):
    file_name = video['name'].split('.')[0]
    folder_name = dest_dir+file_name.split('.')[0]
    
    os.makedirs(folder_name,exist_ok=True)
    vc = cv2.VideoCapture(video['path'])
    
    c = 1
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False

    timeF =1   # 视频帧计数间隔频率

    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        pic_path = folder_name+'/'
        if (c % timeF == 0 and rval):  # 每隔timeF帧进行存储操作
            # print(pic_path + str(c) + '.jpg')
            cv2.imwrite(pic_path + str(c) + '.jpg', frame)  # 存储为图像,保存名为 >文件夹名_数字（第几个文件）.jpg
            ori_images_txt.write("../AI-City-Anomaly-Detection/"+pic_path+str(c)+'.jpg')
            ori_images_txt.write('\n')
        
        c = c + 1
        cv2.waitKey(1)
    vc.release()

dest_dir_processed = "Data/processed_images/"

print("average images")

for video in tqdm.tqdm(videos):
    video_name = video['name'].split('.')[0]
    path_file_number=glob.glob(os.path.join(dest_dir,video_name,'*.jpg')) 
    internal_frame = 4
    start_frame = 100
   
    nums_frames = len(path_file_number)
    alpha=0.1
    Path(dest_dir_processed+video_name).mkdir(exist_ok=True)

    for j in range(4,5):
        internal_frame = 100
        num_pic = int(nums_frames)
        former_im = cv2.imread(dest_dir+video_name+"/100.jpg")
        
        img = cv2.imread(os.path.join(dest_dir,video_name,str(start_frame)+'.jpg'))
        for i in range(num_pic):
            # print(os.path.join(dest_dir,video_name,str(start_frame)+'.jpg'))
            # print(os.path.join(dest_dir,video_name,str(i*internal_frame+start_frame)+'.jpg'))
            now_im = cv2.imread(os.path.join(dest_dir,video_name,str(i*internal_frame+start_frame)+'.jpg'))
            if now_im is not None:
              if np.mean(np.abs(now_im-former_im))>5:
                  img = img*(1-alpha)+now_im*alpha
                  cv2.imwrite(dest_dir_processed+video_name+'/'+str(i*internal_frame+start_frame)
                        +'_'+str(j)+'.jpg',img)
              else:
                  cv2.imwrite(dest_dir_processed+video_name+'/'+str(i*internal_frame+start_frame)
                        +'_'+str(j)+'.jpg',img*0)
              former_im = now_im

