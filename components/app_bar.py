import flet as ft


def NavBar(page):
    NavBar = ft.AppBar(
        title=ft.Text("Flet Example"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.Icons.HOME, on_click=lambda e: page.go("/")),
            ft.IconButton(
                ft.Icons.SETTINGS_ROUNDED, on_click=lambda e: page.go("/settings")
            ),
            ft.PopupMenuButton(
                icon=ft.Icons.FACE,
                
                items=[
                    ft.PopupMenuItem(
                        text="Profile",
                        icon=ft.Icons.INFO_OUTLINE_ROUNDED,
                        on_click=lambda e: page.go('/profile')
                    ),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Logout",
                        icon=ft.Icons.LOGOUT,
                        checked=False,
                        on_click=lambda e: page.go('/logout') 
                    ),
                ]
            ),
        ],
    )

    return NavBar

def Info_SnackBar(text):
    return ft.SnackBar(content=ft.Text(text),bgcolor=ft.Colors.GREEN)

def Error_SnackBar(text):
    return ft.SnackBar(content=ft.Text(text,color=ft.Colors.WHITE),bgcolor=ft.Colors.RED)

def Warn_SnackBar(text):
    return ft.SnackBar(content=ft.Text(text,color=ft.Colors.RED),bgcolor=ft.Colors.YELLOW)
