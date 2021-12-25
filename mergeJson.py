import json

def mergeJson(filename1, filename2, outputFilename):
    with open(filename1) as f1:               # open the file
        data1 = json.load(f1)

    with open(filename2) as f2:                # open the file       
        data2 = json.load(f2)

    oldlen1 = len(data1)
    oldlen2= len(data2)
    
    data1.extend(data2[:])
    assert len(data1) == oldlen1 + oldlen2

    with open(outputFilename, 'w') as out:               # open the file
        json.dump(data1, out)

# mergeJson("channelListResponse_1.json", "channelListResponse_2.json", "channelListResponse.json") #so this actually was already up-to-date with all 56 channelIds because I had enough quota to run it on 56 ids before it gave up in searchListResponse
mergeJson("searchListResponse_1.json", "searchListResponse_2.json", "searchListResponse.json")
mergeJson("videoListResponse_1.json", "videoListResponse_2.json", "videoListResponse.json")