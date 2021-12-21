import webvtt
import glob
import os

class transcripts:
    def clean_up_transcripts(dir):
        os.system("mkdir {}".format("semantic_analysis/"+dir+"/txt"))
        for vttfile in glob.glob("semantic_analysis/" + dir+"/*.en.vtt"):
            with open("semantic_analysis/"+dir+"/txt/"+vttfile.split('/')[2].split('.')[0]+".txt", 'w') as txtfile:
                for caption in webvtt.read(vttfile):
                    txtfile.write(str(caption.text)+"\n")
                print(">", "semantic_analysis/"+dir+"/txt/"+vttfile.split('/')[2].split('.')[0]+".txt", " created")
                
