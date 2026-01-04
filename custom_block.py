#create struct from custom code
#save struct to file
#out put block
import json_process
from random_req import *
import os
save_dir = "struct/"


def generate_contrasting_color(hex_color, brightness_threshold=128):
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = sum(rgb_color) / 3
    target_brightness = 255 if brightness < brightness_threshold else 0
    ratio = target_brightness / brightness if brightness != 0 else 1
    adjusted_color = tuple(min(max(int(value * ratio), 0), 255) for value in rgb_color)
    hex_contrasting_color = "#{:02X}{:02X}{:02X}".format(*adjusted_color)

    return hex_contrasting_color
class custom_block():
    def __init__(self,code = None,arg_mode = 1,args = False,kwargs = False,sidedot = False,function_name = None):
        self.code = code
        self.arg_mode = arg_mode
        self.args = args
        self.kwargs = kwargs
        self.sidedot = sidedot
        self.function_name = function_name
    def create_struct(self):
        struct = list()
        style = [("text",None),("para",None)]
        struct.append(style)
        if self.sidedot:
            struct.append(("adsb","."))
        struct.append(("code",self.code))
        struct.append(("bracket","("))
        if self.arg_mode ==1:
            struct.append(("arg",None))
        else:
            struct.append(("arg", []))
        struct.append(("bracket",")"))
        return struct

    def save_to_json(self):
        data = self.create_struct()
        self.file_name = generate_random_string(10)+".json_process"
        dir = save_dir+self.file_name
        with open(dir, 'w') as file:
            json_process.dump(data, file)
        if not os.path.exists('struct/file_dic.json'):
            with open('struct/file_dic.json','w') as file:
                data = []
                json_process.dump(data, file, indent=2)
        color = generate_random_color()
        text_color = generate_contrasting_color(color)
        self.save_to_dic(self.file_name,color,text_color)

    def save_to_dic(self,file_name,color,text_color):
        data = {
            'filename':file_name,
            'func_name':self.function_name,
            'color':color,
            'text_color':text_color
        }

        with open('struct/file_dic.json','r') as file:
            data_buffer = json_process.load(file)
            if len(data_buffer)>=1 and not data_buffer[0]:
                data_buffer = data_buffer[1:]
            with open('struct/file_dic.json','w') as file:
                    data_buffer.append(data)
                    json_process.dump(data_buffer, file, indent=2)


def read_json(jsonfile):
    with open(jsonfile, 'r') as file:
        json_data = json_process.load(file)

    style = json_data[0]
    json_data = json_data[1:]
    for n,item in enumerate(style):
        item = tuple(item)
        style[n] = item
    for n,item in enumerate(json_data):
        item = tuple(item)
        json_data[n] = item
    json_data.insert(0,style)
    return json_data


