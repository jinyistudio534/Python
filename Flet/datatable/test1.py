import flet as ft

def main(page: ft.Page):
    def do_submit(text, i):        
        inputs['Byte'+str(i)].value = text.control.value
        inputs['Byte'+str(i)].update()
        print("Byte"+str(i)+": "+text.control.uid)
    

    inputs={}
    outputs={}
    rows=[]
    for i in range(8):
        inputs['Byte'+str(i)]=ft.Text("0",text_align=ft.TextAlign.RIGHT,expand=1)
        outputs['Byte'+str(i)]=ft.TextField(content_padding=ft.padding.symmetric(vertical=-13,horizontal=3),text_size=16,width=100,height=32,border=ft.InputBorder.NONE,filled=True, focused_bgcolor=ft.Colors.AMBER_100,on_submit=lambda text, i=i: do_submit(text,i))
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Row([ft.Text("Byte"+str(i),text_align=ft.TextAlign.CENTER,expand=1)])),
                    ft.DataCell(ft.Row([inputs['Byte'+str(i)]])),
                    ft.DataCell(outputs['Byte'+str(i)])
                ]
            )
        )
    
    page.add(        
        ft.DataTable(
            border=ft.border.all(2, "blue"),
            data_row_max_height=48,
            vertical_lines=ft.BorderSide(2, "blue"),
            horizontal_lines=ft.BorderSide(2, "blue"),                                       
            width=500,
            columns=[
                ft.DataColumn(ft.Text(value="Key",text_align=ft.TextAlign.RIGHT,expand=1)),
                ft.DataColumn(ft.Text("Input")),
                ft.DataColumn(ft.Text("Output")),
            ],
            rows=rows,
        )
    )

ft.app(target=main)
