import flet as ft
from roll_back import rollback_buffer as rbb
import global_control as gc
import copy as c
#(key(upper),shift,ctrl,alt)
undo = ("Z",False,True,False)
redo = ("Y",False,True,False)
key_buffer = [(undo,"undo"),(redo,"redo")]



def run_shortcut(type):
    # if type=="undo":
    #     print("undo")
    #     print("pointer",gc.globals_rbb.current_pointer)
    #     gc.globals_rbb.undo()
    #     print("befor",gc.global_playground.controls)
    #     content = gc.globals_rbb.get_content()
    #     print(content)
    #     gc.update_content(target=gc.global_playground,
    #                       content=content)
    #     print("after",gc.global_playground.controls)
    #     pass
    # elif type == "redo":
    #     print("redo")
    #     gc.globals_rbb.redo()
    #     content = gc.globals_rbb.get_content()
    #     print("befor", gc.global_playground.controls)
    #     gc.update_content(target=gc.global_playground,
    #                       content=content)
    #     print("after",gc.global_playground.controls)
    #     pass
    pass

def keyboard_listener(e:ft.KeyboardEvent):
    key = e.key
    shift = e.shift
    ctrl = e.ctrl
    alt = e.alt

    key_tup = (key,shift,ctrl,alt)

    for shortcut,type in key_buffer:
        if key_tup == shortcut:
            run_shortcut(type=type)
            pass

