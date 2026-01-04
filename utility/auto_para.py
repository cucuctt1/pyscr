def auto_para(struct):
    style = struct['style']
    n = 0
    for item in style:
        if item == ('para',None):
            n+=1
    return n