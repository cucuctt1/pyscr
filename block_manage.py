import blocklogic as b
import flet as ft
import random
import string
from json_process import json_reader as jsrd

dir = "./default_block/"

print_dir = dir+"normal_block/print.json"
var_dir = dir+"variable/variable.json"
add_dir = dir+"normal_block/add.json"
assign_dir = dir+"normal_block/assign.json"
def_dir = dir+"define/def.json"
for_dir = dir+"container/for.json"
if_dir = dir+"container/if.json"
class_dir = dir+"class/class.json"
def generate_random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def add_print(stack,page):
    data = b.block(x=190, y=190, color=ft.colors.GREY, content=None,
                   code_container=stack, id="level 3 block",struct = jsrd.read_json(print_dir)
                   ,have_parameter=True,Npara=1,args=True,page=page)
    stack.controls.append(data)
    del data
    stack.update()

def add_variable(stack):
    random_data = generate_random_string(10)
    data = b.block( x=235, y=65, color=ft.colors.GREEN, content=None, code_container=stack, id="level 1 block",name=random_data,struct=jsrd.read_json(var_dir),Npara=0)
    stack.controls.append(data)
    del data
    stack.update()

def add_add(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",have_parameter=True,Npara=2,struct=jsrd.read_json(add_dir))
    stack.controls.append(data)
    del data
    stack.update()
def add_assign(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",
                   have_parameter=True, Npara=2, struct=jsrd.read_json(assign_dir))
    stack.controls.append(data)
    del data
    stack.update()

def add_def(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",
                   have_parameter=True, Npara=0, struct=jsrd.read_json(def_dir),iscontainer=True,clone_para=True)
    stack.controls.append(data)
    del data
    stack.update()

def add_for(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",
                   have_parameter=True, Npara=2, struct=jsrd.read_json(for_dir),iscontainer=True,clone_para=True,clone_restrict=-1)
    stack.controls.append(data)
    del data
    stack.update()
def add_if(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",
                   have_parameter=True, Npara=1, struct=jsrd.read_json(if_dir),iscontainer=True)
    stack.controls.append(data)
    del data
    stack.update()

def add_class(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack,
                   have_parameter=True, Npara=1, struct=jsrd.read_json(class_dir),iscontainer=True)
    stack.controls.append(data)
    del data
    stack.update()






