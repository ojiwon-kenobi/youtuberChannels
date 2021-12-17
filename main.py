# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

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
"UCC-slLJZ4p4HOznMUcFn_2g"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRETS_FILE = "client_secret.json"
LIST_OF_UPLOAD_IDS = ['UU' + ids[2:] for ids in LIST_OF_CHANNEL_IDS]

# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import os
import multiprocessing as mp
import time
import json
import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import client # Added
from oauth2client import tools # Added
from oauth2client.file import Storage # Added

def get_authenticated_service(): # Modified
    credential_path = os.path.join('./', 'credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Credentials are invalid")
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

results=[]
youtubeApiClient = get_authenticated_service()

def get_result(result):
    results.append(result)

def collect_channel_info(channelId):
    ts = time.time()
    response= youtubeApiClient.channels().list(part="snippet, contentDetails, statistics", id=channelId).execute()
    print(channelId, ' took ', time.time() - ts, 'in parallel')
    return response

def main():
    # execute_youtube_api_and_collect_data(LIST_OF_CHANNEL_IDS[3])
    pool = mp.Pool(mp.cpu_count())
    pool_result=pool.map(collect_channel_info, LIST_OF_CHANNEL_IDS)
    pool.close()
    pool.join()
    print(pool_result)
    with open('channelListResponse.json', 'w') as file:
        json.dump(pool_result, file)

def collect_videos_initial_page(channelId):
    ts = time.time()
    request = youtubeApiClient.search().list(
        part="snippet",
        channelId=channelId,
        maxResults=50,
    )
    response = request.execute()
    response_list = [response]
    while ("nextPageToken" in response):
        nextPageToken = response["nextPageToken"]
        response = collect_videos_using_pageToken(channelId, nextPageToken)
        response_list.append(response)
    print(channelId, ' took ', time.time() - ts, 'in parallel')
    return {channelId: response_list}

def collect_videos_using_pageToken(channelId, pageToken):
    ts = time.time()
    request = youtubeApiClient.search().list(
        part="snippet",
        channelId=channelId,
        maxResults=50,
        pageToken=pageToken
        )
    response = request.execute()
    print("pageToken", ' took ', time.time() - ts, 'in parallel')
    return response

def collect_videos():
    pool= mp.Pool(mp.cpu_count())
    pool_result= pool.map(collect_videos_initial_page, LIST_OF_CHANNEL_IDS)
    pool.close()
    pool.join()
    print("done")
    with open('searchListResponse.json', 'w') as file:
        json.dump(pool_result, file)

def collect_vidInfo_execute(ids):
    ts=time.time()
    request = youtubeApiClient.videos().list(
        part="statistics,contentDetails,status,topicDetails",
        id=ids
    )
    response = request.execute()
    print("videos ", ' took ', time.time() - ts, 'in parallel')
    return response

def process_list_of_videoIds():
    with open('listOfVideoIds.json', 'r') as j:
        listOfVidIds = json.loads(j.read())
    return set(listOfVidIds)

def process_dict_of_channelId_to_listOfVidIds():
    with open('masterSheet.json', 'r') as j:
        dictOfChannelIdToListOfVidInfos = json.loads(j.read())
    return dictOfChannelIdToListOfVidInfos

def collect_videoInfo():
    listOfVidIds = process_list_of_videoIds()
    pool= mp.Pool(mp.cpu_count())
    n=50
    print(len([listOfVidIds[k:k+n] for k in range(0, len(listOfVidIds), n)]))
    print(len(listOfVidIds))
    pool_result= pool.map(collect_vidInfo_execute, [listOfVidIds[k:k+n] for k in range(0, len(listOfVidIds), n)])
    pool.close()
    pool.join()
    print("done")
    with open('videoListResponse.json', 'w') as file:
        json.dump(pool_result, file)

def process_list_of_mostViewedVideoIds():
    with open('channelId_to_mostViewedVidId.json', 'r') as j:
        dict = json.loads(j.read())
        print(len(list(dict.values())))
    return list(dict.values())

def collect_video_mp4s():
    listOfMostViewedVidIds = process_list_of_mostViewedVideoIds()
    print(listOfMostViewedVidIds)
    for mostViewedVidId in listOfMostViewedVidIds:
        url = "https://www.youtube.com/watch?v=" + mostViewedVidId
        os.system("youtube-dl -f 134 """"{}"""" ".format(url))    

def collect_video_captions():
    dictOfChannelIdToListOfVidInfos = process_dict_of_channelId_to_listOfVidIds()
    for channelId in LIST_OF_CHANNEL_IDS:
        os.mkdir(channelId)
        for vidInfo in dictOfChannelIdToListOfVidInfos[channelId]:
            vidId = vidInfo['vidId']
            url = "https://www.youtube.com/watch?v=" + vidId
            os.system("youtube-dl --output """"{}/{}"""" --write-sub --write-auto-sub --sub-lang en --skip-download """"{}"""" ".format(channelId, vidId, url))    

if __name__ == "__main__":
    # main()
    # collect_videos()
    # collect_videoInfo()
    collect_video_captions()