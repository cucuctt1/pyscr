import flet as ft
from utility import string_process as sp
from utility import preview_block as pb
import page_intermediate as pi

class argument_custom(ft.ElevatedButton):
    def __init__(self,data=(None,None),wid = 150,parent=None):
        super().__init__()
        self.data = tuple(data)
        self.width = wid
        self.text_data,self.default_value = data
        self.text = ""
        self.bgcolor = "#FF6A00"
        self.parent = parent
        self.on_click = self.onclick
        self.color = "WHITE"

    def change_data(self,data):
        self.data = data
        self.text_data,self.default_value = data
        self.text = self.text_data
        if self.text =="":
            self.destroy_self()
        try:
            self.update()
        except:
            pass
    def destroy_self(self):
        self.parent.bot_layout.controls.remove(self)
        self.parent.update_arg_buffer()
        print(self.parent.argument_buffer)
        pass
    def onclick(self,e):
        self.parent.access_data(self)

class function_UI(ft.Container):
    def __init__(self,wid):
        super().__init__()
        self.primary_color = "#FFFFFF"
        self.secondary_color = "#F4F4F4"
        self.border_color = "#D3D3D3"
        self.width = wid
        self.height = 400
        self.bgcolor = self.secondary_color
        self.navigation_bar = ft.Container(width=self.width,height=30, bgcolor=self.secondary_color,content=None,alignment=ft.alignment.center_right,padding=ft.padding.only(right=10))
        self.preview = ft.Container(height=250,bgcolor=self.primary_color
                                    ,padding=ft.padding.all(10)
                                    )
        self.setting =  self.load_setting()
        self.display = ft.Column([self.navigation_bar,self.preview,self.setting],spacing=5)
        self.content = self.display
        self.target = None
        self.argument_buffer = list()
        self.load_navigation()
        self.load_preview()
    def load_navigation(self):
        self.close_btn = ft.IconButton(icon=ft.icons.CLOSE, icon_color=ft.colors.RED,bgcolor="", width=40,
                                       height=30, icon_size=15,on_click=lambda e:self.on_closes())
        self.navigation_bar.content = self.close_btn

    def load_preview(self):
        self.preview_block = pb.function(scale=1.6,Npara=4,have_parameter=True
                                         ,preview =  True,text_color="#FFFFFF",color="#B200FF",
                                         code="def ")
        self.preview_block.bgcolor = "#B200FF"
        self.preview_canvas = ft.Stack()
        self.preview_canvas.controls.append(self.preview_block)
        self.preview.content = self.preview_canvas
    def load_setting(self):
        self.code_name_text = ft.Text(value="Code")
        self.func_name_text = ft.Text(value="Function name")
        self.code_name = ft.TextField(width=150,height=40,dense=False,content_padding=ft.padding.only(top=0,left=5,right=5),on_change=self.on_update)
        self.func_name = ft.TextField(width=150,height=40,dense=False,content_padding=ft.padding.only(top=0,left=5,right=5),on_change=self.on_update)

        self.func_name_layout = ft.Row([self.code_name_text,self.code_name,self.func_name_text,self.func_name],spacing=10)

        #seperator
        self.seperate_content = ft.Container()
        # argument setting
        self.argsetting_layout = ft.Row(spacing=10)
        self.arg_name_text = ft.Text(value="Argument name")
        self.arg_name = ft.TextField(width=150,height=40,dense=False,content_padding=ft.padding.only(top=0,left=5,right=5),on_change=self.on_update)
        self.default_value_text = ft.Text(value="Default value")
        self.default_value = ft.TextField(width=150,height=40,dense=False,content_padding=ft.padding.only(top=0,left=5,right=5))

        self.save_btn = ft.ElevatedButton(text="Save change",width=180,height=40,on_click=self.save_change)
        self.button_container = ft.Container(content=self.save_btn,alignment=ft.alignment.center)

        self.argsetting_layout.controls = [self.arg_name_text,self.arg_name,
                                           self.default_value_text,self.default_value,self.button_container]
        self.seperate_content = self.argsetting_layout

        self.top_layout = ft.Row([self.func_name_layout,self.seperate_content],spacing=10,alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        self.bot_layout = ft.Row([ft.ElevatedButton(icon=ft.icons.ADD_ROUNDED,text="ADD",width=150,on_click=self.add_argument,height=32
                                                    ,bgcolor="#FF6A00",icon_color="WHITE",color="WHITE")]
                                      ,height=50,spacing=20
                                      ,scroll=ft.ScrollMode.AUTO,vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                 )
        main_layout = ft.Column([self.top_layout,self.bot_layout],alignment=ft.MainAxisAlignment.CENTER)
        return main_layout

    def argument_manager(self):
        for item in self.bot_layout.controls:
            if isinstance(item,argument_custom):
                if item.data ==(None,None):
                    self.bot_layout.controls.remove(item)
                    self.bot_layout.update()
        self.update_arg_buffer()
    def add_argument(self,e=None,auto_access = True):
        argument = argument_custom(parent=self)
        self.argument_manager()
        self.bot_layout.controls.insert(0,argument)
        if auto_access:
            argument.parent.access_data(argument)
        self.update_arg_buffer()
        self.on_update()
        self.setting.update()

    def access_data(self,target:argument_custom):
        data = target.data
        name,default_value = data
        self.arg_name.value, self.default_value.value = (name, str(default_value)) if default_value is not None else (name, None)
        self.target = target
        self.on_update()
        self.bot_layout.update()
        self.setting.update()

    def change_data(self,target:argument_custom):
        data = (self.arg_name.value,sp.check_type(self.default_value.value))
        target.change_data(data)
        self.arg_name.value,self.default_value.value = (None,None)
        self.target = None
        self.on_update()
        self.bot_layout.update()

    def save_change(self,e):
        if self.arg_name.value and self.target:
            self.change_data(self.target)
        elif self.target:
            self.change_data(self.target)

    def on_update(self,e=None):
        self.preview_block.update_data("def "+self.func_name.value,self.argument_buffer)

    def update_arg_buffer(self):
        self.argument_buffer = [data for data in reversed(self.bot_layout.controls) if isinstance(data,argument_custom)]


    def parse(self):
        return self.argument_buffer

    def load(self,arg_buffer):
        if not self.argument_buffer:
            self.argument_buffer = arg_buffer
            self.bot_layout = reversed(self.argument_buffer)+self.bot_layout

    def load_data(self,data):
        npara,para_data,struct_data = data
        npara = int(npara)
        for i in range(npara):
            argument = argument_custom(parent=self)

            if para_data[i]:
                _,name = para_data[i]["style"][0]
                argument.change_data((name,None))
            self.argument_manager()
            self.bot_layout.controls.insert(0, argument)
            self.update_arg_buffer()
        func_name = struct_data['style'][1]
        _,func_name = func_name
        code_struct = struct_data['struct'][0]
        _,code_name = code_struct
        code_name = code_name[len("def "):]
        self.func_name.value = func_name
        self.code_name.value = code_name
        try:
            self.bot_layout.update()
        except:
            pass
        self.preview_block.update_data("def " + self.func_name.value, self.argument_buffer)

    def submit_data(self):
        extract_data = []
        for item in self.argument_buffer:
            extract_data.append(item.data)
        data = self.code_name.value,self.func_name.value,extract_data
        pi.send_signal_block(data)
    def on_closes(self):
        self.submit_data()
        pi.close_overlay(self)
