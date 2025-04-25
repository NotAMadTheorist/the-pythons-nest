from bs4 import BeautifulSoup
from requests import get
from sys import maxsize
import numpy as np
import pandas as pd
import re

URL = 'https://pokemondb.net/pokedex/gible'

# Request the URL to copy the information contained within it
content = get(URL)

# Extract the HTML contents of the table with class 'wikitable sortable' as a 'Soup' object.
soup = BeautifulSoup(content.text, 'html.parser')
soupSection = soup.find('div', {'class' : 'infocard-list-evo'})

contentSection:list = []
contentColumns: list = ['#', 'Pokémon', 'Requirement']
for x in str(soupSection.get_text()).split('\n'):
    item = re.sub('[()]', '', x).split('#')
    if item != [""]:
        words = item[1].split(" ")
        number, name = words[0], words[1]
        item = [number, name, item[0]]
        contentSection.append(item)
contentDF = pd.DataFrame(np.array(contentSection),  columns=contentColumns)
print(contentDF)