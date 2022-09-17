import csv
import json
from datetime import datetime
from itertools import chain


def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def search_dict(master_dict, keywords, sep=' > '):
    """
    This function searches a dictionary for given keywords recursively and constructs the paths to keyword found

    Example:
        $>>> dictionary = {'1':
        ...                    '1.2':
        ...                        {'1.2.3': 12},
        ...                    'three': 3
        ...                    }
        ...               }
        $>>> search_dict(dictionary, keywords=['4', '3'])
        ['1 > 1.2 > 1.2.3', '1 > three > 3']
        $>>> search_dict(dictionary, keywords=['2', '0'])
        ['1 > 1.2', '1 > 1.2 > 1.2.3', '1 > 1.2 > 1.2.3 > 12']

    Args:
        master_dict (dict): the dictionary to search
        keywords (list[str]): the given keywords to search for
        sep (str): the string that will separate each node in the path

    Returns:
        list[str]: a list of the found constructed results
    """
    if not isinstance(master_dict, dict):
        if any([word in str(master_dict) for word in keywords]):
            return [str(master_dict)]
        else:
            return []
    key_list = list(filter(None, (search_dict(k, keywords) for k in master_dict.keys())))
    value_list = []
    for k, v in master_dict.items():
        for l in search_dict(v, keywords):
            value_list.append(f'{k}{sep}{l[0] if isinstance(l, list) else l}')

    res = list(chain(key_list, value_list))
    return res


def search_json(file_path, keywords, sort_results=True, drop_contained=True, encoding='utf-8'):
    """
    This function searches a json file using :func:``search_dict``
    Args:
        file_path (str): path to json file
        keywords (list[str]): the given keywords to search for
        sort_results (bool): whether to sort the results or not
        drop_contained (bool): whether to drop results contained in other results or not
        encoding (:obj:str, optional): encoding type

    Returns:
        list[str]: a list of the found constructed results
    """
    with open(file_path, 'r', encoding=encoding) as fp:
        master_dict = json.load(fp)

    results = search_dict(master_dict, keywords)
    if drop_contained:
        tmp_res = []
        for el1 in results:
            if sum(1 if el1.casefold() in el2.casefold() else 0 for el2 in results) == 1:
                tmp_res.append(el1)
        results = tmp_res
    if sort_results:
        results.sort()

    return results


def search_csv(file_path, keywords, sort_results=True, retrieve_field_index=-1, encoding='utf-8'):
    """
    This function searches a csv and for each keyword found returns a value from the same row
    Args:
        file_path (str): path to csv file
        keywords (list[str]):
        sort_results (bool): whether to sort the results or not
        retrieve_field_index (int): index of value to retrieve for the keyword found in the same row
        encoding (:obj:str, optional): encoding type
    Returns:
        list[str]: a list of values retrieved from the rows containing a keyword
    """
    results = []
    with open(file_path, "r", newline='', encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for field in row:
                if any(word.casefold() in field.casefold() for word in keywords):
                    results.append(row[retrieve_field_index])

    if sort_results:
        results.sort()

    return results


if __name__ == '__main__':
    words = ['דאבי', "5W 7085", "5W 7086"]
    d = {
        "flights": {
            "arrivals": {
                "5W 7085 אבו דאבי 17/09": {
                    "airline": "WIZZ AIR ABU DHABI",
                    "city": "אבו דאבי",
                    "flight": "5W 7085",
                    "schedule_date": "17/09",
                    "schedule_time": "18:55",
                    "status": "לא סופי",
                    "terminal": "3",
                    "updated_time": "18:55"
                },
                "6E 4037 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "city": "איסטנבול",
                    "flight": "6E 4037",
                    "schedule_date": "17/09",
                    "schedule_time": "15:45",
                    "status": "לא סופי",
                    "terminal": "3",
                    "updated_time": "15:45"
                },
                "6E 4039 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "city": "איסטנבול",
                    "flight": "6E 4039",
                    "schedule_date": "17/09",
                    "schedule_time": "20:20",
                    "status": "לא סופי",
                    "terminal": "3",
                    "updated_time": "20:20"
                },
                "6E 4041 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "city": "איסטנבול",
                    "flight": "6E 4041",
                    "schedule_date": "17/09",
                    "schedule_time": "19:05",
                    "status": "לא סופי",
                    "terminal": "3",
                    "updated_time": "19:05"
                }
            },
            "departures": {
                "5W 7086 אבו דאבי 17/09": {
                    "airline": "WIZZ AIR ABU DHABI",
                    "checkin_counter": "21-24",
                    "city": "אבו דאבי",
                    "flight": "5W 7086",
                    "schedule_date": "17/09",
                    "schedule_time": "19:45",
                    "status": "בזמן",
                    "terminal": "3",
                    "updated_time": "19:45"
                },
                "6E 4040 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "checkin_counter": "34-41",
                    "city": "איסטנבול",
                    "flight": "6E 4040",
                    "schedule_date": "17/09",
                    "schedule_time": "10:30",
                    "status": "בזמן",
                    "terminal": "3",
                    "updated_time": "10:30"
                },
                "6E 4042 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "checkin_counter": "34-38",
                    "city": "איסטנבול",
                    "flight": "6E 4042",
                    "schedule_date": "17/09",
                    "schedule_time": "14:20",
                    "status": "בזמן",
                    "terminal": "3",
                    "updated_time": "14:20"
                },
                "6E 4044 איסטנבול 17/09": {
                    "airline": "INDIGO AIRLINES",
                    "checkin_counter": "34-40",
                    "city": "איסטנבול",
                    "flight": "6E 4044",
                    "schedule_date": "17/09",
                    "schedule_time": "16:40",
                    "status": "בזמן",
                    "terminal": "3",
                    "updated_time": "16:40"
                },
                "6H 047 אילת - רמון 17/09": {
                    "airline": "ISRAIR AIRLINES",
                    "checkin_counter": "355-360",
                    "city": "אילת - רמון",
                    "flight": "6H 047",
                    "schedule_date": "17/09",
                    "schedule_time": "20:00",
                    "status": "בזמן",
                    "terminal": "1",
                    "updated_time": "20:00"
                }
            }
        }
    }
    res = search_json('flight_data.json', words)
    for l in res:
        print(l)

    print('\n----\n')
    res = search_csv('bbc_articles.csv', ['queen', 'gang', 'loop'])
    print(len(res))
    for r in res:
        print(r)
