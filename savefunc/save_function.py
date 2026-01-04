import flet as ft
import blocklogic as b
from random_req import *
import pickle
from savefunc import scan as sc
import global_control as gc
dirs = "./default_block/"
if_dir = dirs+"container/if.json"
def Nget_block(display:ft.Stack):
    return len(display.controls)


def extract_data(obj):
    Bid = generate_random_string(10)
    return ((obj.IsContainer,obj.HaveParameter,obj.IsHeader,obj.Executable,obj.id,
    obj.left,
    obj.top,
    obj.block_height,
    obj.block_width,
    obj.name,
    obj.Npara,
    obj.template,
    obj.args,
    obj.clone_para,
    obj.clone_restrict,
    obj.in_display,
    obj.class_id
    )
            ,Bid)

def get_class_variable(target):
    index = gc.class_buffer.index(target.class_id)
    class_dis = gc.globals_class_manager.class_buffer[index]
    var_buffer = []
    for variable in class_dis[0].child_display_var.controls:
        var_buffer.append(variable.controls[1].controls[0].name)
    #print("daddd",var_buffer)
    return var_buffer
    #print(gc.globals_class_manager)

def get_relation_data(regular_data,obj_list):
    below_data = []
    upper_data = []
    side_block_data = []
    hook_data = []
    contain_data = []
    para_data =[]
    class_ids = []
    for item in obj_list:
        class_ids.append(item.class_id)
        obj_below_data = []
        for data in item.below_code:
            index = obj_list.index(data)
            obj_below_data.append(regular_data[index][1])
        below_data.append(obj_below_data)

        obj_contain_data = []
        for data in item.contain:
            index = obj_list.index(data)
            obj_contain_data.append(regular_data[index][1])
        contain_data.append(obj_contain_data)

        obj_para_data = []
        for n,data in enumerate(item.parameter_buffer):
            if data:
                index = obj_list.index(data)
                obj_para_data.append(regular_data[index][1])
            elif item.arg_buffer[n].content.value != "" and not data:
                obj_para_data.append("----------"+item.arg_buffer[n].content.value )
            else:
                obj_para_data.append(None)
        para_data.append(obj_para_data)

        if item.upper_code:
            upper_data.append(regular_data[obj_list.index(item.upper_code)][1])
        else:
            upper_data.append(None)

        if item.side_block:
            side_block_data.append(regular_data[obj_list.index(item.side_block)][1])
        else:
            side_block_data.append(None)

        if item.hook:
            hook_data.append(regular_data[obj_list.index(item.hook)][1])
        else:
            hook_data.append(None)


    return upper_data,below_data,side_block_data,hook_data,contain_data,para_data,class_ids

def write(obj,filename):
    sc.scan(obj)

    class_regular_data = []
    variable_data = []
    for index,data in enumerate(obj):
        extracted_data = extract_data(data)
        class_regular_data.append(extracted_data)
        if data.class_id !=None:
            variable_data.append((get_class_variable(data),index))


    # relation data
    upper_data,below_data,side_block_data,hook_data,contain_data,para_data,class_ids = get_relation_data(class_regular_data,obj)
    print(class_ids)
    #save

    with open(filename,"w+") as f:
        f.write(str(len(class_regular_data))+"\n")

        for n,item in enumerate(class_regular_data):

            data,Bid = item
            pickle_data = pickle.dumps(data)
            f.write(str(pickle_data)+"\n")
            f.write(Bid+"\n")
            if upper_data[n]:
                f.write(str(upper_data[n]))
            else:
                f.write('')
            f.write("\n")

            for ids in below_data[n]:
                f.write(ids+" ")
            f.write("\n")

            if side_block_data[n]:
                f.write(str(side_block_data[n]))
            else:
                f.write('')
            f.write("\n")

            if hook_data[n]:
                f.write(str(hook_data[n]))
            else:
                f.write('')
            f.write("\n")

            for ids in contain_data[n]:
                f.write(ids+" ")
            f.write("\n")

            for ids in para_data[n]:
                f.write(str(ids)+" ")
            f.write("\n")

            if class_ids[n]:
                f.write(str(class_ids[n]))
            else:
                f.write('')
            f.write("\n")
            #class variable if block is class
            print(variable_data)
            for data,ind in variable_data:
                if ind == n:
                    for name in data:
                        f.write(str(name)+" ")

            f.write("\n")

        #write global var
        for item in gc.global_variable_buffer:
            f.write(str(item)+" ")
        f.write("\n")

