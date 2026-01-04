import time

import flet as ft

def line_len(input_string):
    lines = input_string.splitlines()
    return lines,len(lines)
import subprocess
def console_func(target,command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,shell=True,
                                   universal_newlines=True)
        if command == "quit":
            process.kill()
        for line in iter(process.stdout.readline, ''):
            target.get(line)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")
        process.kill()
    finally:
        process.terminate()
        process.wait()

class console(ft.Container):
    def __init__(self,wid=None,hei = None):
        super().__init__()
        self.color = "#000000"
        self.text_color = "#FFFFFF"
        self.height  = 300
        self.bgcolor = self.color
        self.text_data = ""
        self.readonly_area = ft.Container(content=ft.Text(color=self.text_color,value=""))
        self.enter_field = ft.TextField(color=self.text_color,border_color="",border="none",on_submit=self.text_field_submit,max_lines=999999999999,autofocus=True
                                        ,cursor_color=self.text_color)
        self.container = ft.ListView(controls=[self.readonly_area,self.enter_field],padding=ft.padding.only(left=20,bottom=2,right=20,top=10),auto_scroll=False,on_scroll_interval=1)
        self.container.auto_scroll = False
        self.width = wid
        self.height = hei
        self.content = self.container

    def text_field_submit(self,e):
        data = e.control.value
        e.control.value = ""
        console_func(self,data)
        self.add_to_readonly(data + "\n")
        self.enter_field.focus()
        self.update()

    def add_to_readonly(self,data):
        self.text_data += ">>>"+data
        self.text_data= self.data_manage(self.text_data)
        self.readonly_area.content.value = self.text_data
        self.container.scroll_to(offset=-1, duration=0.1)
        #self.container.scroll_to(offset=10, duration=0)

    def data_manage(self,inp_data):
        data,leng = line_len(inp_data)
        if leng > 100:
            new_data = data[leng-100:]
            string = "\n".join(new_data)
            return string+"\n"
        else:
            return inp_data
            #return "\n".join(new_data)


    def get(self,data):
        self.add_to_readonly(data)
        self.update()
        time.sleep(0.01)



def main(page : ft.Page):
    csl = console()
    page.add(csl)
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
