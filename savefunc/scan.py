import blocklogic as b


def scan(content):
    for data in content:
        break
        if data.upper_code and data.upper_code.block_name == "class" and data.block_name == "def":
            print(data)