import json


def tuple_transform(itemlist:list):
    new_list = list()
    for item in itemlist:
        new_list.append(tuple(item))
    return new_list
def read_json(jsonfile):
    try:
        with open(jsonfile, 'r') as file:
            json_data = json.load(file)
            object = {}
            for key, value in json_data.items():
                if isinstance(value, list):
                    if key != "block setting":
                        object[key]=tuple_transform(value)
                    else:
                        object[key] = value
                else:
                    object[key] = value
            return object
    except:
        return {}

