
import flet as ft
from utility.color_palette import *



class navigation_drawer(ft.Container):
    def __init__(self,wid = 300):
        super().__init__()
        self.primary_color = white
        self.secondary_color = white_2
        self.border_color = white_3

        self.bgcolor = debug_green
        self.width = wid
        self.height =1000
        self.load_tab()
    def load_tab(self):
        self.tab = ft.Tabs(selected_index=1,
                           expand=1,
                           tabs=[ft.Tab(icon=ft.icons.INSERT_DRIVE_FILE_OUTLINED,
                                        content=ft.Text("this is text")),
                                 ft.Tab(icon=ft.icons.DATASET,
                                        content=ft.Text("this is data"))
                                 ],
                           tab_alignment=ft.TabAlignment.CENTER
                           )
        self.content = self.tab

