import flet as ft
import savefunc.save_function as sf
import global_control as gc
import os
file_dir = ""
def result(e):
    file_dir = e.path if e.path else None
    if file_dir:
        file_dir+=".pyscr"
        sf.write(gc.global_playground.controls,file_dir)

def open_winexp(page):
    save_interface = ft.FilePicker(on_result=result)
    save_interface.file_type = ft.FilePickerFileType.CUSTOM
    save_interface.allowed_extensions = ["pyscr"]
    page.add(save_interface)
    save_interface.save_file(file_type=ft.FilePickerFileType.CUSTOM,allowed_extensions=['pyscr'])

#open_winexp(page)