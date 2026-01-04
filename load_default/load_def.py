from load_default.create_dir import *
import setting
import flet as ft
from UIs import block_display as bd
import blocklogic as b
import json_process.json_reader as jsrd
block_dir_list = create_dir(folder_dirs[setting.define_i],define)


def load(block_dir_list,display,top_layer,page):
    for dirs in block_dir_list:
        data = b.block(x=0, y=0,
                       have_parameter=True, Npara=1, struct=jsrd.read_json(dirs),clone_para=True)
        slot = bd.display_slot(wid=250,hei=data.block_height+10,page=page,top_layer=top_layer)

        slot.change_block(data)
        display.add_block(slot)
        display.set_display_block(display.block_buffer)

class stackd(ft.Stack):
    def __init__(self,page=None):
        super().__init__()
        self.page = page
    def interact(self, data,e,mode=1):
        if mode==2:
            self.controls.remove(e.control)
            self.update()
        pass
simmainpage = stackd()
def main(page:ft.Page):
    page.window_maximized=False
    page.overlay.append(simmainpage)
    display = bd.Display_container(wid=250,hei=page.height,page=page)
    load(block_dir_list,display,simmainpage,page)
    page.add(display)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)



