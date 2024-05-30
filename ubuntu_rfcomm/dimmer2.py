import random
import asyncio
import serial_asyncio


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):       
        self.transport = transport
        transport.serial.rts = False  # You can manipulate Serial object via transport
        print('made')
        self.Buff=b''
        self.Next = 0

    def data_received(self, data):
        #print('  >>  ', repr(data))
        self.Buff = self.Buff + data               

        if self.Buff==b'#OK\r':            
            self.Buff = b''
            self.Next = 1
            print('  >> #OK')
           

        elif self.Buff==b'#NOK\r':            
            self.Next = 2    
            print('  >> #NOK')
            self.Buff=b''

        else:
            self.Next = 0    
        #print(self.Next)
        # stop callbacks again immediately
        self.pause_reading()

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):       
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        
        self.transport.resume_reading()


async def reader():
  transport, protocol = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, '/dev/rfcomm0', baudrate=19200)
  ct = 0
  while True:       
        await asyncio.sleep(0.1)
        if protocol.Next==0:
                bs1 =  b'.$DM2:%d\r' % random.randint(0, 255)        
                transport.write(bs1)  # Write serial data via transport
                protocol.Next = 99
                protocol.resume_reading()
                print(bs1,end='')

        elif protocol.Next in (1,2):                
                ct = ct + 1
                if ct>999:
                        break;
                #print(ct)
                protocol.Next =0



loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()
'''
async def main():
    tasks = [reader()]
    await asyncio.gather(*tasks)

asyncio.run(main())
'''
