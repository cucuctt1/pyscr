import flet as ft
from utility.color_palette import *
class tab():
    def __init__(self,tab=None,icon=None,icon_color=None,content=None,icon_size = None,text_size = None,
                 text_color = None,text = None):
        self.tab = tab
        self.icon = icon
        self.icon_color = icon_color
        self.content = content
        self.icon_size =icon_size
        self.text_size = text_size
        self.text_color = text_color
        self.text = text
class modded_container(ft.Container):
    def __init__(self,content = None,parent = None,index = None):
        super().__init__()
        self.content = content
        self.on_click = self.onclick
        self.parent = parent
        self.index = index
        self.color_state = False
        self.width =40
        self.height =40
    def change_bg(self,primary):
        self.bgcolor = primary
        self.color_state = not self.color_state
    def onclick(self,e):
        self.parent.select(self.index)
        try:
            self.parent.update()
        except:
            pass
class vertical_tab(ft.Container):
    def __init__(self,tabs:list=[],scroll= False,tab_color=None,
                 main_color=None,tab_wid = 40,wid=None,hei=None,
                 select_index = 1,padding:ft.Padding = None,select_color = white,render_color = white_2):
        super().__init__()
        self.tab_data = tabs
        self.scroll = scroll
        self.tab_color = tab_color
        self.main_color = main_color
        self.tab_wid = tab_wid
        self.width = wid
        self.height = hei
        self.render_color = render_color
        self.select_color = select_color

        self.tab_area = ft.Column(width=self.tab_wid,height=self.height,alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=10)
        self.render_area = ft.Container(bgcolor=render_color,height=self.height,width=self.width-self.tab_wid,margin=ft.margin.only(top=-20))

        self.tab_area_container = ft.Container(content=self.tab_area,bgcolor=self.tab_color)

        self.layout = ft.Row([self.tab_area_container,self.render_area],spacing=0)
        self.padding = padding
        self.bgcolor = self.tab_color

        self.padding = ft.padding.only(top=20)
        self.select_index = select_index
        self.render_buffer = list()
        self.load()
        self.content = self.layout

    def load(self):
        for index,item in enumerate(self.tab_data):
            container = modded_container(content=item.tab,index=index,parent=self) #special container
            self.tab_area.controls.append(container)
            self.render_buffer.append(item.content)
        self.select(self.select_index-1)

    def select(self,index):
        if len(self.render_buffer) >index:
            self.container_select(index)

            self.render_area.content = self.render_buffer[index]
            self.select_index = index+1
            try:
                self.update()
            except:
                pass

    def container_select(self,index):
        self.tab_area.controls[self.select_index-1].change_bg(self.tab_color)
        self.tab_area.controls[index].change_bg(self.select_color)
        try:
            self.update()
        except:
            pass


def main(page:ft.Page):
    page.window_maximized=False
    veti = vertical_tab(
        tab_color="#AA00AA",render_color=white_3,select_color=white,wid=300,select_index=2,hei=1000,tabs=[tab(tab=ft.Container(content=ft.Icon(name=ft.icons.DATASET)),content=ft.Text("homo")),
                                               tab(tab=ft.Container(content=ft.Icon(name=ft.icons.ADD)),content=ft.Text("no homo"))])

    page.add(veti)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)