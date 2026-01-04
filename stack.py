
import flet as ft
class stack_buffer(ft.Stack):
    def __init__(self,wid = 1000,hei =1000):
        super().__init__()
        self.controls = []
        self.data = []
        self.height=500

    def add_block(self,block):
        self.controls.append(block)
        self.data.append(block)

    def interact(self,data,e,mode=1):
        if mode==2:
            try:
                self.controls.remove(e.control)
            except:
                pass
            for item in self.controls:
                if item.left < 300 and item.hide_content:
                    try:
                        self.controls.remove(item)
                    except:
                        pass

            #self.update()
        pass
