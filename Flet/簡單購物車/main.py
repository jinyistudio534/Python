import flet as ft

products=[
    {
        'item_name': 'EasyCAT Shield',
        'item_spec': 'For Arduino uno gpio',
        'item_src': 'easyCAT_Shield.png',
        'item_quantity': 1,
        'item_bought': False,
    },
    {
        'item_name': 'EasyCAT Hat',
        'item_spec': 'For Raspberry PI gpio',
        'item_src': 'easyCAT_Hat.png',
        'item_quantity': 1,
        'item_bought': False,
    },
    {
        'item_name': 'EasyCAT Gateway',
        'item_spec': 'Ethernet/VCOM',
        'item_src': 'easyCAT_gateway.png',
        'item_quantity': 1,
        'item_bought': False,
    },
    {
        'item_name': 'EasyCAT PRO',
        'item_spec': 'spi interface',
        'item_src': 'easyCAT_Shield.png',
        'item_quantity': 1,
        'item_bought': False,
    },    
]

class Product(ft.Row):
    def __init__(self, item_name, item_spec,item_src,item_quantity=1, item_bought = False):
        super().__init__()       
        self.bought = item_bought
        self.item_name = item_name
        self.item_spec = item_spec
        self.item_src = item_src               
        self.bought_item = ft.Checkbox(value=False, label="", on_change = self.bought_changed)
        self.quantity = ft.TextField(read_only=True,border_radius=ft.border_radius.all(8), value=item_quantity, text_align= "right", width = 60,height=48, input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$",replacement_string=""))
        self.expand= True
        self.spacing=3
        self.controls = [ 
            self.bought_item,           
            ft.Image(src=self.item_src, width=90, height=90),
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Text(self.item_name),
                    ft.Text(self.item_spec),
                ]
            ),
            ft.IconButton(
                icon=ft.Icons.EXPOSURE_PLUS_1, 
                on_click = self.plus_clicked, 
                data=0
            ),
            self.quantity,                            
            ft.IconButton(
                icon=ft.Icons.EXPOSURE_MINUS_1, 
                on_click = self.minus_clicked, 
                data=0
            ),
        ]                          
        
 
    def bought_changed(self, e):
        self.bought = self.bought_item.value
        #self.item_bought_change()
    

    def minus_clicked(self, e):
        if int(self.quantity.value) > 1:
            self.quantity.value = str(int(self.quantity.value)-1)
            self.quantity.border_color=ft.Colors.BLACK
            self.quantity.border_width=1
        else:
            self.quantity.border_color=ft.Colors.RED
            self.quantity.border_width=2
        self.quantity.update()

    def plus_clicked(self, e):
        self.quantity.value = str(int(self.quantity.value)+1)
        if (self.quantity.border_width if self.quantity.border_width is not None else 1)>1:
            self.quantity.border_color=ft.Colors.BLACK
            self.quantity.border_width=1
        self.quantity.update()


def main(page: ft.Page):
    def button_clicked(e):  
        print('hello')
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files()
    

        

    page.title= "Shopping App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window.width = 500

    rows=[]
    for product in products:
        rows.append(Product(product['item_name'], product['item_spec'],product['item_src'])) 

    text = ft.Text(f"Valid: False")        

    page.add(
        ft.Text("Shopping List",size=24,weight=ft.FontWeight.W_600,text_align=ft.TextAlign.CENTER,expand=1),
        ft.Divider(),
        ft.Column(
            controls=rows,
            expand=1
        ),       
        ft.Divider(),
        
    )



ft.app(main)