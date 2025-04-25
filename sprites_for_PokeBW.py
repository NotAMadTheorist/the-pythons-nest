import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re

# Beautiful Soup https://www.crummy.com/software/BeautifulSoup/bs4/doc/

spritesURLs = ["",
               "https://archives.bulbagarden.net/w/index.php?title=Category:Black_and_White_sprites",
               "https://archives.bulbagarden.net/w/index.php?title=Category:Black_and_White_sprites&filefrom=%2A176%0AS"
               "pr+5b+176.png#mw-category-media",
               "https://archives.bulbagarden.net/w/index.php?title=Category:Black_and_White_sprites&filefrom=%2A317%0AS"
               "pr+5b+317+m.png#mw-category-media",
               "https://archives.bulbagarden.net/w/index.php?title=Category:Black_and_White_sprites&filefrom=%2A469%0AS"
               "pr+5b+469.png#mw-category-media",
               "https://archives.bulbagarden.net/w/index.php?title=Category:Black_and_White_sprites&filefrom=%2A633%0AS"
               "pr+5b+634.png#mw-category-media"]

pokedexURL = "C:\\Users\\Acer\\Documents\\Personal Research Notes and Docs\\Programming\\Python\\Code Files\\My Coding " \
             "Projects\\pokemon in python\\Main Code Files\\scraping_files\\pokedex_scraping_csv.csv"
folderURL = "C:\\Users\\Acer\\Documents\\Personal Research Notes and Docs\\Programming\\Python\\Code Files\\My Coding " \
             "Projects\\pokemon in python\\Main Code Files\\scraping_files\\spriteImagesBW"

def reverseInt(num):
    temp = num
    reversed_num = 0

    # Create the reversed integer
    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    return reversed_num

def getPokedex(url: str):
    # Read the data file
    pokedex = pd.read_csv(filepath_or_buffer=url, index_col=False).loc[:, "#":"Name"]
    # loc[:, "#":"Name] - select only the Pokemon number and name

    # Filter out any Mega Evolutions, Galarian and Alolan Forms
    # Ref: https://stackoverflow.com/questions/30791265/how-to-filter-a-pandas-dataframe-by-cells-that-do-not-contain-a-substring
    pokedex = pokedex[~pokedex['Name'].str.contains('\(Mega')]
    pokedex = pokedex[~pokedex['Name'].str.contains('Alolan')]
    pokedex = pokedex[~pokedex['Name'].str.contains('Galarian')]
    pokedex = pokedex[~pokedex['Name'].str.contains('Partner')]

    pd.set_option('display.max_rows', None)
    return pokedex

def downloadSprites(pokedex: pd.DataFrame, pokedexURL: str, folderURL: str, isTestRun: bool = False):
    # Create a handle, named 'page', to handle the contents of the website
    page = req.get(pokedexURL)

    # Extract the HTML contents of the table as a 'Soup' object
    soup = BeautifulSoup(page.text, 'html.parser')
    images = soup.find_all('img')

    sourceURLandFileNames = []

    for imgtag in images[3:-1]:
        source = 'http:' + imgtag['src']
        pokeNumberMatch = re.search(r'\d+$', source[:-4])
        pokeNumber = 000
        if pokeNumberMatch is None:
            sourceReversed = source[-5::-1]
            pokeNumberMatch = re.search(r'\d+', sourceReversed)
            pokeNumber = int(pokeNumberMatch.group()[::-1])
            pokeNote = re.search(r'^[^0-9]', sourceReversed).group()[::-1]
        else:
            pokeNumber = int(pokeNumberMatch.group())
            pokeNote = ''

        # Ref: https://stackoverflow.com/questions/17071871/how-to-select-rows-from-a-dataframe-based-on-column-values
        pokeName = pokedex.loc[pokedex['#'] == pokeNumber].values[0][1]

        fileName = str(pokeNumber) + "_" + pokeName
        if pokeNote is '':
            fileName = str(pokeNumber) + "_" + pokeName + ".png"
        else:
            fileName = str(pokeNumber) + "_" + pokeName + "_" + pokeNote + ".png"

        sourceURLandFileNames.append((source, fileName))

        #print(imgtag['src'], fileName)

    gallerytexts = soup.find_all('div', {'class' : "gallerytext"})
    totalKB = 0
    for gt in gallerytexts:
        kilobytes = reverseInt(int(re.search('\d+', repr(gt)[::-1]).group()))
        totalKB += kilobytes

    print("")
    answer = input(f"Download to directory: {folderURL} \n \n"
                   f"Are you sure to download all {len(sourceURLandFileNames)} images? This process will take up "
                   f"{totalKB} KB of space. Type YES to proceed. \n")
    print("")

    if answer != 'YES':
        print("Download operation aborted.")
        return None

    # Ref: https://www.kite.com/python/answers/how-to-download-an-image-using-requests-in-python
    if not isTestRun:
        for sourceURL, fileName in sourceURLandFileNames:
            print(f"Downloading {fileName} from {sourceURL}")
            sourcePage = req.get(sourceURL)
            spriteFile = open(folderURL + '\\' + fileName, "wb")
            spriteFile.write(sourcePage.content)
            spriteFile.close()
    else:
        for sourceURL, fileName in sourceURLandFileNames:
            print(f"Downloading {fileName} from {sourceURL}")

    print("Download Successful!")


Pokedex = getPokedex(pokedexURL)
downloadSprites(Pokedex, spritesURLs[1], folderURL, isTestRun = True)