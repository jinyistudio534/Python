import random
import asyncio
import serial_asyncio
import time
# 接收异步函数，收到后打印时间、收到的内容和接收的序号
async def read_from_serial(reader):
    count = 0
    buff = b''
    cmd = 0
    while True:
        data = await reader.read(1000)
        buff = buff + data
        #print(f'reciived {buff}, {len(buff)}')

        if b'#OK\r' in buff:            
          cmd = 1                

        elif b'#NOK\r' in buff:            
          cmd = 2       

        if cmd in (1,2):
          p = time.strftime("%X", time.localtime())
          print(f'received at {p}, {buff}, serial = {count}')
          count += 1
          buff = b''
          cmd = 0

# 发送异步函数，每隔两秒钟发送一次
async def write_to_serial(writer):
    while True:
        bs1 =  b'.$DM2:%d\r' % random.randint(0, 255) 
        writer.write(bs1)
        await writer.drain()
        await asyncio.sleep(0.1)
        
async def dimmer():
    # 连接串口，其中的'/dev/cu.usbserial-1140'是串口的名称，
    # windows 的串口名一般是 'comx' 的格式，例如：'com3；
    # linux 的串口格式一般是 '/dev/ttyx' 的格式，例如：'dev/ttyUSB0'。
    reader, writer = await serial_asyncio.open_serial_connection(url='/dev/rfcomm0', baudrate=19200)
    # 生成串口读写异步任务各一个
    task_1 = asyncio.create_task(read_from_serial(reader))
    task_2 = asyncio.create_task(write_to_serial(writer))
    # 并行运行两个异步任务
    await task_1
    await task_2


async def main():
  tasks = [dimmer()]
  await asyncio.gather(*tasks)

asyncio.run(main())

# alias supy='sudo -E env PATH=$PATH python3'
  
