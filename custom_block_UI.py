import flet as ft
from random_req import *
import custom_block as cus_block
import blocklogic as bl
from utility import preview_block as pb
from utility.color_process import *
primary_color = "#FFFFFF"
secondary_color = "#F4F4F4"
border_color = "#D3D3D3"

PREVIEW_HEI = 300

TEXT_WID = 80 #px
TEXT_HEI = 30

class preview_block():
    def __init__(self,color,code,Npara,args,kargs):
        self.color = ft.colors.RED
        self.code = code
        self.Npara = Npara
        self.args = args
        self.kargs = kargs

        self.preview_block = pb.block(color=self.color,code=self.code,have_parameter=True,Npara=self.Npara,args=self.args,preview=True
                                      ,scale=1.6)
        self.preview_block.top = 100
        self.preview_block.left = 400
        self.display = ft.Stack([self.preview_block])


    def update(self,color,code,Npara,args,kargs,text_color):
        self.color = color
        self.code = code
        self.Npara = Npara
        self.args = args
        self.kargs = kargs
        self.text_color = text_color
        self.preview_block = bl.block(color=self.color, code=self.code, have_parameter=True, Npara=self.Npara,
                                      args=self.args, preview=True,scale=1.6,text_color=text_color)
        self.preview_block.top = 100
        self.preview_block.left = 100
        self.display = ft.Stack([self.preview_block])

class color_pick_popup(ft.Container):
    def __init__(self,target = None):
        super().__init__()
        self.primary_color = "#FFFFFF"
        self.secondary_color = "#F4F4F4"
        self.border_color = "#D3D3D3"
        self.width = 300
        self.height = 400
        self.bgcolor = "#E1EAF5"
        self.padding = ft.padding.all(10)
        self.content = self.load_content()
        self.border_radius = ft.border_radius.all(5)
        self.preview_color = ""
        self.target = target
    def load_content(self):
        RGB_track = ft.Column([
            ft.Text("RED",height=30,color="RED",size=15,weight=ft.FontWeight.BOLD),
            ft.Slider(value=255,height=50,divisions=255,min=0, max=255,on_change=lambda e:self.on_change_slider()),
            ft.Text("GREEN",height=30,color="GREEN",size=15,weight=ft.FontWeight.BOLD),
            ft.Slider(value=255,height=50,divisions=255,min=0, max=255,on_change=lambda e:self.on_change_slider()),
            ft.Text("BLUE",height=30,color="BLUE",size=15,weight=ft.FontWeight.BOLD),
            ft.Slider(value=255,height=50,divisions=255,min=0, max=255,on_change=lambda e:self.on_change_slider()),
        ],spacing=0,alignment=ft.alignment.center)
        self.preview_color = secondary_color
        color_preview = ft.Container(bgcolor=self.preview_color,height=50,border=ft.border.all(2, ft.colors.GREY),border_radius=ft.border_radius.all(5))

        random_color_btn = ft.OutlinedButton("random color",on_click=self.random_color,width=300)
        confirm_btn = ft.FilledButton("Confirm",on_click=self.change,width=135)
        dismiss_btn = ft.OutlinedButton("Dismiss",on_click=self.random_color,width=135)
        button_area = ft.Row([dismiss_btn,confirm_btn],spacing=10,alignment=ft.alignment.bottom_center)
        color_render_layout = ft.Column([RGB_track, color_preview,random_color_btn])
        return color_render_layout

    def on_change_slider(self):
        r = self.content.controls[0].controls[1].value
        g = self.content.controls[0].controls[3].value
        b = self.content.controls[0].controls[5].value
        self.preview_color = hex_decode(r,g,b)
        self.content.controls[1].bgcolor = self.preview_color
        self.content.update()

    def random_color(self,e):
        color = generate_random_color()
        r,g,b = rgb_decode(color)
        self.content.controls[0].controls[1].value = r
        self.content.controls[0].controls[3].value = g
        self.content.controls[0].controls[5].value = b
        self.on_change_slider()
    def change(self):
        self.target.control.bgcolor = self.preview_color
        pass
    def change_to_target(self):
        pass
    def dismiss(self,e):
        pass
class custom_block_UI(ft.Container):
    def __init__(self,page):
        super().__init__()
        self.bgcolor = primary_color
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        self.page = page
        self.padding = ft.padding.only(top=10, bottom=10, left=10, right=10)
        self.border_radius = ft.border_radius.all(10)
        self.alignment = ft.alignment.bottom_center
        setting = ft.Row([
            ft.Text("code:"),
            ft.TextField(bgcolor=secondary_color, width=TEXT_WID, height=TEXT_HEI, dense=False,
                         content_padding=ft.padding.only(top=-5, left=3, right=3), border_color=border_color,on_change=self.len_update
                         ),
            ft.VerticalDivider(width=10, color=primary_color),

            ft.Text("function name:"),
            ft.TextField(bgcolor=secondary_color, width=TEXT_WID, height=TEXT_HEI, dense=False,
                         content_padding=ft.padding.only(top=-5, left=3, right=3), border_color=border_color,on_change=self.len_update),
            ft.VerticalDivider(width=10, color=primary_color),

            ft.Text("number of parameter:"),
            ft.TextField(bgcolor=secondary_color, width=TEXT_WID, height=TEXT_HEI, dense=False,
                         content_padding=ft.padding.only(top=-5, left=3, right=3), border_color=border_color,on_change=self.len_update),
            ft.VerticalDivider(width=10, color=primary_color),

            ft.Text("block color:"),
            ft.Container(bgcolor=primary_color, width=TEXT_WID, height=TEXT_HEI,
                          on_click=self.focus_block_color,border_radius=ft.border_radius.all(5),border=ft.border.all(1,border_color)),
            ft.VerticalDivider(width=10, color=primary_color)
            ,
            ft.Text("text color:"),
            ft.Container(bgcolor="BLACK", width=TEXT_WID, height=TEXT_HEI,
                          on_click=self.text_color_focus,border_radius=ft.border_radius.all(5),border=ft.border.all(1,border_color)),
            ft.VerticalDivider(width=10, color=primary_color),

            ft.Text("args"),
            ft.Checkbox(label="enable", width=TEXT_WID, height=TEXT_HEI),
            ft.VerticalDivider(width=10, color=primary_color),

            ft.Text("kwarg"),
            ft.Checkbox(label="enable", width=TEXT_WID, height=TEXT_HEI)

        ], spacing=5, tight=True, wrap=True, alignment=ft.alignment.center)

        block_preview = ft.Container(bgcolor=secondary_color, height=PREVIEW_HEI,
                                     border_radius=ft.border_radius.all(10))
        self.block_preview_content = preview_block(code = "",color = "",Npara = 0,args=False,kargs=False)
        block_preview.content = self.block_preview_content.display
        block_preview.alignment = ft.alignment.center
        dismiss_btn = ft.FilledButton("Dismiss",width=100)
        accept_btn = ft.OutlinedButton("Accept",width=100) # add new block here
        button_row = ft.Row([dismiss_btn,accept_btn],spacing=10)
        self.vertical_layout = ft.Column([block_preview,setting,button_row],spacing=8)
        self.content = self.vertical_layout
        self.page.update()
        #self.dialog_setup()

    def dialog_setup(self,e,accept_target):
        confirm_btn = ft.FilledButton("Confirm",width=135,on_click=accept_target)
        dismiss_btn = ft.OutlinedButton("Dismiss",width=135,on_click=self.dismiss)
        self.color_pick_popup = ft.AlertDialog(
            modal=True,
            content= color_pick_popup(e)
            ,on_dismiss=lambda e:print("hh"),
            actions=[
                dismiss_btn,confirm_btn
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
            )
    def focus_block_color(self,e):
        self.dialog_setup(e,self.change)
        self.open_dlg(self.color_pick_popup)
    def text_color_focus(self,e):
        self.dialog_setup(e,self.text_change)
        self.open_dlg(self.color_pick_popup)
    def text_change(self,e):
        self.color_pick_popup.content.change()
        self.color_pick_popup.open = False
        self.update_preview()
        self.page.update()
    def open_dlg(self,dialog):
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    def dismiss(self,e):
        self.color_pick_popup.open = False
        self.page.update()
    def change(self,e):
        self.color_pick_popup.content.change()
        bgcolor = self.content.controls[1].controls[10].bgcolor
        self.content.controls[1].controls[13].bgcolor = cus_block.generate_contrasting_color(bgcolor,brightness_threshold=100)
        self.color_pick_popup.open = False
        self.update_preview()
        self.page.update()
    def len_update(self,e):
        self.update_preview()
    def update_preview(self):
        code = self.content.controls[1].controls[1].value
        name = self.content.controls[1].controls[4].value
        try:
            npara = int(self.content.controls[1].controls[7].value)
        except:
            npara = 0
        base_color = self.content.controls[1].controls[10].bgcolor
        text_color = self.content.controls[1].controls[13].bgcolor
        print(base_color)
        self.block_preview_content.preview_block.update_data(color=base_color,code=name,Npara=npara,text_color = text_color)
        self.content.controls[0].content = self.block_preview_content.display
        self.page.update()



def main(page:ft.Page):
    page.window_maximized=False
    color_render = custom_block_UI(page)
    page.add(color_render)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)