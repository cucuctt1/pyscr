import re

def check_type(inputData):
    if inputData.lower() == "none":
        return None
    else:
        try:
            return int(inputData)
        except ValueError:
            try:
                return float(inputData)
            except ValueError:
                return f'{inputData}'


def extract_empty_head(input_string):
    match = re.match(r'^(\s*)', input_string)
    if match:
        print(1,match.group(1),1)
        return match.group(1)
    else:
        return ""

