import json
from functools import reduce
from itertools import chain
from datetime import datetime


def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def search_dict(master_dict, words, sep=' > '):

    if not isinstance(master_dict, dict):
        if any([word in master_dict for word in words]):
            return [str(master_dict)]
        else:
            return []
    key_chain = list(filter(None, (search_dict(k, words) for k in master_dict.keys())))
    value_chain = []
    for k, v in master_dict.items():
        for l in search_dict(v, words):
            value_chain.append(f'{k}{sep}{l[0] if isinstance(l, list) else l}')

    # value_chain = list(chain(list(chain(f'{k}{sep}{val}' for val in chain(search_dict(v, words)))) for k,v in master_dict.items()))
    res = list(chain(key_chain, value_chain))
    return res


def search_json(json_path, words, sort_results=True, drop_contained=True, encoding='utf-8'):

    with open(json_path, 'r', encoding=encoding) as fp:
        master_dict = json.load(fp)

    results = search_dict(master_dict, words)
    if drop_contained:
        tmp_res = []
        for el1 in results:
            if sum(1 if el1 in el2 else 0 for el2 in results) == 1:
                tmp_res.append(el1)
        results = tmp_res
    if sort_results:
        results.sort()

    return results


if __name__ == '__main__':
    words = ('דאבי', "5W 7085", "5W 7086", '03', 'city')
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
    print(type(res))
    print('%')
    for l in res:
        print(l)


        




