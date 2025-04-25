import requests as req
import lxml.html as lh
import pandas as pd
import numpy as np

url = "https://bulbapedia.bulbagarden.net/wiki/Venusaur_(Pok%C3%A9mon)"
page = req.get(url)


def data_array(xpath, i=0):
    global url, page
    html_table = lh.fromstring(page.content).xpath(xpath)[i]
    str_table = lh.etree.tostring(html_table)
    try:
        data = np.array(pd.read_html(str_table)[0])
        return(data)
    except:
        pass

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

for i in [0, 20, 37, 54, 69]:
    print(i)
    print(data_array('//table[@class="roundy"]', i), '\n'*4)