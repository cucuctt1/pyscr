
from setting import *

import blocklogic as b
from utility import auto_para as ap
#

def load_from_local(buffer):
    block_buffer = []
    for data in buffer:
        # add to a container with load function if class args
        if data[0]['block name'] == "class":
            #load block with args one
            struct = data[0]
            block = b.block(x=0, y=0, have_parameter=True, Npara=1, struct=struct,args=True)
            block_buffer.append(block)
        else:
            struct = data[0]
            npara = (ap.auto_para(struct)-1)
            block = b.block(x=0,y=0,have_parameter=True,Npara=npara,struct=struct)
            block_buffer.append(block)
    pass

def load_from_file(file_arr):
    for file in file_arr:
        filename = file+'.json'
        #load to file from CF_store
        #load to local_CF_buffer
        data = None # read here
        if data['block_name'] == "class":
            #load block with args one
            pass
        else:
            #load normal block
            pass

    pass

