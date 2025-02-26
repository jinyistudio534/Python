import  asyncio
import  pysoem
import  time
import  ctypes
import  threading
from    stopwatch import Stopwatch

import  flet as ft
from    datetime import datetime
from    flet_timerparam.flet_timerparam import TimerParam

class OutputPdo(ctypes.Structure):
    _pack_ = 1
    _fields_ =[        
        ('Byte0',ctypes.c_uint8),
        ('Byte1',ctypes.c_uint8),
        ('Byte2',ctypes.c_uint8),
        ('Byte3',ctypes.c_uint8),
        ('Byte4',ctypes.c_uint8),
        ('Byte5',ctypes.c_uint8),
        ('Byte6',ctypes.c_uint8),
        ('Byte7',ctypes.c_uint8),
        ('Byte8',ctypes.c_uint8),
        ('Byte9',ctypes.c_uint8),
        ('Byte10',ctypes.c_uint8),
        ('Byte11',ctypes.c_uint8),
        ('Byte12',ctypes.c_uint8),
        ('Byte13',ctypes.c_uint8),
        ('Byte14',ctypes.c_uint8),
        ('Byte15',ctypes.c_uint8),
        ('Byte16',ctypes.c_uint8),
        ('Byte17',ctypes.c_uint8),
        ('Byte18',ctypes.c_uint8),
        ('Byte19',ctypes.c_uint8),
        ('Byte20',ctypes.c_uint8),
        ('Byte21',ctypes.c_uint8),
        ('Byte22',ctypes.c_uint8),
        ('Byte23',ctypes.c_uint8),
        ('Byte24',ctypes.c_uint8),
        ('Byte25',ctypes.c_uint8),
        ('Byte26',ctypes.c_uint8),
        ('Byte27',ctypes.c_uint8),
        ('Byte28',ctypes.c_uint8),
        ('Byte29',ctypes.c_uint8),
        ('Byte30',ctypes.c_uint8),
        ('Byte31',ctypes.c_uint8)
        
    ]

class InputPdo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Byte0',ctypes.c_uint8),
        ('Byte1',ctypes.c_uint8),
        ('Byte2',ctypes.c_uint8),
        ('Byte3',ctypes.c_uint8),
        ('Byte4',ctypes.c_uint8),
        ('Byte5',ctypes.c_uint8),
        ('Byte6',ctypes.c_uint8),
        ('Byte7',ctypes.c_uint8),
        ('Byte8',ctypes.c_uint8),
        ('Byte9',ctypes.c_uint8),
        ('Byte10',ctypes.c_uint8),
        ('Byte11',ctypes.c_uint8),
        ('Byte12',ctypes.c_uint8),
        ('Byte13',ctypes.c_uint8),
        ('Byte14',ctypes.c_uint8),
        ('Byte15',ctypes.c_uint8),
        ('Byte16',ctypes.c_uint8),
        ('Byte17',ctypes.c_uint8),
        ('Byte18',ctypes.c_uint8),
        ('Byte19',ctypes.c_uint8),
        ('Byte20',ctypes.c_uint8),
        ('Byte21',ctypes.c_uint8),
        ('Byte22',ctypes.c_uint8),
        ('Byte23',ctypes.c_uint8),
        ('Byte24',ctypes.c_uint8),
        ('Byte25',ctypes.c_uint8),
        ('Byte26',ctypes.c_uint8),
        ('Byte27',ctypes.c_uint8),
        ('Byte28',ctypes.c_uint8),
        ('Byte29',ctypes.c_uint8),
        ('Byte30',ctypes.c_uint8),
        ('Byte31',ctypes.c_uint8)
    ]

def convert_input_data(data):
    return InputPdo.from_buffer_copy(data)

# I use this config function
def peasycat_config_func(slave_pos):
    global easycat
    # all default config

output_data = OutputPdo() 
input_data = InputPdo()
master = pysoem.Master()
easycat = None

def worker(event,data):
    global easycat
    state=-1
    def Scan():
        if master.config_init() > 0:
            for i, slave in enumerate(master.slaves):
                print("{} ({}) {}".format(slave.man,f'0x{slave.id:X}', slave.name))

            easycat = master.slaves[0]
        
            easycat.config_func = peasycat_config_func
            master.config_map()

            return len(master.slaves)
        else:
            print('no device found')
            return -1
        
    def ProcessData(id=0, sampling_time=0.01):
        global input_data,output_data

        easycat = master.slaves[id]
        if master.state_check(pysoem.SAFEOP_STATE, 50_000) == pysoem.SAFEOP_STATE:
            master.state = pysoem.OP_STATE
            
            master.send_processdata()
            master.receive_processdata(1_000)           
            master.write_state()
            master.state_check(pysoem.OP_STATE, 5_000_000)
            if master.state == pysoem.OP_STATE:
                print('IN OP STATE')
                stopwatch = Stopwatch(0.5)
                stopwatch.reset()                
                c1 = 0                            
                try:
                    data['connected'] = True
                    while 1:                      
                        easycat.output = bytes(output_data)
                        master.send_processdata()
                        master.receive_processdata(1_000)                        
                        input_data = convert_input_data(easycat.input)                      
                        time.sleep(sampling_time)
                        if event.is_set():                                                       
                            break
                        # print('Input :', input_data.Byte0, input_data.Byte1, input_data.Byte2, input_data.Byte3, input_data.Byte4, input_data.Byte5,' Output:', output_data.Byte0, output_data.Byte1, output_data.Byte2, output_data.Byte3, output_data.Byte4, output_data.Byte5)                                                                  

                except KeyboardInterrupt:
                    print('stopped')
                    del(data['connected'])
                    return -1
                # zero everything
                easycat.output = bytes(len(easycat.output))
                master.send_processdata()
                master.receive_processdata(1_000)
                print('thread end')
                del(data['connected'])

                return 0
            else:
                print('al status code {} ({})'.format(hex(easycat.al_status), pysoem.al_status_code_to_string(easycat.al_status)))
                print('failed to got to op state')
                del(data['connected'])

                return -2

    master.open('\\Device\\NPF_{A49DCDDE-F083-4985-A824-45BFBE483E3C}') 
    # master.open('eth0')
    time.sleep(1)     
    try:
        while True:
            if event.is_set():
                event.clear()
                if data['scan'] == 999:                                         
                    data['scan'] = Scan()
                    print('Scanning ... {}'.format(data['scan']))

                elif data['slave'] in range(0,255):
                    print('ProcessData ... {}'.format(data['slave']))
                    ProcessData(data['slave'])
                    data['slave'] = 999
                
            time.sleep(0.01)

    except KeyboardInterrupt:
        print('stopped')    

    # zero everything
    #easycat.output = bytes(len(easycat.output))
    master.send_processdata()
    master.receive_processdata(1_000) 
    master.close()

# Shared data:
shared_data = {}
soem_event = threading.Event()

task = threading.Thread(target=worker,args=(soem_event, shared_data))
task.daemon = True
task.start()



act_id = -1
act_name = ""
def main(page: ft.Page):  
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else "red"
        e.control.update()

    def on_click_slave(e,id): 
        global act_id,act_name
        act_id = id
        act_name = e.control.content.controls[1].controls[1].value
        print("slave id:{0} name:{1}".format(act_id,act_name))       

        shared_data['slave'] = act_id
        soem_event.set()

        page.go("/slave")

    async def check_scan():               
        print('check_scan')
        while 1:
            if soem_event.is_set():                                
                await asyncio.sleep(0.1)
            else:
                print('scanned')
                n1 = shared_data['scan']
                if n1!=999:
                    page.controls.clear()
                    if n1>0:
                        for i, slave in enumerate(master.slaves): 
                            _Container = ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Image(
                                            src=f"easycat_shield.png",
                                            width=81,
                                            height=81,
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text("{}".format(f'0x{slave.id:X}')),
                                                ft.Text("{}".format(slave.name)),
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                ),                                   
                                padding=5, 
                                on_hover=on_hover,
                                on_click=lambda e,index=i: on_click_slave(e,index),                                                                                                                                
                            )                       

                            item = ft.Card(content = _Container,)     
                            page.controls.append(item) #ft.Text("{} {} {}".format(slave.man,f'0x{slave.id:X}', slave.name)))
                            
                            page.controls.append(
                                ft.Container(
                                    content = ft.Text("Have {} slave in the bus".format(len(master.slaves))),  
                                    alignment=ft.alignment.center_right,                         
                                )
                            )       
                    
                    break              
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.update()    

    def route_change(e):
        global act_id,act_name,master

        print(f"Route changed to {e.route}")
        #page.views.clear()
        if page.route == "/slave":                     
            #page.views.append(  
            if act_id>=0:      
                easycat = master.slaves[act_id]        
                page.controls=[  
                    ft.Card(
                        content=ft.Row([
                            ft.Image(
                                src=f"easycat_shield.png",
                            ),
                            ft.Column([
                                ft.Text("Slave ID:"),
                                ft.Text(f'0x{easycat.id:X}',color="blue",weight=ft.FontWeight.BOLD),
                            ],expand=True)
                        ]),                                              
                    ),             
                    ft.Column(
                    [
                        ft.DataTable(
                            border=ft.border.all(1, "blue"),
                            data_row_max_height=48,
                            vertical_lines=ft.BorderSide(1, "blue"),
                            horizontal_lines=ft.BorderSide(1, "blue"),                                                                   
                            columns=[
                                ft.DataColumn(ft.Text(value="Key",text_align=ft.TextAlign.RIGHT,expand=1)),
                                ft.DataColumn(ft.Text("Input")),
                                ft.DataColumn(ft.Text("Output")),
                            ],
                            rows=rows,
                        ) 
                    ],expand=True,scroll=ft.ScrollMode.ALWAYS),                
                    TimerParam(name="timer", interval_s=0.01, callback=refresh, args=(soem_event,shared_data)),
                ]        
            else:
                page.controls=[ft.Text("No slave selected",color="red",weight=ft.FontWeight.BOLD)]

            page.update()
        elif page.route == "/scan":    
            act_id = -1
            act_name = ""

            page.horizontal_alignment = ft.MainAxisAlignment.CENTER
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.controls=[ 
                ft.Container(
                    content=ft.Text("Slave scanning ..."),                    
                    alignment=ft.alignment.center,
                )
            ]
            page.update()   

            shared_data['scan'] = 999 
            soem_event.set()

            page.run_task(check_scan)

        elif page.route == "/about":
            #page.horizontal_alignment = ft.MainAxisAlignment.CENTER
            page.vertical_alignment = ft.MainAxisAlignment.CENTER

            def on_hover(e):
                e.control.bgcolor = "blue" if e.data == "true" else "red"
                e.control.update()

            images = ft.Row(                               
                controls=[
                    ft.Image(
                        src=f"easycat_shield.png",
                        fit=ft.ImageFit.NONE,   
                        width=120,
                        height=120,    
                        tooltip="EasyCAT Shield",                                                           
                    ),
                    ft.Image(
                        src=f"easycat_hat.png",
                        fit=ft.ImageFit.NONE,    
                        width=150,
                        height=150,                       
                        tooltip="EasyCAT Hat",
                    ),
                    ft.Image(
                        src=f"easycat_gateway.png",
                        fit=ft.ImageFit.NONE,                        
                        width=150,
                        height=150,   
                        tooltip="EasyCAT Gateway",
                    ),
                    ft.Image(
                        src=f"easycat_pro.png",
                        fit=ft.ImageFit.NONE,                       
                        width=150,
                        height=150,   
                        tooltip="EasyCAT Pro",
                    ),
                ],wrap=False, scroll="always",
            )
            
            _column=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="ethercat.png",                                
                            ),alignment=ft.alignment.center,
                        )
                        ,  
                        images,     
                        ft.Container(
                            content=ft.Image(
                                src="easycat.png",
                            ),alignment=ft.alignment.center,
                        )
                    ],
                    spacing=10,                                                                  
                ),                    
                alignment=ft.alignment.center,
            )
            
            page.controls=[ 
                _column,                         
            ]
            page.update()
    


    def _on_press(e):
        match e.control.selected_index:
            case 0:
                page.go("/scan")
            case 1:
                page.go("/slave")
            case 2:
                page.go("/about")

    def do_submit(e,id):  
        global output_data       
        if e.control.value.isdigit():                  
            n1 = int(e.control.value)
            if n1>=0 and n1<=255:
                print("id:{0}  value:{1}".format(id,e.control.value)) 
                setattr(output_data, f'Byte{id}', int(e.control.value))
            else:
                print("number out of range")
                e.control.value = '0'
        else:
            print("valid digit")  
            e.control.value = '0'          
        
        page.update()    
    
    inputs     = {}
    outputs    = {}
    rows=[]
    for i in range(32):
        inputs['Byte'+str(i)]=ft.Text("0",text_align=ft.TextAlign.RIGHT,expand=1)
        outputs['Byte'+str(i)]=ft.TextField(content_padding=ft.padding.symmetric(vertical=-13,horizontal=3),text_size=16,width=80,height=32,border=ft.InputBorder.NONE,filled=True, focused_bgcolor=ft.Colors.AMBER_100,on_submit=lambda e, i=i: do_submit(e,i))
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Row([ft.Text("Byte"+str(i),text_align=ft.TextAlign.CENTER,expand=1)])),
                    ft.DataCell(ft.Row([inputs['Byte'+str(i)]])),
                    ft.DataCell(outputs['Byte'+str(i)])
                ]
            )
        )
    
    
    def refresh(event,data):                     
        global input_data
        
        if 'connected' in shared_data:
            for i in range(0, 32):               
                b1 = getattr(input_data,'Byte'+str(i))
                if inputs['Byte'+str(i)].value != str(b1):
                    inputs['Byte'+str(i)].value = str(b1)
                    inputs['Byte'+str(i)].update()
         
    page.title = "NavigationBar Example"
    page.navigation_bar = ft.NavigationBar(
        on_change=_on_press,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Scan"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Slave"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="About",
            ),
            
        ]
    )   
    page.window_width=400
    page.resizable = False
    page.auto_update = True
    #page.scrollable = True
    page.title = "EasyNavigator V2.0 "
    page.on_route_change = route_change
    page.go('/scan')


ft.app(target=main)
