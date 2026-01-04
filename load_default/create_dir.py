import os
import setting

default_dir = os.path.join(".",'default_block')
folder_dirs = os.listdir(default_dir)
class_func = os.listdir(os.path.join(default_dir,folder_dirs[0]))
condition = os.listdir(os.path.join(default_dir,folder_dirs[1]))
container = os.listdir(os.path.join(default_dir,folder_dirs[2]))
define = os.listdir(os.path.join(default_dir,folder_dirs[3]))
normal = os.listdir(os.path.join(default_dir,folder_dirs[4]))
python_func = os.listdir(os.path.join(default_dir,folder_dirs[5]))
misc = os.listdir(os.path.join(default_dir,folder_dirs[6]))


def create_dir(folder_dirs,choice_dir):
    dir_list = []
    for item in choice_dir:
        dirs = os.path.join(default_dir,folder_dirs,item)
        dir_list.append(dirs)
    return dir_list
#print(create_dir(folder_dirs[0],class_func))