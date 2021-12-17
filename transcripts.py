import webvtt
import glob

def clean_up_transcripts():
    for vttfile in glob.glob("vtt/*"):
        with open("txt/"+vttfile.split('/')[1].split('.en.')[0]+".txt", 'w') as txtfile:
            for caption in webvtt.read(vttfile):
                txtfile.write(caption.text)

clean_up_transcripts()


