import flet as ft
import copy as c
class block(ft.GestureDetector):
    def __init__(self, have_parameter=False,
                  color="WHITE",
                 block_height=30, block_width=150, code=None,Npara=0
                 ,args = False,preview = False,scale = 1,
                 text_color = ft.colors.BLACK):
        super().__init__(self)
        self.scale = scale
        self.text_color = text_color
        self.HaveParameter = have_parameter
        self.preview = preview
        self.left = 100
        self.top = 100
        if self.HaveParameter:
            self.Npara = Npara
        else:
            self.Npara = 0
        self.code = code
        self.color = color
        self.bgcolor = "WHITE"
        self.block_height = block_height*self.scale
        self.block_width = block_width*self.scale
        self.width = self.block_width
        self.height = self.block_height
        self.args = args
        self.on_pan_update = self.drag
        self.content = self.load()

    def load(self):
        print("loader")
        para_wid = 30*self.scale
        para_hei = 20 *self.scale
        para_slot = ft.Container(bgcolor=ft.colors.WHITE,width=para_wid,height=para_hei,border_radius=ft.border_radius.all(4))
        text = ft.Text(self.code,color=self.text_color)
        self.bgcolor = self.color
        display = ft.Row([ft.VerticalDivider(thickness=5,color="WHITE"),text],spacing=10)
        container = ft.Container(content=display, bgcolor="WHITE")
        for n in range(self.Npara):
            display.controls.append(para_slot)

        return container
    def update_data(self,color,text_color,Npara,code):
        para_wid = 30*self.scale
        para_hei = 20 *self.scale
        para_slot = ft.Container(bgcolor=ft.colors.WHITE,width=para_wid,height=para_hei,border_radius=ft.border_radius.all(4))
        text = ft.Text(code,color=text_color)
        leng = max(0,len(code)*6*self.scale)
        self.color = color
        display = ft.Row([ft.VerticalDivider(thickness=5,color=self.color),text],spacing=10*self.scale)
        container = ft.Container(content=display,bgcolor=color,border_radius=ft.border_radius.all(4))
        for n in range(Npara):
            display.controls.append(para_slot)
            leng+=para_wid+10*self.scale
        leng+=40*self.scale
        self.width = max(150*self.scale,leng)
        self.block_width = self.width
        self.content = container

    def drag(self,e):
        e.control.top += e.delta_y*self.scale
        e.control.left += e.delta_x*self.scale
        self.update()

class function(ft.GestureDetector):
    def __init__(self, have_parameter=False,
                  color="WHITE",
                 block_height=30, block_width=150, code=None,Npara=0
                 ,args = False,preview = False,scale = 1,
                 text_color = ft.colors.BLACK,arg_data=[]):
        super().__init__(self)
        self.scale = scale
        self.text_color = text_color
        self.HaveParameter = have_parameter
        self.preview = preview
        self.left = 500
        self.top = 100
        if self.HaveParameter:
            self.Npara = Npara
        else:
            self.Npara = 0
        self.code = code
        self.color = color
        self.bgcolor = "WHITE"
        self.block_height = block_height*self.scale
        self.block_width = block_width*self.scale
        self.width = self.block_width
        self.height = self.block_height
        self.args = args
        self.on_pan_update = self.drag
        self.arg_data = arg_data
        self.content = self.load()

    def load(self):
        para_wid = 30*self.scale
        para_hei = 20*self.scale
        para_slot = ft.Container(bgcolor="#FF6A00",width=para_wid,height=para_hei,border_radius=ft.border_radius.all(4))
        text = ft.Text(self.code,color=self.text_color)
        leng = max(0,len(self.code)*6*self.scale)
        display = ft.Row([ft.VerticalDivider(thickness=1,color=self.color),text],spacing=10*self.scale)
        container = ft.Container(content=display,bgcolor=self.color,border_radius=ft.border_radius.all(4))
        for indice, datas in enumerate(self.arg_data):
            text_data, _ = datas.data
            if not text_data:
                text_data = ""
            text_data_len = max(0, len(text_data) * 6 * self.scale)
            para_wid = max(para_wid, text_data_len)
            slot = ft.Container(bgcolor="#FF6A00", width=para_wid, height=para_hei,
                                border_radius=ft.border_radius.all(4))
            display.controls.append(c.deepcopy(slot))

            leng += para_wid + 10 * self.scale
        leng+=40*self.scale
        self.width = max(150*self.scale,leng)
        self.block_width = self.width

        return container
    def update_data(self,code,para_data):
        para_wid = 30*self.scale
        para_hei = 20*self.scale
        para_slot = ft.Container(bgcolor="#FF6A00",width=para_wid,height=para_hei,border_radius=ft.border_radius.all(4))
        text = ft.Text(code,color=self.text_color)
        leng = max(0,len(code)*6*self.scale)
        display = ft.Row([ft.VerticalDivider(thickness=1,color=self.color),text],spacing=10*self.scale)
        container = ft.Container(content=display,bgcolor=self.color,border_radius=ft.border_radius.all(4))
        for indice,datas in enumerate(para_data):
            para_wid = 30*self.scale
            text_data,_ = datas.data
            if not text_data:
                text_data = ""
            text_data_len = max(0, len(text_data) * 6 * self.scale)
            para_wid = max(para_wid,text_data_len)
            text = ft.Text(value=text_data,color=self.text_color)
            slot = ft.Container(bgcolor="#FF6A00", width=c.copy(para_wid), height=para_hei,
                                     border_radius=ft.border_radius.all(4),content=text,alignment=ft.alignment.center)
            display.controls.append(slot)

            leng+=para_wid+10*self.scale
        leng+=30*self.scale
        self.width = max(150*self.scale,leng)
        self.block_width = self.width
        self.content = container
        try:
            self.update()
        except:
            pass

    def drag(self,e):
        e.control.top += e.delta_y*self.scale
        e.control.left += e.delta_x*self.scale
        self.update()


class for_block(ft.GestureDetector):
    def __init__(self, have_parameter=False,
                  color="WHITE",
                 block_height=30, block_width=150, code=None,Npara=0
                 ,args = False,preview = False,scale = 1,
                 text_color = ft.colors.BLACK,arg_data=[],code2 = None):
        super().__init__(self)
        self.scale = scale
        self.text_color = text_color
        self.HaveParameter = have_parameter
        self.preview = preview
        self.left = 500
        self.top = 100
        if self.HaveParameter:
            self.Npara = Npara
        else:
            self.Npara = 0
        self.code = code
        self.code2 = code2
        self.color = color
        self.bgcolor = "WHITE"
        self.block_height = block_height*self.scale
        self.block_width = block_width*self.scale
        self.width = self.block_width
        self.height = self.block_height
        self.args = args
        self.on_pan_update = self.drag
        self.arg_data = arg_data
        self.content = self.load()

    def load(self):
        para_wid = 30*self.scale
        para_hei = 20*self.scale
        text = ft.Text(self.code,color=self.text_color)
        text2 = ft.Text(self.code2,color=self.text_color)
        if self.arg_data:
            rest = self.arg_data[:-1]
        else:
            rest = self.arg_data
        leng = max(0, len(self.code+self.code2) * 6 * self.scale)
        para_slot = ft.Container(bgcolor="#FF6A00", width=para_wid, height=para_hei,
                                 border_radius=ft.border_radius.all(4))
        display = ft.Row([ft.VerticalDivider(thickness=1, color=self.color), text], spacing=10 * self.scale)

        for item in rest:
            para_wid = 30*self.scale
            text_data_len = max(0, len(item.data) * 6 * self.scale)
            para_wid = max(para_wid, text_data_len)
            text_data = ft.Text(value=item.data, color=self.text_color)
            slot = ft.Container(bgcolor="#FF6A00", width=c.copy(para_wid), height=para_hei,
                                     border_radius=ft.border_radius.all(4),content=text_data,alignment=ft.alignment.center)
            display.controls.append(slot)
            leng += para_wid + 10 * self.scale
        display.controls.append(text2)
        slot = ft.Container(bgcolor="#FFFFFF", width=c.copy(para_wid), height=para_hei,
                            border_radius=ft.border_radius.all(4), alignment=ft.alignment.center)
        display.controls.append(slot)
        leng += para_wid
        leng += 30 * self.scale
        container = ft.Container(content=display, bgcolor=self.color, border_radius=ft.border_radius.all(4))
        self.width = max(150*self.scale,leng)
        self.block_width = self.width
        return container

    def update_data(self,para_data):
        para_wid = 30 * self.scale
        para_hei = 20 * self.scale
        text = ft.Text(self.code, color=self.text_color)
        text2 = ft.Text(self.code2, color=self.text_color)
        rest = para_data[:-1]
        leng = max(0, len(self.code + self.code2) * 6 * self.scale)
        display = ft.Row([ft.VerticalDivider(thickness=1, color=self.color), text], spacing=10 * self.scale)

        for item in rest:

            para_wid = 30 * self.scale
            text_data_len = max(0, len(item.data) * 6 * self.scale)
            para_wid = max(para_wid, text_data_len)
            text_data = ft.Text(value=item.data, color=self.text_color)
            slot = ft.Container(bgcolor="#FF6A00", width=c.copy(para_wid), height=para_hei,
                                border_radius=ft.border_radius.all(4), content=text_data, alignment=ft.alignment.center)
            display.controls.append(slot)
            leng += para_wid + 10 * self.scale
        display.controls.append(text2)
        slot = ft.Container(bgcolor="#FFFFFF", width=c.copy(para_wid), height=para_hei,
                            border_radius=ft.border_radius.all(4), alignment=ft.alignment.center)
        display.controls.append(slot)
        leng += para_wid
        leng += 30 * self.scale
        container = ft.Container(content=display, bgcolor=self.color, border_radius=ft.border_radius.all(4))
        self.width = max(150 * self.scale, leng)
        self.block_width = self.width
        self.content = container
        try:
            self.update()
        except:
            pass

    def drag(self,e):
        e.control.top += e.delta_y*self.scale
        e.control.left += e.delta_x*self.scale
        self.update()


