# Importando as bibliotecas
import flet as ft
import asyncio
from datetime import datetime

# Função principal dp flet
def main(page: ft.Page):
    page.fonts = {
        "Montserrat": "assets/Montserrat-VariableFont_wght.ttf",  
        "Seven7":"assets/digital-7.ttf",      
    }

    page.window.width = 350
    page.window.height = 600
    page.bgcolor = ft.colors.BLUE

    # função para actualizar a hora actual
    async def hour():
        while True:
            now = datetime.now()
            hr = now.strftime('%H')
            min = now.strftime('%M')
            sec = now.strftime('%S')

            # pegando o Text com a hora para actualizar
            hora.content.controls[0].value = hr

            # pegando o Text com o minuto para actualizar
            minuto.content.controls[0].value = min

            # pegando o Text com o segundo para actualizar
            segundo.content.controls[0].value = sec
            page.update() # actualizando a página

            await asyncio.sleep(1)

    # container com a hora, minuto e segundos
    class Clock(ft.Container):
        def __init__(
            self,
            value: str,
            text: str
        ):
            super().__init__()
            # o col só funciona quando o control é inserido dentro de uma responsiverow.
            self.col = {'xs': 4}
            self.height = page.width * 0.09
            self.border= ft.border.all(
                width=1,
                color=ft.colors.GREEN
            )
            self.border_radius=10
            self.shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=1,
                offset=ft.Offset(0, 0),
                color=ft.colors.with_opacity(0.08, 'black'),
                blur_style=ft.ShadowBlurStyle.SOLID
            )
            self.content=ft.Column(
                controls=[
                    ft.Text(
                        value=value,                        
                        size=48,
                        color=ft.colors.YELLOW,
                        font_family='Seven7'
                    ),
                    ft.Text(
                        value=text,
                        color=ft.colors.with_opacity(0.8, 'black'),
                        weight='bold',
                        size=15,
                        font_family='Montserrat'
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            )
            self.bgcolor=ft.colors.with_opacity(0.6, 'green')
            self.alignment=ft.alignment.center
    
    # responsiverow com os tres containers criados usando o clock
    clocks = ft.ResponsiveRow(
        controls=[
            hora := Clock(value='23', text='Hour'),
            minuto := Clock(value='05', text='Minutes'),
            segundo := Clock(value='16', text='Seconds')
        ],
        width=page.width,
        height=page.window.height,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(clocks) # adicionado a responsiverow na página
    asyncio.run(hour()) # Actualizado os containers com as horas actuais

if __name__ == '__main__':
    ft.app(target=main)