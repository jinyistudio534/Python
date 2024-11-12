import flet as ft
import generator
import os


captcha_code=generator.captcha()

text_field=ft.TextField(
    "type here",
    color="black",
    border="underline",
    cursor_color="black",
    focused_border_color="black"
)

image_field=ft.Image(
    src=f'assets/{captcha_code}.png',                                                                           
)

def check(e):
    global captcha_code
    print(text_field.value==captcha_code)

def refresh(e):
    global captcha_code
    os.remove(f'{captcha_code}.png')
    captcha_code=generator.captcha()    
    image_field.src=f'assets/{captcha_code}.png'
    image_field.update()
    print(captcha_code)

class CaptchaControl():
    def __init__(self):
        self.body=ft.Container(
            content=ft.Column([
                ft.Text("Captcha",
                    size=22,
                    color="black",
                    weight="700",
                    font_family="consolas",
                ),
                ft.Row([
                    image_field,
                    ft.Container(
                        ft.Image(
                            src='assets/refresh.png',                                                                           
                        ),
                        width=48,
                        height=48,  
                        bgcolor="#7f69fa",
                        padding=10,
                        border_radius=12,
                        on_click= refresh
                    )
                ],alignment="center"),
                text_field,
                ft.ElevatedButton(
                    "submit captcha",
                    bgcolor="#7f69fa",
                    color="white",
                    height=50,
                    width=300,
                    on_click=check

                ),
            ],horizontal_alignment="center"),
            width=400,
            height=400,
            bgcolor="white",
            padding=20,
        )

    def build(self):
        return self.body
    
captcha_field=CaptchaControl()
Body=ft.Container(  
    captcha_field.build()
   
    
)

def main(page: ft.Page):
    page.padding=0
    page.window.max_width=680
    page.window.min_height=600
    page.window.resizable=False
    page.bgcolor="#7f69fa"
    page.window.bgcolor="#7f69fa"
    page.horizontal_alignment="center"
    page.vertical_alignment="center"
    page.add(
        Body
    )

ft.app(target=main)