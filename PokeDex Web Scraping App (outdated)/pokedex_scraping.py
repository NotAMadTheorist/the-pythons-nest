#
# REFERENCES:  https://www.youtube.com/watch?list=PLuVTNX0oceI87L2sPUTODZmwn-ORos-9Z&v=egYVP-TeSg8&feature=emb_logo
#              https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
#
# Note that the code shown here is quite different from the one obtainable through the links. Some variable names
# ... have been changed for clarity and ease of reading. But there have been new functions and processes that I've
# ... added in by myself as the original code doesn't work as I expected. These major changes include the correction
# ... function, configuring the table display, time measurement and the method of which data is dumped onto the table.

import requests as req
import lxml.html as lh
import pandas as pd

from time import time
from re import sub

from keywords import PTYPE


# Correction Tuples
ptypes = tuple(map(lambda x: x.capitalize(),  PTYPE.ALL))
pokemon_numbers_with_long_names = (122,  # Mr. Mime
                                   439,  # Mime Jr.
                                   474,  # Porygon-Z
                                   772,  # Type: Null
                                   785,  # Tapu Koko
                                   786,  # Tapu Lele
                                   787,  # Tapu Bulu
                                   788,  # Tapu Fini
                                   866)   # Mr. Rime


def correction(raw_data: str):
    """a table-specific function which corrects text information per row of the table and returns it in a more suitable
    form for display.  Returns a list of all data values in the row."""

    split_raw = raw_data.split("\\n", -1)
    split_raw.pop()   # removes the last entry ("") after the last \\n
    split_raw.pop(0)  # removes the first entry which is also empty ("")

    split_remaining: list = split_raw[1:len(split_raw)]  # the remaining data values (base stats)

    region_raw: str = split_raw[0]   # represents the first three columns (without the \\n's!)
    region_fixed_list: list = sub(r"([A-Z])", r" \1", region_raw).split()   # list of words without spaces

    # regex sub formula from:  https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters

    # pokedex number of the Pokemon
    data_number = region_fixed_list[0]

    # check if it has a name with more than 1 word
    if int(data_number) in pokemon_numbers_with_long_names:  # make sure to convert to an integer before comparing
        has_single_word_name: bool = False
    else:
        has_single_word_name: bool = True

    # name of the Pokemon
    if has_single_word_name:
        data_name = region_fixed_list[1]
    else:
        data_name = region_fixed_list[1] + " " + region_fixed_list[2]

    # check if dual type or not
    is_dual_type = (region_fixed_list[-1] in ptypes) and (region_fixed_list[-2] in ptypes)

    # type(s) of the Pokemon
    if is_dual_type:
        data_ptype = region_fixed_list[-2] + "/" + region_fixed_list[-1]   # order matters (left to right)
    else:
        data_ptype = region_fixed_list[-1]

    # check for any special names
    region_fixed_list.pop(0)  # removes the number
    region_fixed_list.pop(0)  # removes the main

    if not has_single_word_name:
        region_fixed_list.pop(0)  # removes the second word in the main name (if there's any)

    region_fixed_list.pop()   # removes one of the types
    if is_dual_type:
        region_fixed_list.pop()    # removes the other type should there be two

    if region_fixed_list != []:  # if there is a special name, add it to the name of the pokemon in parentheses
        special_name: str = " ".join(region_fixed_list)
        data_name = data_name + f" ({special_name})"

    data_all_values = [data_number, data_name, data_ptype] + [int(x) for x in split_remaining]
    return data_all_values


url = "https://pokemondb.net/pokedex/all"


def pokedex_data_frame():

    # Create a handle, named 'page', to handle the contents of the website
    page = req.get(url)

    # Store the contents of the website under the variable 'doc'
    doc = lh.fromstring(page.content)

    # Parse data that are stored in each row (tr) of the table in the HTML source for the website
    row_elements = doc.xpath('//tr')
    # Create an empty list for the columns of each row
    cols = []
    row_i = 0

    # For the first row, store append to cols a tuple containing the first element (header) and
    # ... its own list holding all the data values below it
    for cell in row_elements[0]:
        row_i += 1
        name = cell.text_content()
        cols.append((name, []))

    row_size = 10    # the intended number of entries per row

    # Data is stored on the second row onwards.
    for j in range(1, len(row_elements)):
        R = row_elements[j]   # represents the j'th row

        # If the row is not of the right size, this row data can't be considered in our table
        if len(R) != row_size:
            break

        # i is the index of our row
        i = 0

        # Row in raw string format
        data = repr(R.text_content())

        # BUT, our text content isn't formatted correctly. If you print its representation (repr), notice that the
        # ... first 3 columns aren't spaced by new lines (\n).
        #   ex.)  WRONG:   \n001 BulbasaurGrass Poison\n318\n45\n49\n49\n65\n65\n45\n
        #
        # We therefore have to correct it before placing all the data into 'cols', which connects to the table.
        #   ex.)  CORRECT:   \n001\nBulbasaur\nGrass and Poison\n318\n45\n49\n49\n65\n65\n45\n
        #
        # These changes are done with a correction function separate from the loop, since different tables may have
        # ... differing corrections, while some simple ones don't need such.

        data_list = correction(data)

        # Iterate through each element of the row
        for i in range(row_size):
            cols[i][1].append(data_list[i])


    # Assemble the dictionary for the data frame.
    # Dictionary Comprehension!  (a new concept indeed)
    frame_dict: dict = {title: column for (title, column) in cols}
    data_frame = pd.DataFrame(frame_dict)

    # Prevents Pandas from truncating the table when printed
    # always done after producing the data frame!
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)


    return data_frame


# print the table (max number of rows = 1034 as of September 6, 2020)
# df.head(n) - first n rows of the table
# df.tail(n) - last n rows of the table
n = 1034

elapsed_start = time()
data_frame = pokedex_data_frame()
elapsed_end = time()
elapsed = round(elapsed_end - elapsed_start, 2)

#row = next(data_frame.iterrows())[1]
data_frame.to_csv(path_or_buf="C:\\Users\\Acer\\Documents\\Personal Research Notes and Docs\\Programming\\Python\\Code"
                              " Files\\My Coding Projects\\pokemon in python\\Main Code Files\\scraping_files\\pokedex_"
                              "scraping_csv_0.csv")

print(data_frame.head(n))    # all columns have dtype 'object'
#print('')
#print(data_frame.at[3, "Name"])


print(f"Time taken: {elapsed} s")
