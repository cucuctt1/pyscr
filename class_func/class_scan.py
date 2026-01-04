
import blocklogic as b



def scan_check(target,self):
    #print(target,self)
    if self in target.contain:
        target.class_update()
