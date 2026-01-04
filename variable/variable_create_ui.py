

import flet as ft
from utility.color_palette import *
import blocklogic as b
from json_process import json_reader as jsrd
import copy as c
import sys
import global_control as gc
dir2 = "./default_block/"
var_dir = dir2+"variable/variable.json"






class var_slot(ft.Stack):
    def __init__(self,wid,hei,page,parent):
        super().__init__()
        self.height = hei
        self.width = wid
        self.page = page
        self.parent = parent
    def add(self,data):
        self.width = data.block_width
        self.height = data.block_height
        data.top = (self.height-data.block_height)/2
        data.left =(self.width-data.block_width)/2

        self.controls.append(data)

    def interact(self,data,e,mode = 1):
        if mode ==1:
            new_block = c.deepcopy(data)
            data.hook_to_mouse = True
            data.top = e.global_y-e.local_y
            data.left = e.global_x-e.local_x
            new_block.code_container = self
            data.hook_to_mouse = True
            self.controls[0] = new_block
            data.code_container = self.parent
            c2 = data.hidecontent()
            data.content_hide = c2
            self.parent.controls.append(data)


        # Wait for the listener thread to finish

        self.page.update()



class variable_container(ft.Container):
    def __init__(self,wid,hei,page,parent):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.parent = parent
        self.primary = white
        self.secondary =white_2
        self.outline = white_3
        self.bgcolor = self.primary
        self.choice_list = []
        self.padding = ft.padding.only(top=10)
        self.input_section = ft.TextField(width=self.width,height=40,border_color=self.outline,label="variable name")
        self.accept_btn = ft.OutlinedButton(width=self.width,height=40,text="Create",on_click=self.create_new_var)
        self.variable_display = ft.ListView(expand=True,width=self.width,height=self.height,spacing=15,controls=[],on_scroll_interval=1,auto_scroll=True
                                       ,padding=ft.padding.only(left=0,bottom=2,right=20,top=10))

        self.display = ft.Container(height=self.height-50*4-40,width=self.width,content=self.variable_display,border_radius=ft.border_radius.all(10),border=ft.border.all(1,white_3)
                                    )

        self.dell_button = ft.ElevatedButton(text="Delete",bgcolor="RED",color="WHITE",width=self.width,height=40
                                             ,on_click=self.remove_item)
        main_layout = ft.Column([self.input_section,self.accept_btn,self.display,self.dell_button])
        self.content = main_layout
        self.datalist = []


    def create_new_var(self,e):
        if self.input_section.value:
            gc.global_variable_buffer.append(self.input_section.value)
            var = var_slot(wid=150, hei=40, page=self.page,parent = self.parent)
            data = b.block(x=0, y=0, content=None, code_container=var,
                            name=self.input_section.value, struct=jsrd.read_json(var_dir),indisplay=True)
            var.add(data)

            checkbtn = ft.Checkbox()

            vertical_layout = ft.Row([checkbtn, var])
            self.datalist.append((checkbtn, vertical_layout))
            self.variable_display.controls.append(vertical_layout)
            self.input_section.value = ""
            try:
                self.input_section.update()
                self.variable_display.update()
            except:
                pass
    def create_var(self,data_text):
        var = var_slot(wid=150, hei=40, page=self.page,parent = self.parent)
        data = b.block(x=0, y=0, content=None, code_container=var,
                       name=data_text, struct=jsrd.read_json(var_dir), indisplay=True)
        var.add(data)
        checkbtn = ft.Checkbox()
        vertical_layout = ft.Row([checkbtn, var])
        self.datalist.append((checkbtn, vertical_layout))
        self.variable_display.controls.append(vertical_layout)
        try:
            self.update()
        except:
            pass

    def wipe_all(self):
        self.datalist = []
        self.variable_display.controls = []
        try:
            self.update()
        except:
            pass

    def remove_item(self,e):
        clone = c.copy(self.datalist)
        for state,main in clone:
            if state.value:
                gc.global_variable_buffer.remove(main.controls[1].controls[0].name)
                self.variable_display.controls.remove(main)
                self.datalist.remove((state,main))
        #print(gc.global_variable_buffer)
        self.update()


def main(page:ft.Page):
    top_layer.page = page
    page.window_maximized=False
    var = variable_container(wid=200,hei=page.height,page=page,parent = top_layer )
    page.overlay.append(top_layer)
    page.add(var)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
    sys.exit()