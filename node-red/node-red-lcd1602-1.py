import sys
import board
import time
import asyncio
import json
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode

lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=2, num_cols=16)
lcd.home()
mq = []
async def loop_lcd(): 
	while	True:
		if len(mq)>0:			
			jps = mq[0]			
			del mq[0]

			jp = json.loads(jps)			

			if not(jp.get('clear') is None):
				if jp['clear']:
					lcd.clear()

			if not(jp.get('cursor') is None):
				match jp['cursor']:
    					case 1:
        					lcd.set_cursor_mode(CursorMode.LINE)
    					case 2:
        					lcd.set_cursor_mode(CursorMode.BLINK)
    					case _:
        					lcd.set_cursor_mode(CursorMode.HIDE)  

			if not(jp.get('home') is None):
				if jp['home']:
					lcd.home()

			if not(jp.get('msgs') is None):
				r1=0
				_pos = False
				for msg in jp['msgs']:	
					if not(msg.get('x') is None):
						if not(msg.get('y') is None):
							lcd.set_cursor_pos(msg['y'], msg['x'])
							print('goto.{}/{}'.format(msg['y'], msg['x']))
							_pos = True

					t1 = msg['text']
					l1 = len(t1)

					if l1>20:
						t1 = msg['text'][0:20]
						l1 = len(t1)

					if l1>0:	
						print('pos.{}'.format(_pos))					
						if not(_pos):
							c1 = 0
							if not(msg.get('center') is None):
								if msg['center']:
									c1 = 8 - l1//2

							#print(l1,c1)							
							lcd.set_cursor_pos(r1, c1)

						lcd.print(t1)
						
					r1 += 1

		await asyncio.sleep(0.02)
	    

async def loop_stdin():	
	loop = asyncio.get_event_loop()
	while True:
		s1 = await loop.run_in_executor(None, sys.stdin.readline)
		s1 = s1.strip()
		if len(s1)>0:
			mq.append(s1)
			print(s1)
			
		await asyncio.sleep(0.02)    

async def main():
    tasks = [loop_stdin(),loop_lcd()]
    await asyncio.gather(*tasks)


asyncio.run(main())
    

