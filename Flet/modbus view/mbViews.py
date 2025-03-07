#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

An example of a single threaded synchronous client.

usage: simple_async_client.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio

import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

import  flet as ft
from flet_timer.flet_timer import Timer

async def run_async_simple_client(comm, host, port, framer=FramerType.SOCKET):    
    """Run async client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    print("get client")
    client: ModbusClient.ModbusBaseClient
    if comm == "tcp":
        client = ModbusClient.AsyncModbusTcpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # source_address=("localhost", 0),
        )
    elif comm == "udp":
        client = ModbusClient.AsyncModbusUdpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # source_address=None,
        )
    elif comm == "serial":
        client = ModbusClient.AsyncModbusSerialClient(
            port,
            framer=framer,
            # timeout=10,
            # retries=3,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )
    else:
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    await client.connect()
    # test client is connected
    assert client.connected

    print("get and verify data")
    try:
        # See all calls in client_calls.py
        rr = await client.read_coils(1, count=1, slave=1)
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received exception from device ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
        return
    ct=0
    while True:
        try:
            # See all calls in client_calls.py
            rr = await client.write_register(10, ct, slave=1)
            #rr = await client.read_holding_registers(10, count=2, slave=1)
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            client.close()
            return
        
        if rr.isError():
            print(f"Received exception from device ({rr})")
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            client.close()
            return
        
        await asyncio.sleep(0.5)
        ct += 1
        if ct>100:
            print(f"Write ({ct})")
            break

    value_int32 = client.convert_from_registers(rr.registers, data_type=client.DATATYPE.INT32)
    print(f"Got int32: {value_int32}")
    print("close connection")
    client.close()


from datetime import datetime

def main(page: ft.Page):  
    client: ModbusClient.ModbusBaseClient

    def update_time():
        timer_txt.value = datetime.now().strftime("%H:%M:%S")
        page.update()

    #def StartModbus(e):
    #    page.run_task(run_async_simple_client,"tcp", "192.168.1.19", 502)

    timer = Timer(name='Timer',callback=update_time, interval_s=1)

    timer_txt = ft.Text(
        value='', 
        text_align="center",
        size=24
    )   

    async def mb_open(e):
        global client
        if mb_connect.data<=0:
            mb_connect.data=1
            client = ModbusClient.AsyncModbusTcpClient(
                "192.168.1.19",
                port=502,
                framer=FramerType.SOCKET,
                # timeout=10,
                # retries=3,
                # source_address=("localhost", 0),
            )
            print("connect to server")
            await client.connect()
            # test client is connected
            assert client.connected

            mb_connect.tooltip="Connected"
            mb_connect.data=2
            mb_connect.color="green"  
            mb_connect.update()           
            mb_panel.visible=True
            mb_panel.update()
            mb_view.update()
            await asyncio.sleep(0.1)            
            mb_panel.scale=1
            mb_panel.update()
            print(mb_view.height)

    async def mb_close(e):
        global client
        if mb_connect.data>=1:
            print("close connection")
            client.close()
            mb_connect.tooltip="close"
            mb_connect.data = 0
            mb_connect.color="gray"
            mb_connect.update()
            mb_panel.scale=0
            mb_panel.update()    
            await asyncio.sleep(0.3)          
            mb_panel.visible=False
            page.update()
            print(mb_view.height)

    async def mb_exec(e):
        global client
        print('go')
        print(mb_panel.controls[0].value)
        r1 = mb_panel.controls[0].value
        a1 = int(mb_panel.controls[1].value)
        c1 = int(mb_panel.controls[2].value)
        rows=[]
        if r1 in ['1','2']: #coils
            try:                
                if r1=='1':
                    rr = await client.read_coils(address=a1, count=c1, slave=1)                
                else:
                    rr = await client.read_discrete_inputs(address=a1, count=c1, slave=1)
            except ModbusException as exc:
                print(f"Received ModbusException({exc}) from library")

            if rr.isError():
                print(f"Received exception from device ({rr})")
                # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
               
                return;
            print(rr.bits)            
           
            for i in range(c1):
                #inputs['Byte'+str(i)]=ft.Text("0",text_align=ft.TextAlign.RIGHT,expand=1)
                #outputs['Byte'+str(i)]=ft.TextField(content_padding=ft.padding.symmetric(vertical=-13,horizontal=3),text_size=16,width=100,height=32,border=ft.InputBorder.NONE,filled=True, focused_bgcolor=ft.Colors.AMBER_100,on_submit=lambda text, i=i: do_submit(text,i))
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Text(str(a1+i))
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Text(str(rr.bits[i]))
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ),                           
                        ]
                )
            )

        else:
            try:                
                if r1=='3': # holding
                    rr = await client.read_holding_registers(address=a1, count=c1, slave=1)                
                else:
                    rr = await client.read_input_registers(address=a1, count=c1, slave=1) 

            except ModbusException as exc:
                print(f"Received ModbusException({exc}) from library")
       
            if rr.isError():
                print(f"Received exception from device ({rr})")
                # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message                    
            
            print(rr.registers)
            for i in range(c1):
                #inputs['Byte'+str(i)]=ft.Text("0",text_align=ft.TextAlign.RIGHT,expand=1)
                #outputs['Byte'+str(i)]=ft.TextField(content_padding=ft.padding.symmetric(vertical=-13,horizontal=3),text_size=16,width=100,height=32,border=ft.InputBorder.NONE,filled=True, focused_bgcolor=ft.Colors.AMBER_100,on_submit=lambda text, i=i: do_submit(text,i))
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Text(str(a1+i))
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Text(str(rr.registers[i]))
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ),                           
                        ],
                        
                    )
                )
        #------------------
        # List data table
        #------------------
        ls = mb_view.content.controls 
        ls.clear()        
        dt = ft.DataTable(
            border=ft.border.all(1, "blue"),            
            heading_row_height=32,
            data_row_min_height=32,
            data_row_max_height=32,
            column_spacing=100,
            vertical_lines=ft.BorderSide(1, "blue"),
            horizontal_lines=ft.BorderSide(1, "blue"),                                       
            expand=1,
            columns=[
                ft.DataColumn(ft.Text(value="Address"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Value",expand=1),heading_row_alignment=ft.MainAxisAlignment.CENTER),               
            ],
            rows=rows,
        )
        ls.append(dt)
        mb_view.update()
                    
    mb_panel=ft.Row(
        [
            ft.DropdownM2(
                label="Register",
                value='3',
                options=[
                    ft.dropdownm2.Option(text="Coil",key='1'),
                    ft.dropdownm2.Option(text="Status",key='2'),
                    ft.dropdownm2.Option(text="Holding",key='3'),
                    ft.dropdownm2.Option(text="Input",key='4'),
                ],
                autofocus=True,
                expand=1,
            ),
            ft.TextField(label="Address", value="0",width=80),
            ft.TextField(label="Count", value="1",width=70),
            ft.FilledButton(text='Exec',on_click=mb_exec)
        ],
        visible=False,
        scale=ft.transform.Scale(scale=0),
        animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
    )
    mb_view = ft.Container(
        content=ft.ListView(
            expand=1, 
            spacing=10, 
            padding=10, 
            auto_scroll=True    
        )
        ,bgcolor=ft.Colors.AMBER_100
        ,expand=1     
        ,border_radius=10
        ,border=ft.border.all(1, ft.Colors.BLACK)
        ,margin=8  
        ,padding=0    
    )
    mb_view.content.controls.append(ft.Text('hello'))

    mb_body=ft.Container(
        content=ft.Column([
            mb_view,
            mb_panel
        ])
        ,expand=1        
        
    )

    mb_connect=ft.Icon(name=ft.Icons.RUN_CIRCLE, size=36,color="gray",data=0,tooltip='close')
    mb_head=ft.Column(
        [
            ft.Row(
                [
                    ft.TextField(label="Host", value="127.0.0.1",expand=1),
                    ft.TextField(label="Port", value="502",width=100),
                ],
                
            ),
            ft.Row(
                [
                    ft.Row(
                        [
                            mb_connect,
                        ]
                        ,expand=1
                        ,spacing=10
                    ),                    
                    ft.Row(
                        [
                            ft.FilledButton(
                                text="Open",    
                                on_click=mb_open,
                            ),
                            ft.FilledButton(
                                text="Close",  
                                on_click=mb_close,
                            ),                    
                        ]
                        ,alignment=ft.MainAxisAlignment.END
                        ,spacing=10
                        ,expand=1
                    ),
                ]
            ),              
        ],       
        spacing=10,       
    )

    page.title="Modbus Viewer"
    page.window.max_width=400
    page.window.max_height=600
    page.window.width=400
    page.window.height=600
    page.resizable=False

    page.add(
        mb_head,         
        mb_body,
        timer,         
    )
    
    
                                          
ft.app(target=main)