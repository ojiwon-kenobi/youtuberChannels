import webvtt
import glob
import os

class transcripts:
    def clean_up_transcripts(dir):
        os.system("mkdir {}".format(dir+"/"+"txt"))

        for vttfile in glob.glob(dir+"/*.en.vtt"):
            print("!!", vttfile)
            with open(dir+"/txt/"+vttfile.split('/')[1].split('.')[0]+".txt", 'w') as txtfile:
                for caption in webvtt.read(vttfile):
                    txtfile.write(caption.text)


