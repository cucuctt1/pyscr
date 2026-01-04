from load_default.create_dir import *
import setting
import flet as ft
from utility.color_palette import *
import copy as c
import blocklogic as b
from utility.auto_para import *
import json_process.json_reader as jsrd
# from utility import auto_para as ap
# def load_func_buffer(buffer,display,top_layer,page):
#     for data in buffer:
#         if data[0]['block name'] == "class":
#             #load block with args one
#             struct = data[0]
#             block = b.block(x=0, y=0, have_parameter=True, Npara=1, struct=struct,args=True)
#         else:
#             struct = data[0]
#             npara = (ap.auto_para(struct)-1)
#             block = b.block(x=0,y=0,have_parameter=True,Npara=npara,struct=struct)
#         slot = bd.display_slot(wid=250,hei=40,page=page,top_layer=top_layer)
#         slot.change_block(block)
#         display.add_block(slot)
#
#     display.set_display_block(display.block_buffer)
#
# def load_from_file(file_buffer,display,top_player,page):
#     for file in file_buffer:
#         print(file)
class display_slot(ft.Stack):
    def __init__(self,wid,hei,page,top_layer):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.top_layer = top_layer
        self.controls = [None]

    def change_block(self,block):
        block.in_display = True
        block.code_container = self
        block.top = (self.height-block.block_height)/2
        block.left = (self.width-block.block_width)/2
        self.controls[0] = block

    def interact(self,data,e,mode=1):
        #mode 1 block interact
        #mode 2 block destroy
        #print(mode)
        if mode == 1:
            #create new block
            new_block = c.deepcopy(data)
            self.change_block(new_block)
            #data.hook_to_mouse = True
            #calculate position
            #print("hover",data)
            data.top = e.global_y-e.local_y
            data.left = e.global_x-e.local_x

            data.code_container = self.top_layer
            data.hidecontent()
            self.top_layer.controls.append(data)
        #print(self.top_layer.controls)
        self.page.update()


class Search_bar(ft.Container):
    def __init__(self,wid=300,hei = None,page = None,parent = None):
        super().__init__()
        self.height = hei
        self.width = wid
        self.page = page

        self.primary = white
        self.secondary = white_2
        self.outline = white_3
        self.padding = ft.padding.only(top=5,left=5,right=5)
        self.parent = parent
        self.seacrh_bar = ft.TextField(width=self.width,height=self.height,border_color=self.outline,
                                       border_radius=4,on_change=self.change,label="Block name/Block code",
                                       dense=True)
        self.content = self.seacrh_bar

    def change(self,e):
        data = self.query(e.control.value)
        self.parent.set_display_block(data)
        self.parent.update()
        pass

    def find_code(self,struct):
        for item in struct:
            type,data = item
            if type=="code":
                return data
        return ""

    def query(self,keyword):
        result_list = []
        for item in self.parent.block_buffer:
            res1 = self.find_code(item.controls[0].template['struct'])
            res2 = item.controls[0].block_name

            if keyword in res1 or keyword in res2:
                result_list.append(item)

        return result_list

class Display_container(ft.Container):
    def __init__(self,wid=300,hei = None,page = None,misc_hei = 40):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.primary = white
        self.secondary = white_2
        self.outline = white_3
        self.border = ft.border.all(1,self.outline)
        self.border_radius = ft.border_radius.all(5)
        self.bgcolor = self.primary

        self.misc_height = misc_hei
        self.search_bar = Search_bar(wid=self.width,hei=40,page=self.page,parent=self)
        self.misc = ft.Column([],width=self.width,height=self.misc_height)
        self.misc.controls.append(self.search_bar)

        self.block_buffer = []
        self.display_content = []
        self.block_display = ft.ListView(width=self.width,height=1200)


        self.main_layout = ft.Column([self.misc,self.block_display],width=self.width,height=self.height
                                     ,alignment=ft.MainAxisAlignment.CENTER)

        self.content = self.main_layout

    def add_block(self,slot:display_slot):
        self.block_buffer.append(slot)
        pass

    def remove_block(self,slot:display_slot):
        self.block_buffer.remove(slot)

    def display_block_manager(self):
        pass

    def set_display_block(self,block_list):
        self.display_content = block_list
        self.block_display.controls = self.display_content
class func_display(ft.Container):
    def __init__(self,wid,hei,page,parent,buffer):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.parent = parent
        self.gl_buffer = buffer
        self.bgcolor = "#FFFFFF"
        self.main_content = Display_container(wid=self.width,hei=self.height,page=self.page)
        self.main_content.set_display_block(self.main_content.block_buffer)
        self.buffer = []
        self.data_buffer = []
        self.content = self.main_content


    def update_content(self,buffer):
        #buffer infrom of style struct

        for data2,id in buffer:
            data = jsrd.read_json("./CF_store/"+id+".json")

            if id not in self.buffer:
                self.buffer.append(id)
                self.data_buffer.append(data)
                npara = auto_para(data)
                data = b.block(x=0,y=0,struct=data,have_parameter=True,Npara=npara)
                slot = display_slot(wid=250,hei=data.block_height+20,page=self.page,top_layer=self.parent)
                slot.change_block(data)
                self.main_content.add_block(slot)
                try:
                    self.main_content.update()
                except:
                    pass
            elif id in self.buffer and data != self.data_buffer[self.buffer.index(id)]:

                self.data_buffer[self.buffer.index(id)] = data
                npara = auto_para(data)
                bd = b.block(x=0,y=0,struct=data,have_parameter=True,Npara=npara)
                self.main_content.block_buffer[self.buffer.index(id)].change_block(bd)

    def remove(self,target):
        index = self.buffer.index(target)
        self.main_content.block_buffer.pop(index)
        self.buffer.pop(index)
        self.data_buffer.pop(index)
        try:
            self.main_content.update()
        except:
            pass
        #print("ddddddfdfsdf",out_side)

class class_display(ft.Container):
    def __init__(self,wid,hei,page,parent,buffer):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.parent = parent
        self.gl_buffer = buffer
        self.bgcolor = "#FFFFFF"
        self.main_content = Display_container(wid=self.width,hei=self.height,page=self.page)
        self.main_content.set_display_block(self.main_content.block_buffer)
        self.buffer = []
        self.data_buffer = []
        self.content = self.main_content

    def update_content(self,buffer):
        #buffer infrom of style struct

        for data2,id in buffer:
            data = jsrd.read_json("./CF_store/"+id+".json")

            if id not in self.buffer:

                self.buffer.append(id)
                self.data_buffer.append(data)
                npara = auto_para(data)
                data = b.block(x=0,y=0,struct=data,have_parameter=True,Npara=npara,args=True)
                slot = display_slot(wid=250,hei=data.block_height+20,page=self.page,top_layer=self.parent)
                slot.change_block(data)
                self.main_content.add_block(slot)
                try:
                    self.main_content.update()
                except:
                    pass
            elif id in self.buffer and data != self.data_buffer[self.buffer.index(id)]:

                self.data_buffer[self.buffer.index(id)] = data
                npara = auto_para(data)
                bd = b.block(x=0,y=0,struct=data,have_parameter=True,Npara=npara,args=True)
                self.main_content.block_buffer[self.buffer.index(id)].change_block(bd)
    def remove(self,target):
        index = self.buffer.index(target)
        self.main_content.block_buffer.pop(index)
        self.buffer.pop(index)
        self.data_buffer.pop(index)
        try:
            self.main_content.update()
        except:
            pass

