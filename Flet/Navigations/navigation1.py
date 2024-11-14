import flet as ft

def main(page:ft.Page):
    page.bgcolor="#8ab9eb"
    page.theme_mode="dark"
    page.title="Navigations"
    page.window.width=450
    page.window.height=700
    page.window.maximizable=False
    page.horizontal_alignment="center"
    page.vertical_alignment="center"

    def btn_edit(e):
        _stack_main.controls.clear()
        _stack_main.update()
        _stack_main.controls.append(_edit)
        _stack_main.update()

    def btn_config(e):
        _stack_main.controls.clear()
        _stack_main.update()
        _stack_main.controls.append(_config)
        _stack_main.update()

    def btn_search(e):
        _stack_main.controls.clear()
        _stack_main.update()
        _stack_main.controls.append(_search)
        _stack_main.update()

    def btn_favorite(e):
        _stack_main.controls.clear()
        _stack_main.update()
        _stack_main.controls.append(_favorite)
        _stack_main.update()

    def btn_toshare(e):
        _stack_main.controls.clear()
        _stack_main.update()
        _stack_main.controls.append(_toshare)
        _stack_main.update()


    page.floating_action_button=ft.FloatingActionButton(
        icon=ft.icons.ADD,
        bgcolor="blue",
        on_click=btn_toshare
    )
    page.floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor="#f6f6f6ff",
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.EDIT,icon_color="blue",icon_size=24,on_click=btn_edit),
                ft.IconButton(icon=ft.icons.SEARCH,icon_color="blue",icon_size=24,on_click=btn_search),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS,icon_color="blue",icon_size=24,on_click=btn_config),
                ft.IconButton(icon=ft.icons.FAVORITE,icon_color="blue",icon_size=24,on_click=btn_favorite),
            ]
        )
    )

    _main=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="Start",
            color='black',
            size=32,
        )
    )

    _edit=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="Edit",
            color='black',
            size=32,
        )
    )

    _search=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="Search",
            color='black',
            size=32,
        )
    )

    _config=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="Config",
            color='black',
            size=32,
        )
    )

    _favorite=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="Favorite",
            color='black',
            size=32,
        )
    )

    _toshare=ft.Container(
        width=400,
        height=550,
        bgcolor="#f6f6f6ff",
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=8,color=ft.colors.with_opacity(0.4,'black')),
        content=ft.Text(
            value="to share",
            color='black',
            size=32,
        )
    )


    _stack_main=ft.Stack(
        alignment=ft.alignment.center,
        controls=[
            _main,
        ]
    )

    

    page.add(_stack_main)



ft.app(target=main)