import os
from json_process import (json_writer as jwt)
import random_req as rr
from utility.color_palette import *


def remove_def(string):
    if string.startswith("def "):
        return string[4:]
    else:
        return string
def get_data(data,target):
    if data['block setting']:
        block_dir = data['block setting'][0]
    else:
        block_dir = ""

    block_name = data['block name']

    if block_name == "def":
        if block_dir:
            npara = target.Npara
            function_name = data['style'][1][1]
            function_code = remove_def(data['struct'][0][1])
            color = CF_c
            text_color = "#000000"

            jwt.struct_gennerate(function_name, function_code, Npara=npara, bgcolor=color, textcolor=text_color,
                                 setting=[block_dir], filename=block_dir)

        else:

            npara = target.Npara
            function_name = data['style'][1][1]
            function_code = remove_def(data['struct'][0][1])
            block_dir = rr.generate_random_string(10)
            color = CF_c
            text_color = "#000000"
            jwt.struct_gennerate(function_name,function_code,Npara=npara,bgcolor=color,textcolor=text_color,setting = [block_dir],filename=block_dir)


        send_data(target,block_dir)

def send_data(target,data):
    if target.template['block setting']:
        target.template['block setting'][0] = data
    else:
        target.template['block setting'].append(data)
    target.load_template()