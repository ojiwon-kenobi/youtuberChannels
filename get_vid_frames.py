import cv2
import numpy as np
import youtube_dl
import json
import os

def process_list_of_mostViewedVideoIds():
    with open('channelId_to_mostViewedVidId.json', 'r') as j:
        dict = json.loads(j.read())
        print(len(list(dict.values())))
    return list(dict.values())

def collect_video_frames():
    listOfMostViewedVidIds = process_list_of_mostViewedVideoIds()
    print(listOfMostViewedVidIds)
    for mostViewedVidId in listOfMostViewedVidIds:
        os.mkdir("frames/" + mostViewedVidId)
        url = "https://www.youtube.com/watch?v=" + mostViewedVidId
        ydl_opts = {}

        ydl = youtube_dl.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(url, download=False)

        formats = info_dict.get('formats',None)
        count = 0
        for f in formats:

            # I want the lowest resolution, so I set resolution as 144p
            if f.get('format_note',None) == '360p':

                url = f.get('url',None)
                cap = cv2.VideoCapture(url)

                if not cap.isOpened():
                    print('video not opened')
                    exit(-1)

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    resized = cv2.resize(frame, (256,256), interpolation = cv2.INTER_AREA)
                    cv2.imwrite("frames/{}/{}.png".format(mostViewedVidId, str(count).zfill(5)), resized)  
                    count+=1
                cap.release()

collect_video_frames()