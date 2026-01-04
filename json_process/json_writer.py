struct = {
    "style":[],
    "color":"",
    "text color":"",
    "block type":"",
    "block name":"",
    "block setting":[],
    "struct":[]
}
import json
import os
dir = "./CF_store/"

def write_function(data,filename):

    file_name = filename
    #anti small case
    if os.path.exists(dir+file_name+".json"):
        file_name = filename
    file_dir = dir+file_name+".json"
    directory = os.path.dirname(file_dir)
    os.makedirs(directory, exist_ok=True)
    with open(file_dir, 'w') as f:
        pass
    with open(dir+file_name+".json","w") as file:
        json.dump(data, file)
def create_struct(style = list(),
                  color="",
                  text_color = "",
                  block_type=""
                  ,block_setting=list(),
                  struct = list(),
                  block_name = ""):
    arg_data = []
    arg = locals()
    for item in arg:
        if item !='arg_data':
            arg_data.append((item.replace("_"," "),arg[item]))
    block_struct = {}
    for item in arg_data:
        arg_name,arg_value = item
        block_struct[arg_name] = arg_value
    return block_struct

def struct_gennerate(block_name:str,block_function:str,Npara=1,args=False,bgcolor="",textcolor="",setting=[],filename=""):
    style = [("text",block_name)]
    for i in range(Npara):
        style.append(("para",None))
    color = bgcolor
    textcolor = textcolor
    block_setting = list()
    block_type = "custom"
    for item in setting:
        block_setting.append(item)
    struct = [("code",block_function),("bracket","("),("arg",[]),("adsb",","),("bracket",")")]

    gennerated_struct = create_struct(style=style,color=color,text_color=textcolor,block_type=block_type,
                                      block_setting=block_setting,struct=struct,block_name=block_name)
    write_function(gennerated_struct,filename)


