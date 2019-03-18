from pandas import read_csv, Grouper, Series
from collections import Counter
from tabulate import tabulate

flattened_labels = []

def print_stats(file_name, board_name):
    print('########################')
    print("{}".format(board_name))
    print('########################')
    pd = read_csv(filepath_or_buffer=file_name,sep=';', parse_dates=['created_at'])
    pd['weekday'] = pd['created_at'].apply(lambda x: x.weekday())
    pd['week'] = pd['created_at'].apply(lambda x: x.week)
    pd['just_date'] = pd['created_at'].dt.date
    
    flattened_labels.clear()
    def reduce_labels(x):
        global flattened_labels
        flattened_labels = flattened_labels + x

    pd['labels'] = pd['labels'].apply( lambda x: x.replace('[','').replace(']','').replace("'",'').strip().split(','))
    pd.labels.apply(reduce_labels)

    counts = Counter(flattened_labels)
    
    print()
    most_common = counts.most_common(10)
    print(tabulate(most_common, headers=['label', 'count']))
    # for stat in most_common:
    #     print("{},      {}".format(stat[0].replace("'",'').strip(), stat[1]))
    print('\n\n')
