import blocklogic as b
import stack as st
import flet as ft
import random_req as rq
from function_UI import create_func as cf
import copy as c
from function_UI import func_display as fd
from utility.color_palette import *
from json_process import json_reader as jrd, json_writer as jwt
import os
# globals_rbb = rbb.rollback_buffer()






global_playground = st.stack_buffer()
global_page = None

local_CF_buffer = []
local_class_buffer = []
global_variable_buffer = [] #var name
globals_class_manager = None
class_buffer = []
class_method_buffer = {}
global_class_display = fd.class_display(wid=300-40,hei=1000,page=global_page
                                      ,parent=global_playground,buffer=local_class_buffer)
global_func_display = fd.func_display(wid=300-40,hei=1000,page=global_page
                                      ,parent=global_playground,buffer=local_CF_buffer)
def update_content(target:ft.Stack = None,content=None):
    target.controls = content
    try:
        target.update()
    except:
        pass

def remove_def(string):
    if string.startswith("def "):
        return string[4:]
    else:
        return string


def update_class(target,remove_list = None):
    if target.class_id not in class_buffer:
        class_buffer.append(target.class_id)
        class_method_buffer[target.class_id] = []
        globals_class_manager.add_class(target.name,bgcolor ="#FFF3C7",id=rq.generate_random_string(10))

    class_index = class_buffer.index(target.class_id)
    if remove_list:
        for item in remove_list:
            try:
                index = class_method_buffer[target.class_id].index(item.block_setting[0])
                globals_class_manager.remove_function(class_index,index)
                class_method_buffer[target.class_id] = class_method_buffer[target.class_id][:index]
                target.func_buffer = target.func_buffer[:index]
                break
            except:
                pass
    for n,func in enumerate(target.func_buffer):
        #read
        func_id = func.block_setting[0]
        if func_id not in class_method_buffer[target.class_id]:
            filename = func.block_setting[0]+".json"
            root = "CF_store/"
            struct = jrd.read_json(os.path.join(root,filename))
            if struct:
                npara = func.Npara
                func_block = b.block(x=0,y=0,Npara=npara,struct=struct,have_parameter=True)
                globals_class_manager.add_function(func_block,class_index)
                class_method_buffer[target.class_id].append(func_id)
        else:
            filename = func.block_setting[0]+".json"
            root = "CF_store/"
            struct = jrd.read_json(os.path.join(root,filename))
            if struct:
                npara = func.Npara
                func_block = b.block(x=0, y=0, Npara=npara, struct=struct, have_parameter=True)
                try:
                    globals_class_manager.update_function(class_index,func_block,n)
                    globals_class_manager.update()
                except:
                    pass


def update_class_name(target):
    class_index = class_buffer.index(target.class_id)
    globals_class_manager.class_buffer[class_index][0].class_name= target.name
    col = globals_class_manager.class_buffer[class_index][0].text_color
    globals_class_manager.class_buffer[class_index][0].header = ft.ListTile(title=ft.Text(value=target.name,color=col))
    try:
        globals_class_manager.update()
    except:
        pass

def remove_class(target):
    try:
        index = class_buffer.index(target.class_id)
        class_buffer.remove(class_buffer[index])
        globals_class_manager.remove_class(index)
    except:
        pass

