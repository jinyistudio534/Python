import flet as ft

def main(page: ft.Page):    
    # Define page related settings
    #page.theme_mode = ft.ThemeMode.DARK

    body=ft.Container(
        bgcolor="white10",
        margin=ft.margin.all(30),
        width=200,
        height=200,
        shape=ft.BoxShape("circle"),
        # Define image for profile picture
        image_src="/EasyCAT shield.png",
        image_fit="cover",
        shadow=ft.BoxShadow(
            spread_radius=6,
            blur_radius=20,
            color=ft.colors.with_opacity(0.71, "grey"),
        ),
    )
    page.add(body)


ft.app(target=main, assets_dir="assets")
