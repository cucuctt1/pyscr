import flet as ft
import savefunc.read_function as rf
import global_control as gc
from function_UI import func_display as fd
import stack as st
file_dir = ""


def load(data):
    gc.local_CF_buffer = []
    gc.local_class_buffer = []
    # var name

    gc.class_buffer = []
    gc.class_method_buffer = {}


    for n, item in enumerate(data):
        data[n].code_container = gc.global_playground
    gc.global_playground.controls = data
    try:
        gc.global_playground.update()
    except:
        pass

def result(e,target):
    file_dir = e.files[0].path if e.files[0].path else None
    if file_dir:
        gc.global_variable_buffer = []
        data = rf.load_to_block(file_dir)
        load(data)
        target.wipe_all()
        for var in gc.global_variable_buffer:
            target.create_var(var)



def open_winexp(page,target):
    save_interface = ft.FilePicker(on_result=lambda e:result(e,target))
    save_interface.file_type = ft.FilePickerFileType.CUSTOM
    save_interface.allowed_extensions = ["pyscr"]
    page.add(save_interface)
    save_interface.pick_files(file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=['pyscr'])


#open_winexp(page)

