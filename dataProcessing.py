import json
import pandas as pd
from datetime import datetime

LIST_OF_CHANNEL_IDS = [
    "UCsDmESjqNPukDmVnuneLrqw",
    "UCY6Ij8zOds0WJEeqCLOnqOQ",
    "UClN24S5-fc7LD0JJW0FdGWw",
    "UC3iNdSV_RQU7DHTGpqEW96w",
    "UC_52i6mlrzOZs_NEuSepzAg",
    "UCr3cBLTYmIK9kY0F_OdFWFQ",
    "UCV6g95OBbVtFmN9uiJzkFqQ",
    "UCgCKYs56-LKEPGQ99DzqQOg",
    "UCOwxx9VnEnlFKt5EB70KTzQ",
    "UC2Ds30pkifFVD0CE08wF50g",
    "UC7UGbBVrqLlq6CRxWWUmyKw",
    "UCn1XB-jvmd9fXMzhiA6IR0w",
    "UCFeqAfEuKm7lIg2ddQzh61A",
    "UCAlxwHEm1bWWYoe5VCSQYEg",
    "UCz7iJPVTBGX6DNO1RNI2Fcg",
    "UCOAUz4d1NUNxSHh_SOJtdGQ",
    "UCGGTAB19HlHEWPwwmxHsEKA",
    "UCOsATJw-IZgqGT8MFrHjKGg",
    "UCC-slLJZ4p4HOznMUcFn_2g",
    "UCsKVP_4zQ877TEiH_Ih5yDQ",
    "UCOinp9hALPUcZeoL3Kmaviw",
    "UCGwu0nbY2wSkW8N-cghnLpA",
    "UCu6v4AdYxVH5fhfq9mi5llA",
    "UCj74rJ9Lgl3WTngq675wxKg",
    "UCNIuvl7V8zACPpTmmNIqP2A",
    "UCo8bcnLyZH8tBIH9V1mLgqQ",
    "UCR0O-1cvuPNxDosvSDLpWHg",
    "UCvUmwreRrbxeR1mbmojj8fg",
    "UCUKi4zY5ETSqrKAjTBgjM-g",
    "UCDQBZcjYKP1J1Nu-Y0_D37Q",
    "UCQ9HvHH-KRYHI5ynj2kbLwQ",
    "UCRfg0SWjIHm_h95e4V8X5og",
    "UCWPB0WpnMIy-g7zncwIhvQg",
    "UCj6CFdE3LSddaoszxq604TQ",
    "UCXrtqz4fqf-OUEVpp2A1W0w",
    "UChUg_Sd5i74SFoZH2XvagwQ",
    "UC2hm5rD_IrfYRMfq5YQudgA",
    "UC_nEHeUEVNY5ZYLRWg8KoZQ",
    "UCrlzgjrKUa3AlrfSZTBG2fg",
    "UCupWnlhB3PMW1w0CLfLCfug",
    "UCsW0LA-ThH18OCrT9pa2zfQ",
    "UCG-O5k7KKNPABULS20_MAMA",
    "UCepPGz8AVCbggMl3BvboaBA",
    "UCP21EOiKAkCGjv6kqS6UsZw",
    "UC9z7EZAbkphEMg0SP7rw44A",
    "UCZft8Ol-dMtguwam7bWItnw",
    "UCYaxncRvOBu-vtdhxf6qciA",
    "UCte3qx7A5OWTPSnNjV4oheg",
    "UCRei8TBpt4r0WPZ7MkiKmVg",
    "UC6bXfhbiX1PsSi_-pdQeHjg",
    "UC_7lgWbCA_HZQkaxmmQgNoA",
    "UCQO_C1sfUCpUzzV-gxQ-lxA",
    "UCHw-JjzU80GKrGJwI1Uf1OQ",
    "UCDEaY2XwwfKomQAJgGfehWw",
    "UCI-92EMS3ZJ11gz-S_oyaSA",
    "UC7Mk9RmlKT_x8FAsMOJn1cg",
    "UC9i7x4EzTBlNvslu1wWEB8Q",
    #=======
    "UCnsem444vdU1HhS0mb2wwTA",
    "UCnbtlei4RJMHWSUq4LKn_SQ", 
    "UC9i7x4EzTBlNvslu1wWEB8Q",
    "UC1nM46_BMKq4vd4jmd6iMHA",
    "UCMNxwlfY6P5Rm40QOp8Hqsg"
]
def createChannelIdToListOfVids():
    df = pd.read_json (r'searchListResponse.json')
    channelIdToListOfVids = {} #channelId: []vids

    #initialize the dicts
    for channelId in LIST_OF_CHANNEL_IDS:
        channelIdToListOfVids[channelId] = []

    # #youtuber
    # #0~9ish: items
    # #items: 0~46ish
    count= 0

    for index, midList in df.iterrows():  
        listOfLists = df.iat[index, index]
        for indList in listOfLists:
            for item in indList['items']:
                channelId = item['snippet']['channelId']
                if 'videoId' in item['id'].keys():
                    snippet=item['snippet']
                    vidId = item['id']['videoId']
                    publishTime = snippet['publishTime']
                    vidTitle = snippet['title']
                    vidDesc = snippet['description']

                    vidInfo = {'vidId' : vidId,
                    'publishTime': publishTime,
                    'vidTitle': vidTitle}
                    channelIdToListOfVids[channelId].append(vidInfo)
                    count+=1

    print(len(channelIdToListOfVids.keys()), " keys detected")
    vidCont=0
    for i in channelIdToListOfVids.keys():
        vidCont+=len(channelIdToListOfVids[i])
    print(count, " videos detected")

def flattenList(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

def addVideoMetaDataAndRemoveMusicVids():
    df = pd.read_json (r'videoListResponse.json')
    backend_purposes= {}
    for channelId in LIST_OF_CHANNEL_IDS:
        backend_purposes[channelId]=[]

        matching_vidId_to_info={}
        count = 0
        debugMsg = []
        setOfTypes = []
        for index, indList in df.iterrows():
            items = indList['items']
            for item in items:
                count+=1
                vidId = item['id']
                channelId = item['snippet']['channelId']
                contentDetails= item['contentDetails']
                duration= contentDetails['duration']
                statistics = item['statistics']
                viewCount = statistics['viewCount']
                likeCount = statistics.get('likeCount')
                commentCount = statistics.get('commentCount')
                description = item['snippet']['description']
                if (likeCount == None or commentCount == None):
                    print(vidId, "has", "likes" if likeCount == None else '', "comments" if commentCount == None else '', "disabled")
                topicCategories = []
                if item.get('topicDetails') != None:
                    topicCategories = item.get('topicDetails').get('topicCategories')
                    setOfTypes.append([i for i in topicCategories])
                if True not in ['music' in strng.lower() for strng in topicCategories] or item.get('topicDetails') == None: #all videos that are not music-typed or just don't have a type
                    matching_vidId_to_info[vidId] = {'duration': duration,
                                    'viewCount': int(-1 if viewCount is None else viewCount),
                                    'likeCount': int(-1 if likeCount is None else likeCount),
                                    'commentCount': int(-1 if commentCount is None else commentCount),
                                    'topicCategories': topicCategories,
                                    'description': description}
                    backend_purposes[channelId].append(vidId)
                else: #all videos that are music-typed
                    debugMsg.append(vidId)

        vidIdsCollected =0 
        for i in backend_purposes.keys():
            vidIdsCollected += len(backend_purposes[i])
        print(vidIdsCollected, " videos to run semantic analysis on")
        print(set(flattenList(setOfTypes)))
        print("There were ", 4971-len(matching_vidId_to_info), " videos categorized as music-videos") 
