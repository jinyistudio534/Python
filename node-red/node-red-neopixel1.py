import sys
import board
import neopixel
import time
import json
import asyncio

pixels = neopixel.NeoPixel(board.D18, 4)
neo = [0,0,0,0,0]

async def loop_neopixel():
  global ledOn
  while	True:
    if neo[0]==255:
	    pixels.fill([neo[2],neo[3],neo[4]])	   

    elif neo[0]==0:	    
	    pixels.fill(0)


    await asyncio.sleep(0.02)    
	    

async def loop_stdin():	
	global neo

	print("Got arguments: ", sys.argv)
	loop = asyncio.get_event_loop()
	while True:
		s1 = await loop.run_in_executor(None, sys.stdin.readline)
		s1 = s1.strip()
		if len(s1)==10:
			neo[0] = int(s1[0:2], 16)
			neo[1] = int(s1[2:4], 16)
			neo[2] = int(s1[4:6], 16)
			neo[3] = int(s1[6:8], 16)
			neo[4] = int(s1[8:10], 16)

		print(s1)
		await asyncio.sleep(0.025)  

async def main():
    tasks = [loop_stdin(),loop_neopixel()]
    await asyncio.gather(*tasks)

asyncio.run(main())

