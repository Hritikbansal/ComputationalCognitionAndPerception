from psychopy import event, visual, core, sound
import psychtoolbox as ptb
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Perception Test'
    )
    parser.add_argument('--audiopath', type=str, metavar='PATH', required=True,
                        help='audio filename path')

    return parser.parse_args()

def takeResponse(flag=0,time=0):
	thisResp = None
	# get response
	while thisResp==None:
		allKeys=event.waitKeys()
		for thisKey in allKeys:
			if thisKey=='s' and not flag:
				thisResp = 1 
			elif thisKey in ['q', 'escape']:
				event.clearEvents()
				return 1  # abort experiment
			elif thisKey == 'left' and flag:
				if time<0:
					dic[time]+=1
				thisResp = 1
			elif thisKey == 'right' and flag:
				if time>0:
					dic[time]+=1
				thisResp = 1
			elif ((thisKey == 'up' or thisKey == 'down') and flag):
				if time==0:
					dic[time]+=1
				thisResp = 1
			elif thisKey == 'c' and not flag:
				thisResp = 1
		event.clearEvents()  # clear other (eg mouse) events - they clog the buffer

	return 0

possiblities = [-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
li = 1*[-0.3,-0.2,-0.1,0,0.1,0.2,0.3]

random.shuffle(li)
dic={}
for h in possiblities:
	if h not in dic:
		dic[h]=0


#create a window
mywin = visual.Window([800,600],monitor="testMonitor", units="deg",fullscr=True)

# creating flash stimuli
flash1 = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[0,0], sf=0)
flash2 = visual.GratingStim(win=mywin, mask='circle', size=2, pos=[0,3], sf=0)
# creating sound stimuli

args = parse_arguments()
audioPath = args.audiopath

if not os.path.exists(audioPath):
	print("SOUND FILE NOT FOUND")
	print("CHECK THE PATH PLSS")
	print("EXITING!!!")

mySound = sound.Sound(audioPath,secs=0.3)

message1 = visual.TextStim(win=mywin, pos=[7,0], text='Hit S to start, Q/Esc to Abort!')

message2 = visual.TextStim(win=mywin, pos=[7,2], text='Press ← B before F')
message3 = visual.TextStim(win=mywin, pos=[7,4], text='Press → F before B')
message4 = visual.TextStim(win=mywin, pos=[7,6], text='Press ↑ or ↓ B F same')
message5 = visual.TextStim(win=mywin, pos=[7,-2], text='Press C to continue')
 
#before means bell before 
globalClock = core.Clock()
thisResp = None
#message.autoDraw = True

message1.draw()
mywin.flip()

if(takeResponse(flag=0)):
	core.quit()
	event.clearEvents()

mywin.flip()
ind = 0
message2.draw()
message3.draw()
message4.draw()
message5.draw()
mywin.flip()
resp = takeResponse(flag=0)
while True:
	diffTime = li[ind]
	ind+=1
	if(diffTime<0):
		mySound.play()
		core.wait(-diffTime) 
		flash1.draw()
		mywin.flip()
	elif(diffTime>0):
		flash1.draw()
		mywin.flip()
		core.wait(diffTime)
		mySound.play()
	else:
		mySound.play()
		flash1.draw()
		mywin.flip()
	
	resp = takeResponse(flag=1,time= diffTime)
	if(resp):
		core.quit()
	mywin.flip()
	if(ind == len(li)):
		break
	core.wait(1.5)

print("Experiment completed!!")
mywin.close()

#plotter
y = []
factor = len(li)/len(possiblities)
for h in possiblities:
	y.append((100*dic[h])/factor)
x = [1000*j for j in possiblities]
plt.plot(x,y)
plt.title("Result")
plt.xlabel("Time difference between bell and flash(ms)")
plt.ylabel("Accuracy(%)")
plt.show()