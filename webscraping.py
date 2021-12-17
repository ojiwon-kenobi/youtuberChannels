import requests
from bs4 import BeautifulSoup
import regex as re
response = requests.get(
	url="https://youtube.fandom.com/wiki/OverSimplified",
)
print(response.status_code)
soup = BeautifulSoup(response.content, 'html.parser')
elems = [elem for elem in soup.findAll('li') if 'million' in str(elem.text)]
print(len(elems))