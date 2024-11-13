import flet as ft



def main(page: ft.Page):
    page.window.width=360
    page.window.height=500

    def youchangechioce(e):
        pass

    mytab = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        unselected_label_color="black",
        label_color="white",
        indicator_color="white",
        indicator_border_radius=30,
        divider_color="#7c59f0",
        scrollable=True,
        on_change=youchangechioce,
        tabs=[
            ft.Tab(
                text="Home",
                icon="home"
            ),
            ft.Tab(
                text="Face",
                icon="face"
            ),
            ft.Tab(
                text="Person",
                icon="person"
            ),
            ft.Tab(
                text="Notifications",
                icon="notification_add"
            ),
        ]
    )
    mybar=ft.Container(
        border_radius=ft.border_radius.vertical(bottom=30),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color="#fc4795",
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#fc4795","#7c59f0"],
        ),
        width=page.window.width,
        height=150,
        padding=10,
        content=ft.Column([
            ft.Row([
                ft.IconButton(icon="menu",
                    icon_size=25,
                    icon_color="white",
                ),
                ft.Text("Flet App",
                    size=25,
                    color="white",
                    weight="bold",
                ),
                ft.Row([
                    ft.IconButton(icon="notifications",
                        icon_size=25,
                        icon_color="white",
                    ),
                    ft.IconButton(icon="search",
                        icon_size=25,
                        icon_color="white",
                    ),
                ])
            ],alignment="spaceBetween"),
            mytab
        ])        
    )
    page.overlay.append(mybar)
    page.add(
        ft.Column([
            ft.Container(
                margin=ft.margin.only(
                    top=page.window.height/2
                ),
                #border=ft.border.only(top=ft.BorderSide(color="black",width=1)),
                #bgcolor="blue",
                alignment=ft.alignment.center,                
                content=ft.Column([
                    ft.Text("Sample",size=30),
                ])
                

            )
        ])
    )


ft.app(target=main)
