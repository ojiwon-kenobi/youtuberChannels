import requests
from bs4 import BeautifulSoup
import json

YOUTUBERS = [strng.replace(' ', '_') for strng in ['Alex Clark', 'Alex Meyers', 'WowRightMeow', 'Andrei Terbea', 'Billy But Better', 'Casually Explained', 
'CircleToonsHD', 'CurtRichy', 'CypherDen', 'Daidus', 'DanPlan', 'Domics', 'Emirichu', 'EroldStory', 'GradeAUnderA', 
'GetMadz', 'GingerPale', 'Ice Cream Sandwich', 'illymation', 'Ivan Animated', 'Jaiden Animations', 'Let Me Explain Studios', 
'Noodle', 'OverSimplified', 'TheOdd1sOut', 'PantslessPajamas', 'SomeThingElseYT', 'sWooZie', 'Tabbes', 'TheAMaazing', 
'Young Don The Sauce God', 'Young Yong Tales', 'Zalinki']]

youtuber_to_milestone_dict = {}

for youtuber in YOUTUBERS:
    response = requests.get(
        url="https://youtube.fandom.com/wiki/{}".format(youtuber),
    )
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    elems = [elem for elem in soup.findAll('li') if 'million' in str(elem.text)]
    print(len(elems))
    youtuber_to_milestone_dict[youtuber] = elems

with open('youtuber_to_milestone_dict.json', 'w') as outfile:
    json.dump(youtuber_to_milestone_dict, outfile)

#CURRENTLY TAGGED