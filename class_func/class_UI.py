
import flet as ft
from utility.valid_name import filter
from utility.color_palette import *
import page_intermediate as pi
class class_edit(ft.Container):
    def __init__(self,wid,hei,page,parent,top = None,left= None):

        super().__init__()
        self.top = top
        self.left = left
        self.width = wid
        self.height = hei
        self.page = page
        self.parent = parent
        self.bgcolor = white_2
        self.border = ft.border.all(1,white_3)
        self.alignment = ft.alignment.center
        self.border_radius = ft.border_radius.only(top_right=10,bottom_right=10,bottom_left=10)
        self.text = ft.TextField(width = self.width-5,bgcolor="WHITE",height=30,content_padding=ft.padding.all(1),hint_text="Class name")
        self.accept_btn = ft.ElevatedButton(text="Accept",width = (self.width-15)/2,bgcolor="GREEN",color="WHITE",on_click=self.accept_click)
        self.cancel_btn = ft.ElevatedButton(text="Cancel", width=(self.width - 15)/2,bgcolor="RED",color="WHITE",on_click=self.close)
        self.btn_row = ft.Row([self.accept_btn,self.cancel_btn],spacing=5,height=30,alignment=ft.MainAxisAlignment.CENTER)
        self.column = ft.Column([self.text,self.btn_row],alignment=ft.MainAxisAlignment.CENTER)
        self.padding = ft.padding.all(5)
        self.content = self.column


    def open(self,data):
        self.text.value = data

    def accept_click(self,e):
        data = self.text.value
        if data:
            data = filter(data)
            template = self.parent.template
            print(template['style'][1][1],data)
            template['style'][1] = ('text',data)
            template['struct'][1] = ('name',data)
            self.parent.name = data
            pi.send_signal_block(template,type="class")

        self.close()
            #interact

    def close(self,e=None):
        pi.close_overlay(self)
        del self
