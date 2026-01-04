import flet as ft
import global_control as gc
import os
import start_parse as sp
file_dir = ""

def write(file):
    with open(file,"w+") as f:
        data = sp.get_code(gc.global_playground)
        f.write(str(data))
def result(e):
    file_dir = e.path if e.path else None
    if file_dir:
        file_dir+=".py"
        write(file_dir)

def open_winexp(page):
    save_interface = ft.FilePicker(on_result=result)
    save_interface.file_type = ft.FilePickerFileType.CUSTOM
    save_interface.allowed_extensions = ["py"]
    page.add(save_interface)
    save_interface.save_file(file_type=ft.FilePickerFileType.CUSTOM,allowed_extensions=['py'])

#open_winexp(page)
def main(page: ft.Page):
    page.window_maximized = False
    open_winexp(page)
    print(file_dir)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)