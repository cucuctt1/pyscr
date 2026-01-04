#new block test

import flet as ft
import copy as c
import page_intermediate as pi
import utility.color_process
from utility.string_process import *
from function_UI import create_func as cf
from function_UI import local_CF_buffer as lCFb
import global_control as gc
from class_func import class_scan as csc
import random_req as rq
def text_tranform(text):
    if isinstance(text,str):
        return text
    else:
        return text

class block(ft.GestureDetector):
    def __init__(self, iscontainer=False, have_parameter=False,
                 isheader=False, executable=False,
                 id=1, x=None, y=None, color=None, content=None, code_container=None,
                 block_height=30, block_width=150, name="", below_code=[], upper_code=None, contain=[],Npara=0,struct = None
                 ,args = False,preview = False,scale = 1,
                 text_color = ft.colors.BLACK,page = None,clone_para= False,clone_restrict = 0,indisplay = False):
        super().__init__(self)
        self.scale = scale

        self.text_color = text_color
        self.border_color = "#000000"
        self.IsContainer = iscontainer
        self.HaveParameter = have_parameter
        self.IsHeader = isheader
        self.Executable = executable
        self.preview = preview
        if self.HaveParameter:
            self.Npara = Npara
        else:
            self.Npara = 0
        self.clone_para = clone_para
        self.clone_restrict = clone_restrict# from right to left
        self.id = id
        self.top = y
        self.left = x
        self.color = color
        self.content = content
        self.code_container = code_container
        self.page = page
        self.page2 = page#over purpose
        self.expand = True
        self.in_display = indisplay

        self.block_height = block_height*self.scale
        self.block_width = block_width*self.scale
        self.width = self.block_width
        self.height = self.block_height

        self.below_code = list(below_code)
        self.upper_code = upper_code
        self.contain = list(contain)
        self.parameter_buffer = [None]*(self.Npara)
        self.args = args
        self.func_buffer = []
        self.class_id = None

        self.offset_height = 20*self.scale
        self.offset1 = 20*self.scale
        self.top_part = 30*self.scale
        self.bot_part = 20*self.scale

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.end_drag
        self.text_wid = 5*10*self.scale

        self.sideblock_offset = 30
        self.hook = None
        self.side_block = None
        self.on_enter = self.hover
        self.on_exit = self.leave
        #code parser
         #string data

        self.template = struct
        self.name = name#name
        self.load_template()
        self.hook_to_mouse = False
        self.load_block()

        self.hide_content = False
        self.content_hide = None
        self.reset_para_size()


    def __deepcopy__(self, memo):
        new_instance = block(
            iscontainer=self.IsContainer,
            have_parameter=self.HaveParameter,
            isheader=self.IsHeader,
            executable=self.Executable,
            id=self.id,
            x=self.left,
            y=self.top,
            color=self.color,
            content=self.content,
            code_container=self.code_container,
            block_height=self.block_height,
            block_width=self.block_width,
            name=self.name,
            below_code=c.deepcopy(self.below_code, memo),
            upper_code=self.upper_code,
            contain=c.deepcopy(self.contain, memo),
            Npara=self.Npara,
            struct=self.template,
            args=self.args,
            preview=self.preview,
            scale=self.scale,
            text_color=self.text_color,
            page=self.page,
            clone_para=self.clone_para,
            clone_restrict=self.clone_restrict,
            indisplay=self.in_display
        )

        if hasattr(self, 'template'):
            new_instance.template = c.deepcopy(self.template, memo)
        memo[id(self)] = new_instance

        return new_instance

    def hover(self,e):
        if not self.hook_to_mouse and self.in_display:
            self.stack_interact(e=e,mode=1)
            self.hook_to_mouse = True

    def leave(self,e):
        if self.hook_to_mouse and self.in_display:
            self.stack_interact(e=e,mode=2)
            self.hook_to_mouse = False
    def load_template(self):
            self.style = self.template["style"]
            self.color = self.template["color"]
            self.border_color = utility.color_process.border_color(self.color)
            self.text_color = self.template["text color"]
            self.block_type = self.template["block type"]
            self.block_name = self.template["block name"]
            self.block_setting = self.template["block setting"]
            self.struct = self.template["struct"]
            if self.block_type == "variable":
                self.style[0] = ("text",self.name)
            if self.block_type == "container" or self.block_type == "class":
                self.IsContainer = True


    def struct_create(self):
        para_data = []
        for item in self.parameter_buffer:
            if item:
                para_data.append(item.template)
            else:
                para_data.append(None)
        packed_data = (self.Npara,para_data,self.template)
        return packed_data
    def get_click(self,e):

        if self.block_name == "def":
            pi.get_signal_block(self.struct_create(),type="func",target=self)
        elif self.block_name == "for":
            pi.get_signal_block(self.struct_create(), type="for", target=self)
        elif self.block_name == "class":
            pi.get_signal_block(self.struct_create(), type="class", target=self,e=e)
    def load_para(self,element_array):#->data

        spacing = 10*self.scale

        para_wid = 30 *self.scale#default
        para_hei = 20 *self.scale#default
        para_x,para_y= None,None
        para_block = ft.Container(bgcolor=ft.colors.WHITE,width=para_wid,height=para_hei,top=para_y,left=para_x)

        text_data = ""
        text_size = None #default
        text_wid = (len(text_data))*10*self.scale
        text_hei = None
        text_y = None
        text_x = None
        text_block = ft.Text(size=text_size,value=text_data,width=text_wid,height=text_hei,top=text_y,left=text_x)

        right_padding = 10
        row_buffer = []
        for item in element_array:
            block_type, data = item

            if block_type=="text":
                text_block = ft.Text(size=text_size, value=text_data, width=text_wid, height=20,color=self.text_color)
                text_block.value = data
                text_block.width = (len(data))*10*self.scale
                row_buffer.append(text_block)
            elif block_type == "btn":
                btn = ft.Container(content=ft.Icon(name=ft.icons.MORE_VERT,color=self.text_color),width=para_wid,height=para_wid,on_click=self.get_click)
                row_buffer.append(btn)

            else:
                content_text_field = ft.TextField(width=para_wid,text_size=15,dense=False,bgcolor=ft.colors.WHITE,cursor_height=para_hei-3,content_padding=ft.padding.only(top=-4,left=3,right=3),on_change=self.on_change)
                para_block = ft.Container(bgcolor=None,width=para_wid,height=para_hei,content=content_text_field)
                row_buffer.append(para_block)
        return list(row_buffer)

    def on_change(self,e):
        data = e.control.value
        data_len = int(len(data)*10-(len(data)*0.553333))
        for index,item in enumerate(self.arg_buffer):
            if e.control is item.content:
                try:
                    e.control.focus()
                except:
                    pass
                self.change_wid(data_len,item)
                break
    def change_wid(self,wid,slot):

        slot.width = max(30,wid)
        self.size_manage()
        self.reset_para_size()
        self.content_update()
        try:
            self.code_container.update()
        except:
            pass
        pass
    def get_row_wid(self,row):
        res = 0
        for item in row:
            res+=item.width
            res+=10
        return res+10

    def get_center(self,item):
        if self.IsContainer:
            center  =(self.top_part-item.height)/2
        else:
            center = (self.block_height-item.height)/2
        return center

    def posion_manage(self,row,para_array,spacing = 10,size=10):
        change_x = 5*self.scale
        for n,packed_data in enumerate(row):
            data_type,data = packed_data
            if data_type == "text":
                text_wid = (len(data)*size)*self.scale
                para_array[n].left = change_x
                para_array[n].top = self.get_center(para_array[n])
                change_x += text_wid+spacing
            else:
                block_wid = int(para_array[n].width)

                para_array[n].left = change_x
                para_array[n].top = self.get_center(para_array[n])

                # try:
                #     index = self.arg_buffer.index(para_array[n])
                #     side_block = self.parameter_buffer[index]
                #     if side_block:
                #         side_wid = side_block.get_side_block_wid()
                #     else:
                #         side_wid = 0
                # except:
                #     side_wid = 0
                change_x += block_wid+spacing

    def get_side_block_wid(self):
        if self.side_block:
            wid = self.side_block.block_width
            return wid + self.side_block.get_side_block_wid() + 1
        else:
            return 0

    def load_block(self):
        if self.template:
            self.data = self.style
        else:
            self.data = [("text","none")]
        self.para_data = self.load_para(self.data)
        self.posion_manage(self.data,self.para_data)
        self.arg_buffer = [item for item in self.para_data if isinstance(item,ft.Container)]
        self.block_width = max(self.block_width,self.get_row_wid(self.para_data))
        display = ft.Stack()
        display.controls.extend(self.para_data)

        if self.IsContainer:
            self.content = ft.Column([
                ft.Container(height=self.top_part, width=self.block_width, bgcolor=self.color,
                             content=display,border_radius=ft.border_radius.only(top_left=4,top_right=4,bottom_right=4)),
                ft.Container(height=self.offset_height, width=self.offset1, bgcolor=self.color),
                ft.Container(height=self.bot_part, width=self.block_width, bgcolor=self.color,border_radius=ft.border_radius.only(bottom_left=4,top_right=4,bottom_right=4))
            ], spacing=0,tight=True)
        else:
            self.content = ft.Container(height=self.block_height, width=self.block_width, content=display, bgcolor=self.color,border=ft.border.all(1,ft.colors.BLACK),border_radius=4)
    def get_below(self):
        if self.upper_code:
            if self in self.upper_code.contain:
                index = self.upper_code.contain.index(self)
                return list(self.upper_code.contain[index+1:])
            else:
                index = self.upper_code.below_code.index(self)
                return list(self.upper_code.below_code[index+1:])
        else:
            return self.below_code
    def reset_height(self):
        self.offset_height = 20
        for item in self.contain:
            self.offset_height+=item.block_height
        if self.IsContainer:
            self.block_height = self.top_part+self.bot_part+self.offset_height
        if self.upper_code:
            self.upper_code.reset_height()

        self.place_block()
        self.content_update()

    def move_to_end(self,target):
        try:#end of code container list
            self.code_container.controls.remove(target)
            self.code_container.controls.append(target)
        except:
            pass

    def move_ontop(self):
        self.move_to_end(self)
        for below in self.below_code:
            below.move_ontop()
        if self.IsContainer:
            for code in self.contain:
                code.move_ontop()
        if self.HaveParameter:
            for code in self.parameter_buffer :
                if code != None:
                    code.move_ontop()
        if self.side_block:
            self.side_block.move_ontop()
    def stack_interact(self,e,mode=1):
        if self.code_container:
            self.code_container.interact(data=self,e=e,mode=mode)
    def start_drag(self,e:ft.DragStartEvent):
        self.showcontent()
        self.hide_content = False
        self.hook_to_mouse = False
        self.in_display = False
        # print(self.code_container)
        if not self.preview:
            self.move_ontop()
            if self.upper_code and self not in self.upper_code.parameter_buffer:
                below_code = self.get_below()
                self.start_pos_list  = [(code.left,code.top) for code in below_code]
                if self.upper_code:
                    if self in self.upper_code.contain:
                        self.upper_code.contain.remove(self)
                        if self.upper_code.block_name == "class":
                            #fix later
                            self.upper_code.class_update()
                        self.upper_code.contain = [item for item in self.upper_code.contain if item not in below_code]
                    else:
                        self.upper_code.below_code.remove(self)
                        self.upper_code.below_code = [item for item in self.upper_code.below_code if item not in below_code]
                    for item in below_code:
                        self.add_to_below(item)
                    self.upper_code.reset_height()
                    self.code_container.update()
                    self.upper_code = None
            elif self.upper_code and not self.IsContainer:
                index = self.upper_code.parameter_buffer.index(self)
                if (self.upper_code and not self.upper_code.clone_para) or (self.upper_code and self.upper_code.clone_para and self.upper_code.clone_restrict == len(self.upper_code.parameter_buffer)-2-index):
                    index = self.upper_code.parameter_buffer.index(self)
                    self.upper_code.parameter_buffer[index] = None
                    self.upper_code.reset_para_size()
                    self.upper_code.place_block()
                    self.upper_code = None
                    self.code_container.update()
                else:
                    new_copy = c.deepcopy(self)
                    index = self.upper_code.parameter_buffer.index(self)

                    self.code_container.controls.append(new_copy)
                    #self.code_container.update()
                    self.upper_code.parameter_buffer[index] = new_copy
                    #self.upper_code.reset_para_size()
                    self.upper_code = None
                    #self.code_container.update()

            elif self.hook:
                temp = self.hook.side_block
                self.hook.side_block = None
                temp.reset_para_size()
                self.hook = None
                self.code_container.update()
        if self.upper_code:
            self.upper_code.reset_height()
            self.code_container.update()

    def drag(self, e: ft.DragUpdateEvent):
        if not self.preview or not self.in_display:
            self.move(delta_x=e.delta_x, delta_y=e.delta_y,bedrag=True)
            self.code_container.update()

    def move(self, delta_x, delta_y,bedrag = False):
        self.left += delta_x
        self.top += delta_y

        if ((self.top >=1400 or self.top < 40) or (self.left >= 2000 or self.left < 300)) and not bedrag:
            self.visible = False
        else:
            self.visible = True

        for child_block in self.below_code:
            child_block.move(delta_x, delta_y,bedrag)
        if self.IsContainer:
            for child_block in self.contain:
                child_block.move(delta_x, delta_y,bedrag)
        if self.HaveParameter:
            for child_block in self.parameter_buffer:
                if child_block:
                    child_block.move(delta_x,delta_y,bedrag)
        if self.side_block:
            self.side_block.move(delta_x,delta_y,bedrag)

    def end_drag(self,e : ft.DragEndEvent):
        self.code_container.interact(data=None,e=None,mode=2)
        if self.template and not self.block_setting:
            try:
                self.block_setting.append(rq.generate_random_string(10))
            except:
                pass
        if not self.preview:
            for item in self.code_container.controls:
                stick_status = self.stick_check(item)

                if item.IsContainer:
                    if item.upper_code:
                        if stick_status == 2:
                            item.add_to_contain(self)
                            if self.upper_code and self.upper_code.block_name == "class":
                                csc.scan_check(self.upper_code, self)
                            self.reset_height()
                            self.code_container.update()
                            return
                    else:
                        if stick_status == 1:
                            item.add_to_below(self)
                            self.reset_height()
                            self.code_container.update()
                            return
                        if stick_status == 2:
                            item.add_to_contain(self)
                            if self.upper_code and self.upper_code.block_name == "class":
                                csc.scan_check(self.upper_code, self)
                            self.reset_height()
                            self.code_container.update()
                            return
                else:
                    if not item.upper_code:
                        if stick_status == 1:
                            item.add_to_below(self)
                            self.reset_height()
                            self.code_container.update()
                            return
                    if not item.IsContainer and not self.hook and not self.IsContainer:
                        if stick_status == 4:
                            item.add_to_sideblock(self)
                            self.code_container.update()
                            return
                if item.HaveParameter and not self.below_code and not self.IsContainer:
                    for n,para_slot in enumerate(item.arg_buffer):
                        stick_status_para = self.stick_check(item,para=para_slot)
                        if stick_status_para == 3:

                            item.add_to_para(self,n)
                            return
        self.limit_check(300-self.block_width*0.5)
        if self.upper_code and self.upper_code.block_name == "class":
            csc.scan_check(self.upper_code,self)
        #gc.globals_rbb.add_content(c.deepcopy(self.code_container.controls))

    def get_next_slot_contain(self):
        result = 0
        for item in self.contain:
            result+=item.block_height
        return result
    def get_next_slot_below(self):
        result = 0
        for item in self.below_code:
            result+=item.block_height
        return result
    def limit_check(self,limit = 260):
        if self.left < limit and not self.IsHeader:
            self.self_destroy()

    def self_destroy(self):
        try:
            self.code_container.controls.remove(self)
        except:
            pass
        try:
            lCFb.remove_from_buffer(self.block_setting[0])
        except:
            pass
        if self.block_name == "class":
            gc.remove_class(self)
        for item in self.below_code:
            item.self_destroy()
        if self.side_block:
            self.side_block.self_destroy()
        for item in self.parameter_buffer:
            if item:
                item.self_destroy()
        for item in self.contain:
            item.self_destroy()
        self.code_container.update()

        del self
    def stick_check(self,target,para = None) -> int: # return status
        upper_check = self.upper_code is None
        if upper_check:
            x_axis_check = -15*self.scale <= self.left - target.left < 80*self.scale
            y_axis_check = -8*self.scale <=self.top - (target.top+target.get_next_slot_below()+target.block_height) < 25*self.scale
        else:
            x_axis_check = False
            y_axis_check = False
        container_check = target.IsContainer
        if container_check:
            x_axis_check_contain = -30*self.scale <= self.left - (target.left) < 80*self.scale
            y_axis_check_contain = -8*self.scale <=self.top - (target.top+target.get_next_slot_contain()+target.top_part) < 25*self.scale
        else:
            x_axis_check_contain = False
            y_axis_check_contain = False

        have_parameter_check = target.HaveParameter
        if have_parameter_check and para:
            x_axis_check_para = -5*self.scale <= self.left -(para.left+target.left) < 25*self.scale
            y_axis_check_para = -3*self.scale <= self.top - (para.top+target.top) < 15*self.scale

        else:
            x_axis_check_para = False
            y_axis_check_para = False

        hook_check = not self.hook
        if hook_check and not target.side_block:
            x_axis_check_sideblock = -5*self.scale <= self.left -(target.left+target.block_width) < 15*self.scale
            y_axis_check_sideblock = -3*self.scale <= self.top - (target.top) < 18*self.scale
        else:
            x_axis_check_sideblock = False
            y_axis_check_sideblock = False

        if x_axis_check_sideblock and y_axis_check_sideblock:
            return 4
        if x_axis_check_para and y_axis_check_para:
            return 3
        if y_axis_check_contain and x_axis_check_contain:
            return 2
        if x_axis_check and y_axis_check:
            return 1
        return 0

    def add_to_sideblock(self,target):
        self.side_block = target
        target.hook = self
        self.size_manage()
        self.place_block()
    def add_to_para(self,target,slot):
        #this make me stupid af

        try:
            if not self.parameter_buffer[slot] and target != self:
                target.upper_code = self
                self.arg_buffer[slot].content.value = ""
                self.parameter_buffer[slot] = target
                self.set_size_para(target, slot)
                self.size_manage()

                self.place_block()
                self.code_container.update()
        except:

            pass

    def content_update(self):
        #print("addd")
        if self.IsContainer:
            display = ft.Stack()
            display.controls.extend(self.para_data)
            self.content.controls[1] = ft.Container(height=self.offset_height, width=self.offset1, bgcolor=self.color)
            self.content.controls[0] = ft.Container(height=self.top_part, width=self.block_width, bgcolor=self.color,
                         content=display,border_radius=ft.border_radius.only(top_left=4,top_right=4,bottom_right=4))
            self.content.controls[2] = ft.Container(height=self.bot_part, width=self.block_width, bgcolor=self.color,border_radius=ft.border_radius.only(bottom_left=4,top_right=4,bottom_right=4))

        try:
            self.content.content.update()
        except:
            pass
        try:
            self.content.controls[0].update()
        except:
            pass
    def set_size_para(self,item,slot):
        self.arg_buffer[slot].height = item.block_height*self.scale-1
        self.arg_buffer[slot].width = item.block_width*self.scale-1+self.parameter_buffer[slot].get_side_block_wid()
        try:
            self.content.content.update()
        except:
            try:
                self.content.controls[0].update()
            except:
                pass

    def get_max_height(self):
        max_hei = 30*self.scale
        for n,item in enumerate(self.parameter_buffer):
            if item != None and item!=self:
                max_hei = max(max_hei, item.get_max_height())
                max_hei = max(max_hei, item.block_height)
            elif item == self:
                self.parameter_buffer[n] = None
        return max_hei
    def get_max_width(self):
        wid = self.para_data[-1].left+self.para_data[-1].width+10
        return wid
    def args_manage(self):
        if self.args:
            if self.parameter_buffer[-1] or self.arg_buffer[-1].content.value:
                para_wid = 30 *self.scale # default
                para_hei = 20 *self.scale # default
                self.Npara += 1
                self.parameter_buffer.append(None)
                content_text_field = ft.TextField(width=para_wid, text_size=15, dense=False, bgcolor=ft.colors.WHITE,
                                                  cursor_height=para_hei - 3,
                                                  content_padding=ft.padding.only(top=-4, left=3, right=3),
                                                  on_change=self.on_change)
                para_block = ft.Container(bgcolor="", width=para_wid, height=para_hei, content=content_text_field,top=0,left=0)
                self.para_data.append(para_block)
                self.data.append(("para",None))
                self.arg_buffer.append(para_block)
                self.content.content.controls.append(para_block)
                self.posion_manage(self.data, self.para_data)
            elif self.Npara>1 and (not self.arg_buffer[-2].content.value and not self.parameter_buffer[-2]):

                self.Npara = max(1,self.Npara)-1
                self.style.pop()
                self.parameter_buffer.pop()
                self.para_data.pop()
                self.arg_buffer.pop()
                self.content.content.controls.pop()


    def size_manage(self):
        for item in self.parameter_buffer:
            if item:
                if self.IsContainer:
                    self.top_part = self.get_max_height()+10
                    self.reset_height()
                else:
                    self.block_height = self.get_max_height()+10
                    self.height = self.block_height
        self.args_manage()
        self.posion_manage(self.data, self.para_data)
        temp = self.get_max_width()

        self.block_width = max(self.block_width,temp)
        self.width = self.block_width
        if self.upper_code and self.upper_code.HaveParameter and self in self.upper_code.parameter_buffer:
            self.upper_code.set_size_para(self, self.upper_code.parameter_buffer.index(self))
            self.upper_code.size_manage()
            self.upper_code.place_block()


        self.reset_height()
        self.place_block()
        self.content_update()

    def reset_para_size(self):
        for n,item in enumerate(self.parameter_buffer):
            if not item and not isinstance(self.arg_buffer[n].content,ft.Icon):
                if not self.arg_buffer[n].content.value:
                    self.arg_buffer[n].width = 30
                    self.arg_buffer[n].height = 20
        if self.IsContainer:
            self.top_part = self.get_max_height()
            self.reset_height()

        else:
            self.height = self.get_max_height()
            self.block_height = self.height

        self.args_manage()
        self.posion_manage(self.data, self.para_data)
        self.width = max(0,self.get_max_width())
        self.block_width = self.width


        if self.upper_code:
            try:
                self.upper_code.set_size_para(self, self.upper_code.parameter_buffer.index(self))
            except:
                pass
            self.upper_code.reset_para_size()
        if self.hook:
            self.hook.reset_para_size()
        self.reset_height()
        self.size_manage()
        self.content_update()
        pass

    def add_to_contain(self,target):
        self.contain.append(target)
        target.upper_code = self
        self.offset_height += target.block_height
        for target_below_code in target.below_code:
            target_below_code.upper_code = self
            self.contain.append(target_below_code)
            self.offset_height+=target.block_height
        target.below_code = []
        self.reset_height() #replace with function
        self.content_update()
        self.place_block()
        self.class_update()

    def add_to_below(self,target):
        self.below_code.append(target)
        target.upper_code = self
        for target_below_code in target.below_code:
            target_below_code.upper_code = self
            self.below_code.append(target_below_code)
        target.below_code = []
        self.content_update()
        self.place_block()

    def place_block(self):
        top_val = self.top
        left_val = self.left
        if self.IsContainer:
            y_change = self.top_part
            x_change = self.offset1
            for item in self.contain:
                item.top = y_change+top_val
                item.left = left_val + x_change
                item.place_block()
                y_change +=item.block_height
        y_change = self.block_height
        x_change = 0
        for item in self.below_code:
            item.top = y_change+top_val
            item.left = left_val+x_change
            item.place_block()
            y_change += item.block_height
        if self.HaveParameter and self.parameter_buffer:
            for para in self.parameter_buffer:
                if para:
                    index = self.parameter_buffer.index(para)
                    para.top = self.arg_buffer[index].top+self.top
                    para.left = self.arg_buffer[index].left + self.left
                    para.place_block()

                    self.posion_manage(self.data,self.para_data)
        if self.side_block:
            self.side_block.top = self.top
            self.side_block.left = self.left+self.block_width+1
            self.side_block.place_block()

    def code_parser(self,level=1):
        parsed_code = ""
        n_para = 0
        struct = iter(self.struct)

        for pack_data in struct:
            kw,data = pack_data

            if kw == "code":
                parsed_code +=data
            elif kw == "bracket":
                parsed_code+=data
            elif kw == "arg":
                if isinstance(data,list):

                    _,adsb = next(struct)
                    for narg,data in enumerate(self.parameter_buffer):
                        if data:
                            parsed_code+=data.code_parser()
                            parsed_code+=adsb
                        elif self.arg_buffer[narg].content.value:
                            parsed_code+=str(text_tranform(check_type(self.arg_buffer[narg].content.value)))
                            parsed_code+=adsb
                    if parsed_code.endswith(adsb):
                        parsed_code = parsed_code[:-1]
                else:

                    if self.parameter_buffer[n_para]:
                        value = self.parameter_buffer[n_para].code_parser()
                        parsed_code += value
                    else:
                        value = self.arg_buffer[n_para].content.value
                        parsed_code += str(check_type(value))
                    n_para+=1
                pass
            elif kw == "adsb":
                parsed_code+=data
                pass
            elif kw == "end":
                parsed_code+=data
                pass
            elif kw == "name":
                parsed_code+=self.name
            elif kw == "def_val" and data:
                if self.upper_code and self.upper_code.IsContainer:
                    parsed_code += " = "+str(check_type(data))
            else:
                parsed_code +=""
                pass
        if self.side_block:
            parsed_code += self.side_block.code_parser()
        for item in self.contain:
            parsed_code+='\n'+"    "*level+item.code_parser(level+1)
        return parsed_code

    def read_data(self,data):
        #unpack
        npara,para_data,self_data = data

        self.Npara = npara
        self.template = self_data
        self.load_template()
        self.data = self.style
        self.para_data = self.load_para(self.data)
        self.posion_manage(self.data,self.para_data)
        self.arg_buffer = [item for item in self.para_data if isinstance(item,ft.Container)]
        self.block_width = max(self.block_width,self.get_row_wid(self.para_data))
        for item in self.parameter_buffer:
            if item and item in self.code_container.controls:
                self.code_container.controls.remove(item)
        self.parameter_buffer = [None]*npara
        for n,item in enumerate(para_data):
            if item['block type'] == 'variable':
                name = item['style'][0][1]
            else:
                name = ""

            new_block = block(x=0, y=0, code_container=self.code_container,
                            struct=item,name=name)
            self.code_container.controls.append(new_block)

            self.add_to_para(new_block,n)
        cf.get_data(self.template,self) #don't ask why
        if self.block_setting:
            lCFb.add_to_buffer(self.template,self.block_setting[0])
        if self.upper_code and self.upper_code.block_name == "class":
            gc.update_class(self.upper_code)
        self.size_manage()
        self.reset_para_size()
        self.content_update()

    def hidecontent(self):
        if not self.hide_content:
            self.content_hide = self.content
            self.content = None
            self.hide_content = True
        return self.content_hide

    def showcontent(self):

        if self.hide_content:

            self.content = self.content_hide
            self.content_hide = None
            self.hide_content = False

    def class_update(self):
        try:
            if self.block_name == 'class':
                if not self.class_id:
                    self.class_id = rq.generate_random_string(10)
                    #create class in class manage

                if not self.func_buffer:
                    self.func_buffer = []

                remove_list = []
                for item in self.func_buffer:
                    if item not in self.contain:
                        self.func_buffer.remove(item)
                        remove_list.append(item)


                for item in self.contain:
                    if item.block_name == "def" and item not in self.func_buffer:
                        self.func_buffer.append(item)

                if self.name:
                    gc.update_class(self,remove_list)
                    pass
        except:
            pass

    def class_name_update(self):
        gc.update_class_name(self)
        #print(self.func_buffer)
