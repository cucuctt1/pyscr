import flet
from flet import (
    Page,
    UserControl,
    Row,
    VerticalDivider,
    Container,
)
from navrail import (
    NavRail,
    BlockDisplay,
)


class TagOfLists(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return Container(
            content=NavRail(),
        )


class ListOfBlocks(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return Container(
            content=BlockDisplay(),
        )


def main(page: Page):
    page.title = "Phake Scratch"
    page.window_always_on_top = True
    page.window_width = 700
    page.window_height = 500
    
    page.add(Row(
        expand=True,
        controls=[
            TagOfLists(),
            VerticalDivider(),
            ListOfBlocks(),
            VerticalDivider(),
        ]
    ))

    page.update()


flet.app(
    target=main,
)