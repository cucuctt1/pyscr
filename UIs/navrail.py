import flet

from flet import (
    NavigationRail,
    NavigationRailDestination,
    Container,
    Draggable,
    Column,
    Stack,
    Text,
    icons,
    colors,
)


class NavRailDest(NavigationRailDestination):
    def __init__(self, icon, label):
        super().__init__()

        self.icon = icon
        self.label = label


class NavRail(NavigationRail):
    def __init__(self):
        super().__init__()

        self.selected_index = 0
        self.destinations=[
            NavRailDest(icons.LIGHTBULB, "Logic"),
            NavRailDest(icons.LOOP, "Loops"),
        ]


class BlockContent(Stack):
    def __init__(self):
        super().__init__()

        self.bgcolor = colors.GREEN
        self.controls = [
            Container(bgcolor=colors.GREEN, width=200, height=50),
            Text("Block mẫu"), # Mỗi loại block làm 1 class riêng vì chả cái nào như cái nào
        ]                      # Nhớ dùng image chứ dùng stack để thiết kế block có mà chết cx ko xong <(")


class Block(Draggable):
    def __init__(self):
        super().__init__()

        self.content = BlockContent()



class BlockDisplay(Container):
    def __init__(self):
        super().__init__()

        self.content = Column(
            controls=[
                Block(),
                Block(),
            ]
        )