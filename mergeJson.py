import json

def mergeJsonLists(filename1, filename2, outputFilename):
    with open(filename1) as f1:               # open the file
        data1 = json.load(f1)

    with open(filename2) as f2:                # open the file       
        data2 = json.load(f2)

    if isinstance(data1, list) and isinstance(data2, list):
        oldlen1 = len(data1)
        oldlen2= len(data2)
        data1.extend(data2[:])
        assert len(data1) == oldlen1 + oldlen2
        with open(outputFilename, 'w') as out:               # open the file
            json.dump(data1, out)

mergeJsonLists("channelListResponse_1.json", "channelListResponse_2.json", "channelListResponse.json")
mergeJsonLists("searchListResponse_1.json", "searchListResponse_2.json", "searchListResponse.json")
mergeJsonLists("videoListResponse_1.json", "videoListResponse_2.json", "videoListResponse.json")