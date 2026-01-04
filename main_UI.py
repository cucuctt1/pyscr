from UIs.vertical_tab import vertical_tab as vt
from UIs import block_display as bd
from load_default import load_normal as ln , load_def as ld,load_class as lc,load_misc as lm,load_python as lp,load_condition as lco,load_container as lcon
from json_process import *
from class_func import class_display as cd
from utility.color_palette import *
from savefunc import read_function as rf
import flet as ft
import blocklogic as b
import start_parse as sp
import page_intermediate as pi
import global_control as gc
from json_process import json_reader as jsrd
from variable import variable_create_ui as vcui
import os
from utility.auto_para import *
from function_UI import func_display as fd
from savefunc import save_ui as saui
from savefunc import open_ui as opui
from savefunc import export_py as expy
from window_mana import get_windows_max_window_size as gt
class free_move(ft.GestureDetector):
    def __init__(self,main_target):
        super().__init__()
        self.on_pan_update =self.move
        self.main = main_target

    def move(self,e:ft.DragUpdateEvent):
        if not e.global_y < 40 and not e.global_x < 300:
            for item in self.main.controls:
                if not item.upper_code and not item.hook:
                    item.move(e.delta_x,e.delta_y)
            self.main.update()

# global_func = None
# global_page = None
def update_func():
    pass
window_wid,window_hei = gt()
window_hei-=70
def main(page=gc.global_page):

    print(window_hei,window_wid)
    gc.global_page = page

    page.window_maximized = True
    page.padding = ft.padding.all(0)

    stack = gc.global_playground
    stack.height = 1200
    pi.set_page(page)

    #stack.height = page.height*0.65

    #recalculate cord
    def run(e):
        code = sp.get_code(stack)
        with open("temp.py","w") as f:
            f.write(code)

        os.system("start cmd /K python temp.py")


    sub_layout1 = ft.Container(width=300, bgcolor="RED", height=window_hei)
    block_display1 = bd.Display_container(wid=300 - 40, page=page, hei=window_hei)
    block_display1.height = window_hei
    ln.load(ln.block_dir_list, block_display1, stack, page)
    block_display1.set_display_block(block_display1.block_buffer)

    block_display2 = bd.Display_container(wid=300 - 40, page=page, hei=window_hei)
    lcon.load(lcon.block_dir_list, block_display2, stack, page)
    block_display2.set_display_block(block_display2.block_buffer)

    #block_display3 = bd.Display_container(wid=300 - 40, page=page, hei=window_hei)
    #fd.load_func_buffer(gc.local_CF_buffer,block_display3,page = page,top_layer=stack)
    #block_display3.set_display_block(block_display3.block_buffer)

    block_display3 = gc.global_func_display
    block_display3.page = page
    block_display3.height = window_hei
    block_display3.main_content.page = page
    block_display3.content.page = page

    block_display4 = gc.global_class_display
    block_display4.page = page
    block_display4.height = window_hei
    block_display4.main_content.page = page
    block_display4.content.page = page

    block_display5 = bd.Display_container(wid=300 - 40, page=page, hei=window_hei)
    lco.load(lco.block_dir_list, block_display5, stack, page)
    block_display5.set_display_block(block_display5.block_buffer)

    block_display6 = cd.class_display(wid=300 - 40, page=page, hei=window_hei, display_layer=stack,
                                      bgcolor=white)
    block_display6.border = ft.border.all(1, white_3)
    block_display6.border_radius = ft.border_radius.all(5)
    gc.globals_class_manager = block_display6

    block_display7 = vcui.variable_container(wid=300-40,page=page,parent=stack,hei=window_hei)
    def update_variable():
        block_display7.wipe_all()
        for var in gc.global_variable_buffer:
            block_display7.create_var(var)

        page.update()

    def opene(e):
        opui.open_winexp(page,block_display7)
        update_variable()

    #icons.PIX variable create
    #icons.EXTENSION
    #icons.ALL_INBOX
    tabs = [vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.WIDTH_NORMAL_OUTLINED)), content=block_display1),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.DATASET)), content=block_display2),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.PALLET)), content=block_display3),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_OUTLINED)), content=block_display4),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CONFIRMATION_NUM_OUTLINED)), content=block_display5),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_)), content=block_display6),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.PIX )), content=block_display7)]
    vertical_drawer = vt.vertical_tab(tab_color=white_3, select_color=accept_col, render_color=white_2,
                                      wid=300, tab_wid=40, select_index=1,
                                      tabs=tabs)
    sub_layout1.content = vertical_drawer
    sub_layout2 = ft.Column([])
    bot_layout = ft.Row([sub_layout1, sub_layout2])

    def save(e):
        saui.open_winexp(page)
    def export(e):
        expy.open_winexp(page)

    save_btn = ft.ElevatedButton(text="save", width=110,on_click=save,icon=ft.icons.SAVE_OUTLINED)
    open_btn = ft.ElevatedButton(text="open", width=110,on_click=opene,icon=ft.icons.FILE_OPEN_OUTLINED)
    export_btn = ft.ElevatedButton(text="export", width=120,on_click=export,icon=ft.icons.DRIVE_FILE_MOVE_OUTLINE)



    run_btn = ft.ElevatedButton(text="run", width=110,on_click=run,col={'xs':1},icon=ft.icons.PLAY_ARROW,icon_color="GREEN",
                                color="GREEN",bgcolor="WHITE")  # icon

    left = ft.Row([save_btn, open_btn, export_btn],col={'lg':4})
    main_top_layout = ft.ResponsiveRow([left, run_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    top_layout = ft.Container(height=40, bgcolor=tab_white, content=main_top_layout,
                              padding=ft.padding.only(left=20, right=20,top=2),
                              border=ft.border.all(1, white_3))

    main_layout = ft.Column([top_layout, bot_layout], spacing=0)

    def layout_manage(e):
        stack.interact(None,None,2)
        sub_layout1.height = e.control.window_height
        block_display1.height = e.control.window_height
        block_display2.height = e.control.window_height
        block_display3.height = e.control.window_height
        block_display4.height = e.control.window_height
        block_display5.height = e.control.window_height
        block_display6.height = e.control.window_height
        vertical_drawer.height = e.control.window_height
        block_display7.height = e.control.window_height
        main_layout.update()
        bot_layout.update()
        vertical_drawer.update()
        e.control.update()
        page.update()
    header = b.block(x=500,y=300,isheader=True,struct=jsrd.read_json("./header.json"),code_container=stack)
    stack.add_block(header)
    #page.on_window_event = layout_manage
    #page.on_resize = layout_manage
    free = free_move(stack)

    page.add(main_layout)
    page.overlay.append(free)
    page.overlay.append(stack)

    page.update()

def add_to_def(id):
    global global_func, global_page

    CF_dir = "./CF_store/"
    filename = id+".json"
    file_dir = CF_dir+filename
    slot = bd.display_slot(wid=250,hei=40,page=global_page,top_layer=gc.global_playground)
    struct = jsrd.read_json(file_dir)
    block = b.block(x=0,y=0,struct=struct,Npara=auto_para(struct),have_parameter=True)
    slot.change_block(block)
    global_func.add_block(slot)
    global_func.set_display_block(global_func.block_buffer)
    global_page.update()
if __name__ == "__main__":
    ft.app(target=main)