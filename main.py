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
"UC5e3Q5ydbj30UQufBZm5wHA",
"UCj74rJ9Lgl3WTngq675wxKg",
"UCo8bcnLyZH8tBIH9V1mLgqQ",
"UCR0O-1cvuPNxDosvSDLpWHg",
"UCQ9HvHH-KRYHI5ynj2kbLwQ",
"UCvUmwreRrbxeR1mbmojj8fg",
"UCWPB0WpnMIy-g7zncwIhvQg",
"UCUKi4zY5ETSqrKAjTBgjM-g",
"UCDQBZcjYKP1J1Nu-Y0_D37Q",
"UCRfg0SWjIHm_h95e4V8X5og",
"UCC-slLJZ4p4HOznMUcFn_2g"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRETS_FILE = "client_secret.json"

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
    with open('channelData.json', 'w') as file:
        json.dump(pool_result, file)
    


if __name__ == "__main__":
    pass
    # main()