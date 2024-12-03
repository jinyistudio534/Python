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
            on_click=lambda e: self.SelectedContainer(e),   #新增click事件
