import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, mode, kurtosis
from keywords import PTYPE
from main import type_multiplier
from collections import Counter


# Prevents Pandas from truncating the table when printed
# always done after producing the data frame!
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

# Read the data file
df = pd.read_csv(filepath_or_buffer="C:\\Users\\Acer\\Documents\\Personal Research Notes and Docs\\04 - Python Code Files (2019-present)\\My Coding Projects\\pokemon in python\\Main Code Files\\scraping_files\\pokedex_scraping_csv.csv", index_col=False).loc[:, "#":]
# loc[:, "#":] - select but the first (unlabeled) column


# SOME SIDE NOTES:
#   a.)   We will be excluding mega evolutions, legendary Pokemon, mythical Pokemon, and Ultra Beasts in our analysis.
#         This is to avoid numerical bias with the majority of regular Pokemon.
#
#   b.)   Whenever a Pokemon has multiple forms (mega evolutions may be optionally counted, but by default are
#         excluded), its base stats are kept separate to allow for differing types.
#
#   c.)   We'll be using the median as our primary measure for central tendency, as opposed to the mean. This is to
#         ensure minimizing outlier bias and to accomodate for the Boxplot diagrams to be shown in comparing a set
#         of generations or statistics.



# Index (#) of the first pokemon in each generation
generations: list = list(range(1, 8+1))
generation_index: dict = {0: 0,
                          1: 152,    # Gen 1 - Kanto (RBY)
                          2: 252,  # Gen 2 - Johto (GSC)
                          3: 387,  # Gen 3 - Hoenn (RSE)
                          4: 494,  # Gen 4 - Sinnoh (DPPt)
                          5: 650,  # Gen 5 - Unova (BW/B2W2)
                          6: 722,  # Gen 6 - Kalos (XY)
                          7: 810,  # Gen 7 - Alola (SM/USUM)
                          8: 1000}  # Gen 8 - Galar (SwSh)
generation_names: dict = {0: 'ALL',
                          1: 'Kanto',
                          2: 'Johto',
                          3: 'Hoenn',
                          4: 'Sinnoh',
                          5: 'Unova',
                          6: 'Kalos',
                          7: 'Alola',
                          8: 'Galar'}


def filtered_dfs(df: pd.DataFrame):

    # Filter out any legendaries and mythicals
    df_regular = df[df["Is Legendary or Mythical?"] == "NO"].loc[:, "#":"Evolves into"]

    # Filter out any non-final evolution but include alternate forms (not megas)
    bool_is_final: list = [("FINAL" in evolves_into) or ("FORM" in evolves_into) for evolves_into
                           in df_regular["Evolves into"]]
    df_regular_final = df_regular[bool_is_final]
    return (df_regular, df_regular_final)


def print_counts(df_regular: pd.DataFrame, df_regular_final: pd.DataFrame):
    print("\n" + f"number of regular Pokemon: {df_regular['#'].nunique()}")
    print(f"number of final evolutions: {df_regular_final['#'].nunique()}")
    print("NOTE: These numbers do not count alternate forms.")
    print("\n")

# Make integer if okay
def make_int(number:float):
    if number % 1 == 0:
        return int(number)
    else:
        return number

# Generator for Histogram Bins
def bin_generator(x_min:float, x_max:float, interval:float):
    x_min = make_int(x_min)
    x_max = make_int(x_max)
    interval = make_int(interval)

    x_accumulate = x_min + interval
    while x_accumulate <= x_max:
        yield x_accumulate
        x_accumulate += interval
    yield x_accumulate

# Test on Any Stat (BST, Speed, etc.) for all fully-evolved regular pokemon
# returns the statistical results
def test_stat(df_regular_final: pd.DataFrame,
              stat:str,
              interval:int = 5,
              is_cumulative:bool = False,
              is_density:bool = True,
              with_plot:bool = True,
              with_printed_results:bool = True,
              up_to_gen:int = 0):

    # Stats
    if up_to_gen <= 0:
        arr_st = df_regular_final[stat].to_numpy()
    else:
        arr_st = df_regular_final[(df_regular_final["#"] <= generation_index[up_to_gen])][stat].to_numpy()

    min_st, max_st = min(arr_st), max(arr_st)

    mode_obj_st = mode(arr_st)
    modes_st = mode_obj_st[0].tolist()
    mode_freq_st = mode_obj_st[1][0]
    stats_st: dict = {"Mean": np.average(arr_st),
                       "Median": np.median(arr_st),
                       "Mode": modes_st,
                       "Standard Deviation": np.std(arr_st),
                       "Quartiles": [int(round(np.quantile(arr_st, x/4), 0)) for x in range(1, 4)],
                       "Range of values": f"{min_st}-{max_st}",
                       "Kurtosis": kurtosis(arr_st)}

    if with_printed_results:
        print(f"RESULTS FOR {'BASE STAT TOTAL' if stat == 'Total' else stat.upper()} -"
              f" UP TO GEN {str(up_to_gen) if up_to_gen > 0 else str(max(generation_index.keys()))}"
              f" ({generation_names[up_to_gen].upper()}):")
        for key, value in stats_st.items():
            if key not in ["Quartiles", "Range of values", "Mode"]:
                if key in ["Kurtosis"]:
                    print(f"{key}: {round(value, 2)}")
                else:
                    print(f"{key}: {int(round(value, 0))}")
            else:
                print(f"{key}: {value}")
        print('\n')

    if with_plot:
        interval_st = interval
        list_bins_st =  list(bin_generator(min_st, max_st, interval_st))
        plt.hist(arr_st, bins = list_bins_st,
                 cumulative=is_cumulative, density=is_density, color="#98b5e3")
        plt.title("Base Stat Total" if stat == "Total" else stat)
        plt.grid(True)

        # plot quartiles
        list_quartile_colors = ['r', 'k', 'r']
        list_quartile_names = ["1st", "2nd", "3rd"]
        for quartile, name, color in zip(stats_st["Quartiles"], list_quartile_names, list_quartile_colors):
            plt.axvline(x=quartile, label=f"{name} Quartile = {quartile}", c=color)

        # plot normal distribution for comparison
        interval_st_curve =  1
        list_x_st_curve =  list(bin_generator(min_st, max_st, interval_st_curve))
        if not is_cumulative:
            list_normal_y = norm.pdf(list_x_st_curve, stats_st["Mean"], stats_st["Standard Deviation"])
            if not is_density:
                hist_area = len(arr_st)*interval
                list_normal_y = hist_area*list_normal_y
        else:
            list_normal_y = norm.cdf(list_x_st_curve, stats_st["Mean"], stats_st["Standard Deviation"])
            if not is_density:
                list_normal_y = len(arr_st)*list_normal_y

        plt.plot(list_x_st_curve, list_normal_y, 'g--')
        plt.legend()
        plt.show()

    return stats_st, arr_st

def test_all_six_stats(df_regular_final: pd.DataFrame,
                       interval: int = 5,
                       is_cumulative: bool = False,
                       is_density: bool = True,
                       with_plot: bool = False,
                       with_printed_results: bool = False,
                       up_to_gen:int = 0):

    six_stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

    dict_measures: dict = {}
    dict_data: dict = {}

    for stat in six_stats:
        some_measures, dict_data[stat] = \
            test_stat(df_regular_final, stat=stat, interval=interval, is_cumulative=is_cumulative,
                      is_density=is_density, with_plot=with_plot, with_printed_results=with_printed_results,
                      up_to_gen=up_to_gen)

        for i in ['Mean', 'Median', 'Standard Deviation']:
            some_measures[i] = int(round(some_measures[i], 0))
        del some_measures['Mean'], some_measures['Mode']
        some_measures['Kurtosis'] = round(some_measures['Kurtosis'], 2)

        #amode = some_measures['Mode']
        #some_measures['Mode'] = amode[0] if len(amode) == 1 else amode

        some_measures['I.Q. Range'] = some_measures['Quartiles'][0::2]
        del some_measures['Quartiles']
        del some_measures['Range of values']

        dict_measures[stat] = some_measures

    # reverse ordering of dict_data
    dict_data_2 = dict(zip(list(dict_data.keys())[::-1], [0]*len(dict_data)))
    dict_data_2 = {key: dict_data[key] for key in dict_data_2.keys()}

    dict_measures_2 = {stat: entry.values() for stat, entry in dict_measures.items()}

    cols_measures = list(dict_measures[six_stats[0]].keys())
    cols_measures = [entry if entry != 'Standard Deviation' else 'St Dev.' for entry in cols_measures]
    df_measures: pd.DataFrame = pd.DataFrame.from_dict(dict_measures_2, orient='index', columns=cols_measures)
    print(f"COMPARISON OF BASE STATS AMONG ALL 6 MEASURES:")
    print(df_measures)
    print("\n")

    colors_stats = ['#FF9F9F',  # HP (red)
                    '#F7BB93',  # Attack (orange)
                    '#FBE99F',  # Defense (yellow)
                    '#BFD0F9',  # Sp. Atk (blue)
                    '#C4E7B3',  # Sp. Def (green)
                    '#FCB2C9']  # Speed (magenta)
    bplot = plt.boxplot(dict_data_2.values(), vert=False, labels=dict_data_2.keys(), patch_artist=True,
                        notch=True)

    for patch, color in zip(bplot['boxes'], colors_stats[::-1]):
        patch.set_facecolor(color)

    plt.title(f'COMPARISON OF BASE STATS AMONG ALL 6 MEASURES:')
    plt.grid(True)
    plt.show()


# Test to compare the stats averaged per generation
def test_stat_per_gen(df_regular_final: pd.DataFrame,
                      stat: str):
    df_gen: dict = dict(zip(generations, [""]*len(generations)))
    stat_data: dict = {}
    stats_stat_gen: dict = dict(zip(generations, [""]*len(generations)))
    stats_stat_list: dict = dict(zip(generations, [""]*len(generations)))

    for gen in df_gen.keys():


        df_gen[gen] = df_regular_final[(df_regular_final["#"] <= generation_index[gen]) &
                                       (df_regular_final["#"] > generation_index[gen - 1])]
        # stat
        arr_stat: np.array = df_gen[gen][stat].to_numpy()
        stat_data[gen] = arr_stat.tolist()

        quartiles = [int(round(np.quantile(arr_stat, x / 4), 0)) for x in range(1, 4)]
        stats_stat_gen[gen]: dict = {"Median": round(np.median(arr_stat)),
                                    "Std Dev": round(np.std(arr_stat)),
                                    "I.Q. Range": [quartiles[0], quartiles[2]],
                                    "# Pokemon": df_gen[gen]["#"].nunique()}
        stats_stat_list[gen]: list = list(stats_stat_gen[gen].values())

    stats_stat_list = {f"Gen {str(gen)}": entries for gen, entries in stats_stat_list.items()}
    stat_data = {f"Gen {str(gen)}": entries for gen, entries in stat_data.items()}

    stats_computed = list(stats_stat_gen[1].keys())
    stats_computed: list = ["Median", "Std Dev", "I.Q. Range.", "# Pokemon"]

    df_stats_stat: pd.DataFrame = pd.DataFrame.from_dict(stats_stat_list, orient='index', columns=stats_computed)
    df_stats_stat = df_stats_stat.sort_values(by="Median", ascending=True)
    stat_data = {gen: stat_data[gen] for gen in df_stats_stat.index}
    df_stats_stat = df_stats_stat.sort_values(by="Median", ascending=False)

    print(f"COMPARISON OF {'BASE STAT TOTAL' if stat == 'Total' else stat.upper()} AMONG ALL GENERATIONS:")
    print(df_stats_stat)
    print("\n")

    plt.boxplot(stat_data.values(), vert=False, labels=stat_data.keys())

    plt.title(f'Comparison of {"Base Stat Total" if stat == "Total" else stat} among all generations')

    plt.grid(True)
    plt.show()


# Test to compute weaknesses in all type combinations of all fully-evolved regular pokemon
def list_of_weaknesses(typeA, typeB, is_levitating:bool = False):
    weaknesses: list = []
    for atype in PTYPE.ALL:
        mult = type_multiplier(atype, typeA, typeB)
        if mult >= 2:
            weaknesses.append(atype)

    if is_levitating:
        if PTYPE.GROUND in weaknesses:
            weaknesses.remove(PTYPE.GROUND)

    return weaknesses

# counting only pokemon with levitate and a weakness to Ground attacks
pokemon_numbers_with_levitate = [92, # Gastly
                                 93, # Haunter
                                 109, # Koffing
                                 110, # Weezing
                                 337, # Lunatone
                                 338, # Solrock
                                 436, # Bronzor
                                 437, # Bronzong
                                 479, # Rotom (all forms)
                                 602, # Tynamo
                                 603, # Eelektrik
                                 604] # Eelektross

def test_weaknesses(df_regular_final: pd.DataFrame,
                    is_cumulative: bool = False,
                    is_density: bool = False,
                    up_to_gen: int = 0):
    if up_to_gen <= 0:
        pass
    else:
        df_regular_final = df_regular_final[(df_regular_final["#"] <= generation_index[up_to_gen])]
    df_regular_final = df_regular_final.loc[:, "#":"Type"]

    poke_numbers = [int(x) for x in df_regular_final["#"].to_numpy().tolist()]
    is_levitating_bool: list = [number in pokemon_numbers_with_levitate for number in poke_numbers]

    type_pairs_packed = df_regular_final["Type"].to_numpy().tolist()
    type_pairs = []
    type_pairs_with_bool = []
    for i in range(len(type_pairs_packed)):
        pair_pack = type_pairs_packed[i]
        if "/" not in pair_pack:
            type_pairs.append((pair_pack, ""))
            type_pairs_with_bool.append((pair_pack, "", is_levitating_bool[i]))
        else:
            typeA, typeB = tuple(pair_pack.split("/"))
            type_pairs.append((typeA, typeB))
            type_pairs_with_bool.append((typeA, typeB, is_levitating_bool[i]))
    del df_regular_final["Type"]
    df_regular_final["Type Pair"] = type_pairs

    type_weaknesses = [list_of_weaknesses(typeA, typeB, is_levitating) for typeA, typeB, is_levitating
                       in type_pairs_with_bool]

    weakness_counter = dict(zip(PTYPE.ALL, [0]*len(PTYPE.ALL)))
    del weakness_counter[""]

    for w_list in type_weaknesses:
        for atype in w_list:
            weakness_counter[atype] += 1
    counter_sum = sum(weakness_counter.values())


    weakness_probabilities = {atype: freq / counter_sum for atype, freq in weakness_counter.items()}
    weakness_percents = {atype: str(round(percent*100, 2))+" %" for atype, percent in weakness_probabilities.items()}
    df_weaknesses = pd.DataFrame.from_dict(weakness_percents, orient='index', columns=['Percent'])\
        .sort_values('Percent', ascending=False)
    print(df_weaknesses)
    print("\n")


    w_counts = [len(sublist) for sublist in type_weaknesses]
    counts_counter = Counter(w_counts)
    counts_sum = sum(counts_counter.values())
    counts_probabilities = {number: freq / counts_sum for number, freq in counts_counter.items()}
    counts_percents = {number: str(round(percent * 100, 2)) + " %" for number, percent in counts_probabilities.items()}

    if is_density:
        df_counts = pd.DataFrame(list(counts_percents.items()), columns=['Weak Types', "Percent"])\
            .sort_values('Weak Types', ascending=True)
    else:
        df_counts = pd.DataFrame(list(counts_counter.items()), columns=['Weak Types', "# Pokemon"]) \
            .sort_values('Weak Types', ascending=True)

    print(df_counts)

    plt.hist(w_counts, bins = list(range(0, max(w_counts)+2)), cumulative=is_cumulative, density=True, color="#98b5e3")
    plt.title("Number of Weaknesses")
    plt.show()


df_regular, df_regular_final = filtered_dfs(df)
print_counts(df_regular, df_regular_final)

test_stat(df_regular_final, "Total", 5, with_plot=True)
test_all_six_stats(df_regular_final)

test_stat_per_gen(df_regular_final, stat='Total')
test_weaknesses(df_regular_final, is_density = True, is_cumulative=False, up_to_gen=5)






