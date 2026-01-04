import flet as ft
from utility.color_palette import *
import blocklogic as b
import copy as c
import json_process.json_reader as jsrd

dir = "../default_block/"
add_dir = dir+"normal_block/add.json"
class stackd(ft.Stack):
    def __init__(self,page=None):
        super().__init__()
        self.page = page

    def interact(self, data,e,mode=1):

        if mode==2:
            for item in self.controls:
                pass
            #self.controls.remove(e.control)
            #self.update()


simmainpage = stackd()

class display_slot(ft.Stack):
    def __init__(self,wid,hei,page,top_layer):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.top_layer = top_layer
        self.controls = [None]

    def change_block(self,block:b.block):
        block.in_display = True
        block.code_container = self
        block.top = (self.height-block.block_height)/2
        block.left = (self.width-block.block_width)/2
        self.controls[0] = block

    def interact(self,data:b.block,e,mode=1):
        if mode == 1:
            #create new block
            new_block = c.deepcopy(data)
            self.change_block(new_block)
            data.top = e.global_y-e.local_y
            data.left = e.global_x-e.local_x

            data.code_container = self.top_layer
            #data.content = ft.Container(width=150,height=30,bgcolor="BLACK")
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

        self.block_display = ft.ListView(width=self.width,height=self.height-40*2,on_scroll=self.on_sc)

        self.main_layout = ft.Column([self.misc,self.block_display],width=self.width,height=self.height
                                     ,alignment=ft.MainAxisAlignment.START)
        self.alignment = ft.alignment.top_center
        self.content = self.main_layout

    def on_sc(self,e):
        if self.block_display.controls:
            self.block_display.controls[0].top_layer.interact(None,e,mode=2)
        self.page.update()

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



def main(page:ft.Page):
    simmainpage.page = page
    page.window_maximized=False
    page.overlay.append(simmainpage)
    slot = display_slot(wid=250,hei=40,page=page,top_layer=simmainpage)
    data = b.block(x=0, y=0, color=ft.colors.TEAL, content=None, code_container=None, id="level 2 block",
                   have_parameter=True, Npara=2, struct=jsrd.read_json(add_dir))
    slot.change_block(data)
    dis = Display_container(wid=250,hei=page.height,page=page)
    dis.add_block(slot)
    dis.set_display_block(dis.block_buffer)
    page.add(dis)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)