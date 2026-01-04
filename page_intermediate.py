from function_UI import func_display as fd
import function_UI.function_ui as fu
import container.for_edit as fe
from class_func import class_UI as cUI
import flet as ft
from class_func import class_create as cc
from class_func import class_buffer as cb
from json_process import json_writer as jwt
page:ft.Page = None
restriction_area:ft.Container = None
edit_target = None
global_data = None
def set_page(page_data):
    global page,restriction_area
    page = page_data
    restriction_area = ft.Container(width=2000,height=2000,bgcolor="BLACK",opacity=0.5)

def func_sig():
    pass
def for_sig():
    pass
def load_data(data,target:fu.function_UI):
    target.load_data(data)

def get_signal_block(data,type = "func",target=None,e=None):

    global edit_target,global_data

    edit_target = target
    global_data = data

    if type == "func":
        function_ui = fu.function_UI(page.width)
        load_data(data,target=function_ui)
        open_window(function_ui)
    elif type == "for":
        for_ui = fe.function_UI(page.width)
        load_data(data,target=for_ui)
        open_window(for_ui)
    elif type == "class":
        _,_,template = global_data
        cordx = e.global_x
        cordy = e.global_y
        class_editor = cUI.class_edit(200,90,page=page,parent=edit_target,top=cordy,left=cordx)
        class_editor.open(template['style'][1][1])

        page.overlay.append(restriction_area)
        page.overlay.append(class_editor)
        pass
    page.update()
def open_window(target:ft.Container):

    target_wid = target.width if target.width else page.width
    if target.height:
        target_hei = target.height
    else:
        target_hei = page.height

    center_wid = (page.width-target_wid)/2
    center_hei = (page.height-target_hei)/2
    target.top =  center_hei
    target.left = center_wid

    page.overlay.append(restriction_area)
    page.overlay.append(target)

def close_overlay(target):
    page.overlay.remove(target)
    page.overlay.remove(restriction_area)
    page.update()
def send_signal_block(data,type="func"):
    ori_npara, ori_para_data, ori_block_struct = global_data
    #send signal to block
    if type=='func':
        code_name,func_name,para_data = data
        npara = len(para_data)
        temp,main_data = ori_block_struct['struct'][0]
        style_data = [('text', 'def'), ('text', ''), ('btn', None)]
        #print(style_data)
        main_data = "def "+code_name
        ori_block_struct['struct'][0] = (temp,main_data)
        style_data[1] = ('text',func_name)
        for i in range(npara+1):
            style_data.insert(-1,('para', None))
        ori_npara = npara
        new_para_data = []
        ori_block_struct['style'] = style_data
        for n,p_data in enumerate(para_data):
            para_name,para_dval = p_data
            arg = {'style': [('text', '')],
                   'color': '#FF6A00', 'text color': '#000000',
                   'block type': 'variable', 'block name': 'variable',
                   'block setting': [],
                   'struct': [('name', None), ('def_val', None)]
                   }
            arg['style'][0] = ('text',para_name)
            arg['struct'][1] = ('def_val', para_dval)
            new_para_data.append(arg)
        repacked_data = ori_npara,new_para_data,ori_block_struct

        edit_target.read_data(repacked_data)
    elif type=="for":
        ori_npara = len(data)+1
        new_para_data = []
        ori_block_struct['style'] = [('text', 'for'), ('text', 'in'), ('para', None), ('btn', None)]
        ori_block_struct['struct'] = [('code', 'for '), ('code', 'in '), ('arg', None), ('adsb', ':')]
        for index,item in enumerate(data):
            arg = {'style': [('text', '')],
                   'color': '#FF6A00', 'text color': '#000000',
                   'block type': 'variable', 'block name': 'variable',
                   'block setting': [],
                   'struct': [('name', None), ('def_val', None)]
                   }
            arg['style'][0] = ('text',item)
            new_para_data.append(arg)
            ori_block_struct['style'].insert(1,('para',None))
            if index==0:
                ori_block_struct['struct'].insert(1,('adsb', '  '))
            else:
                ori_block_struct['struct'].insert(1, ('adsb', ' , '))
            ori_block_struct['struct'].insert(1, ('arg', None))

        repacked_data = ori_npara,new_para_data,ori_block_struct
        edit_target.read_data(repacked_data)
    elif type == "class":
        edit_target.template = data
        print(data)
        edit_target.class_update()
        edit_target.class_name_update()
        edit_target.load_template()

        edit_target.data = edit_target.style
        edit_target.para_data = edit_target.load_para(edit_target.data)
        edit_target.posion_manage(edit_target.data,edit_target.para_data)
        edit_target.reset_para_size()
        struct = cc.create_class(edit_target.template,edit_target.block_setting[0])
        jwt.write_function(struct,edit_target.block_setting[0])
        #print("asdsd",struct)
        cb.add_to_buffer(struct,edit_target.block_setting[0])
        # try:
        #     edit_target.content_update()
        # except:
        #     pass
        # pass
    pass
