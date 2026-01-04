import time

import flet as ft
import vertical_tab.vertical_tab as vt
import console.console_UI as c
from utility.color_palette import *
import time as t



def main(page: ft.Page):
    page.window_maximized = False
    page.add()
    page.update()

if __name__ == "__main__":
    ft.app(target=main)