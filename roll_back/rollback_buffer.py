import setting

def save_state(buffer,stack):
    buffer.append(stack.controls)

class rollback_buffer():
    def __init__(self,len=setting.roll_back_len):
        super().__init__()
        self.length = len
        self.data = []
        self.current_pointer = 0

    def add(self, object):
        if len(self.data) >= self.length:
            self.data.pop(0)
            self.data.append(object)
            print("add new2")
        else:
            self.data.append(object)
            print("add new")
        print(self.data)

    def resize(self,size):
        self.length = size
        if len(self.data) >size:
            self.data = self.data[len(self.data)-size:]

    def size(self):
        return self.lenght

    def get_current_pointer(self):
        return self.current_pointer

    def get_content(self):
        if self.data:
            return self.data[self.current_pointer-1]
        return None

    def undo(self):
        if self.current_pointer>0:
            self.current_pointer -=1

    def redo(self):
        if self.current_pointer < len(self.data):
            self.current_pointer +=1

    def add_content(self,content):
        self.data = self.data[:self.current_pointer]
        self.add(content)
        self.current_pointer = max(0,len(self.data))
        print(self.current_pointer)



