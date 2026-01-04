from function_UI import load_local_CF as llcf
import global_control as gc

def replace_data(target,id):
    if id:
        for n,data in enumerate(gc.local_CF_buffer):
            indice,_ = data
            if indice == id:
                gc.local_CF_buffer[n] = (target,id)
                gc.global_func_display.update_content(gc.local_CF_buffer)


def check_for_exist(target,id):
    if id:
        if (target,id) in gc.local_CF_buffer:
            return True
        return False

def add_to_buffer(target,id):
    if id:
        if check_for_exist(target,id):
            replace_data(target,id)
        else:
            gc.local_CF_buffer.append((target,id))

    gc.global_func_display.update_content(gc.local_CF_buffer)


def querry_target(target):
    for item,id in gc.local_CF_buffer:

        if target == id:
            return item
    else:
        return ""

def remove_from_buffer(target):

    bid = querry_target(target)
    gc.local_CF_buffer.remove((bid,target))

    gc.global_func_display.remove(target)




