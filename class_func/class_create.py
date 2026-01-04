from utility.auto_para import *


def create_class(template,id):
    print(id,template)
    class_code_style = template['style'][1][1]
    class_code_struct = template['struct'][1][1]
    file = template['block setting'][0]
    color = "#FFD800"
    text_color = "#000000"
    block_type = "custom"
    block_name = "class"
    blocksetting = [file]

    #create struct
    struct = {'style': [('text', class_code_style), ('para', None)],
              'color' : color,
              'text color':text_color,
              'block type':block_type,
              'block name':block_name,
              'block setting':blocksetting,
              'struct':[('code',class_code_struct),('bracket', '('),('arg',[]),('adsb',","),('bracket', ')')]
              }
    return struct