import flet as ft


class new_container(ft.Container):
    def __init__(self,wid = None,hei = None,mode:str = None,bgcolor=None,
                 navigation_color = None,navigation_thickness = 3,content = None,min_area = 5,page = None):
        super().__init__()
        self.width = wid
        self.height = hei
        valid_mode = ["up","down","left","right"]
        if mode.lower() not in valid_mode:
            raise "Please choose from: up, down, left, right"
        else:
            self.mode = mode.lower()
        self.layout_bgcolor = bgcolor
        self.navigation_color = navigation_color
        self.navigation_thickness = navigation_thickness
        self.layout_content = content
        self.min_area = min_area
        # self.padding = ft.padding.all()
        self.loadlayout(self.layout_content)
        self.main_container.content = self.layout_content
        self.bgcolor=ft.colors.BLACK
        self.content = self.main_layout
        self.mouse_on_top = False
        self.page = page


    def loadlayout(self,content = None):
        self.main_layout = ft.GestureDetector(on_hover=self.hover, on_pan_start=self.start_check,
                                              on_pan_update=self.scale_func, mouse_cursor=ft.MouseCursor.BASIC,
                                              width=self.width, height=self.height)
        if self.mode == "up":
            self.navigation = ft.Container(height=self.navigation_thickness, bgcolor=self.navigation_color)
            self.main_container = ft.Container(bgcolor=self.layout_bgcolor, height=self.height - self.navigation_thickness,content=content)
            self.layout = ft.Column([self.navigation, self.main_container], spacing=0)
        elif self.mode == "down":
            self.navigation = ft.Container(height=self.navigation_thickness, bgcolor=self.navigation_color)
            self.main_container = ft.Container(bgcolor=self.layout_bgcolor, height=self.height - self.navigation_thickness,content=content)
            self.layout = ft.Column([self.main_container,self.navigation], spacing=0)
        elif self.mode == "left":
            self.navigation = ft.Container(bgcolor=self.navigation_color, width=self.navigation_thickness)
            self.main_container = ft.Container(bgcolor=self.layout_bgcolor, width=self.width - self.navigation_thickness,content=content)
            self.layout = ft.Row([self.navigation, self.main_container], spacing=0)
        elif self.mode == "right":
            self.navigation = ft.Container(bgcolor=self.navigation_color, width=self.navigation_thickness)
            self.main_container = ft.Container(bgcolor=self.layout_bgcolor, width=self.width - self.navigation_thickness,content=content)
            self.layout = ft.Row([self.main_container,self.navigation], spacing=0)
        self.main_layout.content = self.layout
    def hover(self,e):
        if self.mode == "up":
            if 10 >= e.local_y >= 0:
                self.main_layout.mouse_cursor = ft.MouseCursor.RESIZE_ROW
            else:
                self.main_layout.mouse_cursor = ft.MouseCursor.BASIC
        elif self.mode == "down":
            if self.height >= e.local_y >= self.height-10:
                self.main_layout.mouse_cursor = ft.MouseCursor.RESIZE_ROW
            else:
                self.main_layout.mouse_cursor = ft.MouseCursor.BASIC
        elif self.mode == "left":
            if 10 >= e.local_x >= -4:
                self.main_layout.mouse_cursor = ft.MouseCursor.RESIZE_COLUMN
            else:
                self.main_layout.mouse_cursor = ft.MouseCursor.BASIC
        elif self.mode == "right":
            if self.width >= e.local_x >= self.width-10:
                self.main_layout.mouse_cursor = ft.MouseCursor.RESIZE_COLUMN
            else:
                self.main_layout.mouse_cursor = ft.MouseCursor.BASIC
        e.control.update()
    def scale_func(self,e):
        self.sub_size_change(e.delta_x,e.delta_y)
        if self.mouse_on_top:
            if self.mode == "up":
                self.height -= e.delta_y
                e.control.content.controls[1].height = self.height
                e.control.height -= e.delta_y
                self.height = max(self.height,self.min_area)
                self.content.height = max(self.content.height, self.min_area)
            elif self.mode == "down":
                self.height += e.delta_y
                e.control.content.controls[0].height = self.height
                e.control.height += e.delta_y
                self.height = max(self.height, self.min_area)
                self.content.height = max(self.content.height, self.min_area)
            elif self.mode == "left":
                self.width -= e.delta_x
                e.control.content.controls[1].width = self.width
                e.control.width -= e.delta_x
                self.width = max(self.width, self.min_area)
                self.content.width = max(self.content.width, self.min_area)
            elif self.mode == "right":
                self.width += e.delta_x
                e.control.content.controls[0].width = self.width
                e.control.width += e.delta_x
                self.width = max(self.width, self.min_area)
                self.content.width = max(self.content.width, self.min_area)
        self.update()

    def start_check(self,e):
        if self.mode == "up":
            if 10 >= e.local_y >= 0:
                self.mouse_on_top = True
            else:
                self.mouse_on_top = False
        elif self.mode == "down":
            if self.height >= e.local_y >= self.height-10:
                self.mouse_on_top = True
            else:
                self.mouse_on_top = False
        elif self.mode == "left":
            if 10 >= e.local_x >= -4:
                self.mouse_on_top = True
            else:
                self.mouse_on_top = False
        elif self.mode == "right":
            if self.width >= e.local_x >= self.width-10:
                self.mouse_on_top = True
            else:
                self.mouse_on_top = False

    def sub_size_change(self,delta_x,delta_y):
        index = self.page.controls.index(self)
        for item in range(max(0,index)):
            print(self.page.controls[item].height)
            if self.mode == "up":
                self.page.controls[item].height = self.page.height-(self.height)
                self.page.controls[item].update()
            elif self.mode == "down":
                pass
            elif self.mode == "left":
                pass
            elif self.mode == "right":
                pass

def main(page : ft.Page):
    def update(e):
        #print(e.control.controls)
        e.control.update()
    csl = new_container(wid=100,hei=300,mode="left",bgcolor=ft.colors.RED,navigation_color=ft.colors.GREY
                        ,navigation_thickness=4,page=page)
    csl2 = new_container(wid=None, hei=100, mode="up", bgcolor=ft.colors.RED, navigation_color=ft.colors.GREY,
                        navigation_thickness=4,page=page)
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.END
    page.add(csl,csl2)
    page.on_window_event = update
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
