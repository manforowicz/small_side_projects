import select
import sys
from pykeyboard import PyKeyboard
import time
k = PyKeyboard()

for key in [k.up_key, k.left_key, k.right_key, 'r']:
	k.press_key(key)
	k.release_key(key)

throttleWakeUp = 0
gimbalWakeUp = 0

while True:
	currTime = time.time()

	if throttleWakeUp < currTime:
      k.release_key(k.up_key)
	if gimbalWakeUp < currTime:
		k.release_key(k.left_key)
		k.release_key(k.right_key)
		
	wakeup = min(throttleWakeUp, gimbalWakeUp)
	if wakeup > currTime:
		timeout = wakeup - currTime
	else:
		timeout = 999
	print('hallo, timeout: ' + str(timeout))
	ready, ignored1, ignored2 = select.select([sys.stdin], [], [], timeout)
	print("ready:" + str(len(ready)))
	
	if len(ready) > 0:
		line = sys.stdin.readline()
		throttle,gimbal = line.split()
		throttle = int(throttle)
		gimbal = int(gimbal)
		currTime = time.time()
		if throttle > 0:
			k.press_key(k.up_key)
			throttleWakeUp = currTime + throttle / 1000.0
		else:
			throttleWakeUp = 0
	
		if not gimbal == 0:
			if gimbal > 0:
				k.press_key(k.right_key)
			else:
				k.press_key(k.left_key)
			gimbaleWakeUp = currTime + abs(gimbal / 1000.0)
		else:
			gimbalWakeUp = 0
