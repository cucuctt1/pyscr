import flet as ft
from utility import string_process as sp
from utility import preview_block as pb
import page_intermediate as pi

class argument_custom(ft.ElevatedButton):
    def __init__(self,data='',wid = 150,parent=None,bgcolor = "#FF6A00",color ="WHITE" ):
        super().__init__()
        self.data = data
        self.width = wid
        self.text = ""
        self.bgcolor =bgcolor
        self.parent = parent
        self.on_click = self.onclick
        self.color = color

    def change_data(self,data):
        self.data = data
        self.text = self.data
        try:
            self.update()
        except:
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
        self.preview_block = pb.for_block(scale=1.6,Npara=4,have_parameter=True
                                         ,preview =  True,text_color="#000000",color="#FFD800",
                                         code="for ",code2="in")
        self.preview_block.bgcolor = "#FFD800"
        self.preview_canvas = ft.Stack()
        self.preview_canvas.controls.append(self.preview_block)
        self.preview.content = self.preview_canvas
    def load_setting(self):
        # argument setting
        self.argsetting_layout = ft.Row(spacing=10)
        self.arg_name_text = ft.Text(value="Argument name")
        self.arg_name = ft.TextField(width=150,height=40,dense=False,content_padding=ft.padding.only(top=0,left=5,right=5),on_change=self.on_update)

        self.save_btn = ft.ElevatedButton(text="Save change",width=180,height=40,on_click=self.save_change)
        self.button_container = ft.Container(content=self.save_btn,alignment=ft.alignment.center)

        self.argsetting_layout.controls = [self.arg_name_text,self.arg_name,
                                           self.button_container]
        self.seperate_content = self.argsetting_layout

        self.top_layout = ft.Row([self.seperate_content],spacing=10,alignment=ft.MainAxisAlignment.SPACE_EVENLY)
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
                if item.data == None:
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
        self.arg_name.value = data
        self.target = target
        self.on_update()
        self.bot_layout.update()
        self.setting.update()

    def change_data(self,target:argument_custom):
        data = self.arg_name.value
        target.change_data(data)
        self.arg_name.value = None
        self.target = None
        self.on_update()
        self.bot_layout.update()

    def save_change(self,e):
        if self.arg_name.value and self.target:
            self.change_data(self.target)

    def on_update(self,e=None):
        self.preview_block.update_data(self.argument_buffer)

    def update_arg_buffer(self):
        self.argument_buffer = [data for data in reversed(self.bot_layout.controls) if isinstance(data,argument_custom)]
        self.argument_buffer.append(argument_custom(color="BLACK",bgcolor="#FFFFFF"))

    def load(self,arg_buffer):
        if not self.argument_buffer:
            self.argument_buffer = arg_buffer
            self.bot_layout = reversed(self.argument_buffer)+self.bot_layout


    def load_data(self,data):
        pass

    def submit_data(self):
        extract_data = []
        for item in self.argument_buffer[:-1]:
            if item.data:
                extract_data.append(item.data)

        pi.send_signal_block(extract_data,type="for")
    def on_closes(self):
        self.submit_data()
        pi.close_overlay(self)

def main(page:ft.Page):
    page.window_maximized=False
    function_ui = function_UI(page.width)
    page.add(function_ui)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)