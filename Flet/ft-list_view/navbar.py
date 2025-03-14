import flet
from flet import *
from functools import partial


class ModernNavBar(UserControl):
    def __init__(self):
        super().__init__()
        self.selected=None    
        self.items:list=[] 
           
                    

    def HighlightContainer(self, e):         
        if self.selected != e.control:
            if e.data == "true":        
                e.control.bgcolor='grey200'
                #e.control.content.controls[0].icon_color = "purple300"
                #e.control.content.controls[1].color = "purple300"
           
                e.control.content.controls[1].color = "black"
                e.control.content.controls[1].weight=FontWeight.W_700
                #e.control.content.controls[1].update()               
            else:
                e.control.bgcolor='white'            
                #e.control.content.controls[0].icon_color = "black"
            
                #e.control.update()
                e.control.content.controls[1].color = "black"
                e.control.content.controls[1].weight=FontWeight.NORMAL
                #e.control.content.controls[1].update()
                
        else:
            e.control.bgcolor='green200'
            
        e.control.update()

    def SelectedContainer(self, e):          
        if self.selected is None:
            self.selected=e.control
        else:
            if self.selected != e.control:
                for item in self.body.content.controls:
                    if self.selected==item:
                        self.selected.bgcolor='white'
                        self.selected.update()
                        break

            self.selected=e.control
            self.selected.bgcolor='green200'
            self.selected.update()                   
        

    def ContainedIcon(self, icon_name, text, data):
        return Container(
            data=data,           
            width=180,
            height=45,
            border_radius=10,            
            on_hover=lambda e: self.HighlightContainer(e),
            on_click=lambda e: self.SelectedContainer(e),
            ink=False,
            content=Row(               
                controls=[
                    IconButton(
                        icon=icon_name,
                        icon_size=21,
                        icon_color="blue",
                        selected=False,                                      
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=7),                            
                            overlay_color=colors.TRANSPARENT,
                        ),
                    ),
                    Text(
                        value=text,
                        color="black",
                        size=11,
                        opacity=1,
                        animate_opacity=200,                        
                    ),
                ],
            ),
        )

    def build(self):
        self.body=Container(
            alignment=alignment.center,
            padding=10,
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(                            
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=5,
                controls=[
                    self.ContainedIcon(icons.HOME_FILLED, "Home", 1),
                    self.ContainedIcon(icons.SEARCH, "Search", None),
                    self.ContainedIcon(icons.DASHBOARD_ROUNDED, "Dashboard", 2),
                    self.ContainedIcon(icons.BAR_CHART, "Revenue", 3),
                    self.ContainedIcon(icons.NOTIFICATIONS, "Notifications", None),
                    self.ContainedIcon(icons.PIE_CHART_ROUNDED, "Analytics", None),
                    self.ContainedIcon(icons.FAVORITE_ROUNDED, "Likes", None),
                    self.ContainedIcon(icons.WALLET_ROUNDED, "Wallet", None),
                    Divider(color="black", height=5),
                    self.ContainedIcon(icons.LOGOUT_ROUNDED, "Logout", None),
                ],
            ),
        )
        return self.body
