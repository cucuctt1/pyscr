import pickle
import ast
import blocklogic as b
import flet as ft
import stack as st
import global_control as gc
from function_UI import local_CF_buffer as lCFb
def read_file(filename):
    data = []
    Bid = []
    upper_data = []
    below_data = []
    side_block_data = []
    hook_data = []
    para_data = []
    contain_data = []
    block_var = []
    class_ids = []
    with open(filename,"r+") as f:
        lenght = int(f.readline())
        for index in range(lenght):
            data.append(pickle.loads(ast.literal_eval(f.readline())))
            Bid.append(f.readline().strip())
            upper_data.append(f.readline().strip())
            below_data.append(f.readline().strip().split(" "))
            side_block_data.append(f.readline().strip())
            hook_data.append(f.readline().strip())
            contain_data.append(f.readline().strip().split(" "))
            para_data.append(f.readline().strip().split(" "))
            block_var.append(f.readline().strip().split(" "))
            class_ids.append(f.readline().strip())
        global_var = f.readline().strip().split(" ")
    return (data,Bid,upper_data,below_data,side_block_data,hook_data,contain_data
                  ,para_data,block_var,global_var,class_ids)

def load_to_new_obj(data):
    (IsContainer, HaveParameter, IsHeader, Executable, id,
    left,
    top,
    block_height,
    block_width,
    name,
    Npara,
    template,
    args,
    clone_para,
    clone_restrict,
    in_display,class_id) = data

    block = b.block(iscontainer=IsContainer,have_parameter=HaveParameter,
                    isheader=IsHeader,executable=Executable,
                    id=id,x=left,y=top,block_height=block_height,block_width=block_width,
                    name=name,Npara=Npara,
                    struct=template,args=args,
                    clone_para=clone_para,clone_restrict=clone_restrict,
                    indisplay=in_display)
    block.class_id = class_id
    block.class_update()
    return block

def load_to_block(filename):
    block_buffer = []
    (data, Bids, upper_data, below_data, side_block_data, hook_data, contain_data
     , para_data,var_data,global_var,class_ids) = read_file(filename)

    for property in data:
        block = load_to_new_obj(property)
        block_buffer.append(block)

    # relationship assign
    for index,block in enumerate(block_buffer):
        for data in below_data[index]:
            if data:
                indice = Bids.index(data)
                block_buffer[index].add_to_below(block_buffer[indice])

        for data in contain_data[index]:
            if data:
                indice = Bids.index(data)
                block_buffer[index].add_to_contain(block_buffer[indice])

        for slot,data in enumerate(para_data[index]):
            if data != "None" and data and len(data)==10:
                indice = Bids.index(data)
                block_buffer[index].add_to_para(block_buffer[indice],slot)
            elif data != "None" and data and len(data)>10:

                block_buffer[index].arg_buffer[slot].content.value = data[10:]
                data_len = int(len(data[10:]) * 10 - (len(data[10:]) * 0.553333))
                block_buffer[index].change_wid(data_len,block_buffer[index].arg_buffer[slot])


        block_buffer[index].reset_height()

        if side_block_data[index]:
            if data:
                indice = Bids.index(side_block_data[index])
                block_buffer[index].add_to_sideblock(block_buffer[indice])

        if block_buffer[index].template["block name"] == "def":
            lCFb.add_to_buffer(block_buffer[index].template,block_buffer[index].block_setting[0])
        # add var to global
        # check and create global

        if var_data[index] and var_data[index] != ['']:
            index2 = gc.class_buffer.index(block_buffer[index].class_id)
            for item in var_data[index]:
                data = gc.globals_class_manager.class_buffer[index2][0].var_area.create_var(item)
                gc.globals_class_manager.class_buffer[index2][0].add_var(data)
    for item in global_var:
        gc.global_variable_buffer.append(item)
        # main UI create var with item
        # delete all variable UI create new one

    return block_buffer
    pass

def main(page:ft.Page):
    page.window_maximized=False
    stack = st.stack_buffer()

    data =  load_to_block("../myfile.txt")
    for n,item in enumerate(data):
        data[n].code_container = stack
    stack.controls = data
    page.add(stack)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)

