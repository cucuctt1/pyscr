import flet as ft
from utility.color_palette import *
from utility.color_process import *
from utility.valid_name import *
import blocklogic as b
import copy as c
import stack as st
import setting as s
import json_process.json_reader as jsrd


dirs = "./default_block/"
class_var_dir = dirs + "class/class_var.json"
add_dir = dirs + "normal_block/add.json"
self_dir = dirs + "/class/self.json"


def convert_function(template):
    modded_template_style = template["style"]
    text = modded_template_style[0][1]
    modded_template_style[0] = ('text',"."+text)
    modded_template_struct = template["struct"]
    modded_template_struct.insert(0, ("adsb", "."))

    template['style'] = modded_template_style
    template['struct'] = modded_template_struct

    return template


class display_slot(ft.Stack):
    def __init__(self, wid, hei, page, top_layer):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.top_layer = top_layer
        self.controls = [None]

    def change_block(self, block):
        block.in_display = True
        block.code_container = self
        block.top = (self.height - block.block_height) / 2
        block.left = (self.width - block.block_width) / 2
        self.controls[0] = block

    def interact(self, data, e, mode=1):
        # mode 1 block interact
        # mode 2 block destroy
        if mode == 1:
            # create new block
            new_block = c.deepcopy(data)
            self.change_block(new_block)
            data.hook_to_mouse = True
            # calculate position

            data.top = e.global_y - e.local_y
            data.left = e.global_x - e.local_x

            data.code_container = self.top_layer
            data.hidecontent()
            self.top_layer.controls.append(data)

        self.page.update()


class variable_create(ft.Container):
    def __init__(self, wid, hei, parent, page, top_layer, bgcolor=white):
        super().__init__()
        self.width = wid
        self.height = hei
        self.parent = parent
        self.bgcolor = ""
        self.page = page
        self.top_layer = top_layer
        self.text_field = ft.TextField(width=self.width * 0.60, bgcolor=bgcolor, height=self.height,
                                       content_padding=ft.padding.all(5), hint_text="variable create")
        self.accept_btn = ft.ElevatedButton(text="accept", on_click=self.click, width=self.width * 0.35)

        self.content = ft.Row([self.text_field, self.accept_btn], spacing=5)
        self.padding = ft.padding.only(left=5)

    def create_var(self,data):
        var_struct = jsrd.read_json(class_var_dir)
        var_struct['style'][0] = ('text', "." + data)
        block = b.block(x=0, y=0, struct=var_struct, name=data)
        block.name = data
        slot = display_slot(wid=self.parent.width - 30, hei=block.block_height + 10, page=self.page,
                            top_layer=self.top_layer)
        slot.change_block(block)
        self.del_btn = ft.IconButton(icon_size=20, icon=ft.icons.DELETE, bgcolor="", icon_color="BLACK", width=50,
                                     on_click=self.del_click)
        self.row = ft.Row([self.del_btn, slot], spacing=0, width=self.width)
        return self.row
    def click(self, e):
        if self.text_field.value:
            var_name = filter(self.text_field.value)
            self.create_var(var_name)
            self.text_field.value = ""
            self.parent.add_var(self.row)
            try:
                self.parent.update()
                self.update()
            except:
                pass

    def del_click(self, e):
        for data in self.parent.child_display_var.controls:
            if e.control == data.controls[0]:
                self.parent.remove_var(data)
                break


class class_search(ft.TextField):
    def __init__(self, wid, hei, data, parent):
        super().__init__()
        self.width = wid
        self.height = hei
        self.on_change = self.change
        self.data = data  # class_buffer
        self.parent = parent
        self.bgcolor = "WHITE"
        self.border = ft.border.all(1,white_3)
        self.hint_text = "Search here"
        self.content_padding = ft.padding.only(left=5,top = 1,right=1)

    def change(self, e):
        data = self.query2(self.value)
        index_list = []
        # print(data)
        var_func_check = False
        for item in data:
            class_data, index, var, func = item

            if var_func_check == False and (not var and not func) and class_data:
                var_func_check = True
            if class_data:
                self.parent.main_contain.controls[index].show_content(var, func)
                index_list.append(index)
        if not var_func_check:
            self.parent.show_content(index_list)
        else:
            for item in index_list:
                var = list(range(len(self.parent.main_contain.controls[item].child_display_var.controls)))
                func = list(range(len(self.parent.main_contain.controls[item].child_display_func.controls)))
                self.parent.main_contain.controls[item].show_content(var, func)
            self.parent.show_content(index_list)

        self.parent.update()
        pass

    def find_code(self, struct):
        for item in struct:
            type, data = item
            if type == "code":
                return data
        return ""

    def query2(self, kw):
        # print(self.data)
        query_res = []
        for index, class_data in enumerate(self.data):
            var_list = class_data[0].child_display_var.controls
            func_list = class_data[0].child_display_func.controls

            # class search
            class_res = None
            if kw in class_data[0].class_name:
                class_res = class_data
            # var search
            var_res = []
            for n, row in enumerate(var_list):
                var = row
                if kw in var.controls[1].controls[0].name:
                    var_res.append(n)
                    if not class_res:
                        class_res = class_data

            # func search
            func_res = []
            for n, func in enumerate(func_list):
                res1 = self.find_code(func.controls[0].template['struct'])
                res2 = func.controls[0].block_name

                if kw in res1 or kw in res2:
                    func_res.append(n)
                    if not class_res:
                        class_res = class_data

            packed_data = (class_res, index, var_res, func_res)
            # print(packed_data)
            query_res.append(packed_data)
        return query_res


class class_data_contain(ft.ExpansionPanel):
    def __init__(self, wid, hei, page, top_layer, bgcolor=white):
        super().__init__()
        self.height = hei
        self.width = wid
        self.bgcolor = bgcolor
        self.page = page
        self.top_layer = top_layer
        self.class_name = ""
        self.child_display_func = ft.ListView()
        self.child_display_var = ft.ListView()

        # default view
        self.child_display = ft.ListView([self.child_display_var, self.child_display_func])
        self.show_content(list(range(len(self.child_display_var.controls))),
                          list(range(len(self.child_display_func.controls)))
                          )
        self.var_area = variable_create(self.width, 40, self, self.page, self.top_layer)
        self.column = ft.Column([self.var_area, self.child_display])
        self.content = self.column

    def create_class_data(self, name):
        self.class_name = name
        self.text_color = generate_contrasting_color(self.bgcolor, brightness_threshold=100)
        self.header = ft.ListTile(title=ft.Text(self.class_name, color=self.text_color))

    def add_content(self, content):
        self.child_display_func.controls.append(content)
        self.show_content(list(range(len(self.child_display_var.controls))),
                          list(range(len(self.child_display_func.controls)))
                          )
        self.update_content()

    def add_var(self, content):
        self.child_display_var.controls.append(content)
        self.show_content(list(range(len(self.child_display_var.controls))),
                          list(range(len(self.child_display_func.controls)))
                          )
        self.update_content()

    def remove_var(self, content):
        self.child_display_var.controls.remove(content)
        self.show_content(list(range(len(self.child_display_var.controls))),
                          list(range(len(self.child_display_func.controls)))
                          )
        self.update_content()

    def show_content(self, var, func):

        for n, _ in enumerate(self.child_display_func.controls):
            self.child_display_func.controls[n].visible = False
        for item in func:
            self.child_display_func.controls[item].visible = True

        for n, _ in enumerate(self.child_display_var.controls):
            self.child_display_var.controls[n].visible = False
        for item in var:
            self.child_display_var.controls[item].visible = True
        # self.child_display.controls = [var_dis,func_dis]

        self.update_content()
        pass

    def update_content(self):
        try:
            self.child_display.update()
            self.content.update()
        except:
            pass


class class_display(ft.Container):
    def __init__(self, wid, hei, page, display_layer,bgcolor = None):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.top_layer = display_layer
        self.bgcolor = bgcolor
        self.class_buffer = []

        self.main_contain = ft.ExpansionPanelList(expanded_header_padding=ft.padding.symmetric(vertical=5.0))
        self.display_content = self.main_contain
        self.scroll = ft.ListView(height=self.height, controls=[self.display_content], on_scroll_interval=1)
        self.misc2 = ft.Container()
        self.search_bar = class_search(self.width, hei=40, data=self.class_buffer, parent=self)
        self.misc = ft.Container(content=self.search_bar)
        self.layout = ft.Column([self.misc, self.scroll, self.misc2], spacing=5)
        self.content = self.layout

        self.padding = ft.padding.only(top=5, left=5, right=5)

    def add_function(self, content, class_index=None):
        content.template = convert_function(content.template)
        content.load_template()
        content.load_block()
        content.reset_para_size()
        data = display_slot(wid=self.width, hei=content.block_height + 20, page=self.page, top_layer=self.top_layer)
        data.change_block(content)
        if class_index != None:
            self.class_buffer[class_index][0].add_content(data)  # what is this mean
            self.show_content(list(range(len(self.class_buffer))))
        pass

    def add_class(self, name, bgcolor, id):
        class_data_container = class_data_contain(self.width, hei=30, bgcolor=bgcolor, page=self.page,
                                                  top_layer=self.top_layer)
        class_data_container.create_class_data(name=name)
        self_func = b.block(x=0, y=0, code_container=None,
                            have_parameter=True, struct=jsrd.read_json(self_dir))
        data = display_slot(wid=self.width, hei=self_func.block_height + 20, page=self.page, top_layer=self.top_layer)
        data.change_block(self_func)
        class_data_container.add_content(data)
        self.class_buffer.append((class_data_container, id))
        index = len(self.class_buffer)-1
        self.show_content(list(range(len(self.class_buffer))))
        return index

    def update_content(self):
        try:
            self.content.update()
        except:
            pass

    def show_content(self, class_index):
        for n, _ in enumerate(self.class_buffer):
            self.class_buffer[n][0].visible = False
        for index in class_index:
            self.class_buffer[index][0].visible = True

        self.main_contain.controls = []
        for data, _ in self.class_buffer:
            self.main_contain.controls.append(data)
        self.update_content()

    def update_function(self,class_index,struct,func_index):
        struct.template = convert_function(struct.template)
        self.class_buffer[class_index][0].child_display_func.controls[func_index+1].change_block(struct)
        try:
            self.class_buffer[class_index][0].child_display_func.controls[func_index + 1].update()
        except:
            pass
        self.update_content()

    def remove_function(self,class_index,func_index):
        self.class_buffer[class_index][0].child_display_func.controls = self.class_buffer[class_index][0].child_display_func.controls[:func_index+1]
        self.update_content()

    def remove_class(self,class_index):
        self.class_buffer.remove(self.class_buffer[class_index])
        self.show_content(list(range(len(self.class_buffer))))
        self.update_content()

def main(page: ft.Page):
    page.window_maximized = False
    stack = st.stack_buffer()
    class_dis = class_display(wid=300, hei=page.height, page=page, display_layer=stack)
    class_dis.bgcolor = "GREEN"
    class_dis.add_class("test", bgcolor=debug_red, id=1)
    te = b.block(x=0, y=0, code_container=None, id="level 2 block",
                 have_parameter=True, Npara=2, struct=jsrd.read_json(add_dir))
    class_dis.add_function(content=te, class_index=0)

    class_dis.add_class("test2", bgcolor=debug_red, id=2)
    te = b.block(x=0, y=0, code_container=None, id="level 2 block",
                 have_parameter=True, Npara=2, struct=jsrd.read_json(add_dir))
    class_dis.add_function(content=te, class_index=1)
    class_dis.add_class("test3", bgcolor=debug_red, id=2)
    class_dis.add_class("test4", bgcolor=debug_red, id=2)
    class_dis.add_class("test5", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    class_dis.add_class("test", bgcolor=debug_red, id=2)
    page.overlay.append(stack)
    page.add(class_dis)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
