
import savefunc.save_function as sf
def start_parse(stack):
    code = ""
    datad = stack.controls
    sf.write(obj=datad,filename="myfile.txt")
    for item in stack.controls:
        if item.IsHeader:
            for item in item.below_code:
                code += item.code_parser() + "\n"
                #print(code)
            #exec(code)

def get_code(stack):
    code = ""
    for item in stack.controls:
        if item.IsHeader:
            for itemd in item.below_code:
                code += itemd.code_parser() + "\n"
    return code