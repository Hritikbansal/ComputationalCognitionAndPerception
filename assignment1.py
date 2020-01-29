from psychopy import event, visual, core, sound, prefs
import psychtoolbox as ptb
import random
import numpy as np
import matplotlib.pyplot as plt
import os


flag_start = False
possiblities = [-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
li = 3*[-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
random.shuffle(li)
currDir = os.getcwd()
dic={}
for h in possiblities:
	if h not in dic:
		dic[h]=0

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
			elif thisKey == '1' and flag:
				if time<0:
					dic[time]+=1
				thisResp = 1
			elif thisKey == '3' and flag:
				if time>0:
					dic[time]+=1
				thisResp = 1
			elif thisKey == '2' and flag:
				if time==0:
					dic[time]+=1
				thisResp = 1
			elif thisKey == 'c' and not flag:
				thisResp = 1
		event.clearEvents()  # clear other (eg mouse) events - they clog the buffer

	return 0

#create a window
mywin = visual.Window([800,600],monitor="testMonitor", units="deg")

# creating flash stimuli
flash1 = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[0,0], sf=0)
flash2 = visual.GratingStim(win=mywin, mask='circle', size=2, pos=[0,3], sf=0)
# creating sound stimuli
path = currDir+"\\bell.wav" 
mySound = sound.Sound(path)

message1 = visual.TextStim(win=mywin, pos=[7,0], text='Hit S to start, Q/Esc to Abort!')
message2 = visual.TextStim(win=mywin, pos=[7,2], text='Press 1-Bell before Flash')
message3 = visual.TextStim(win=mywin, pos=[7,4], text='Press 2-Bell same as Flash')
message4 = visual.TextStim(win=mywin, pos=[7,6], text='Press 3-Bell after Flash')
message5 = visual.TextStim(win=mywin, pos=[7,0], text='Press C to continue')
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
		print(diffTime)
		# flash2.draw()
		# mywin.flip()
		# flash2.draw()
		# flash1.draw()
		# core.wait(-diffTime)
		# mywin.flip()
		mySound.play()
		core.wait(-diffTime) 
		flash1.draw()
		mywin.flip()
	elif(diffTime>0):
		# print(diffTime)
		# flash1.draw()
		# mywin.flip()
		# flash1.draw()
		# flash2.draw()
		# core.wait(diffTime)
		# mywin.flip()

		print(diffTime)
		flash1.draw()
		mywin.flip()
		core.wait(diffTime)
		mySound.play()

	else:
		# print(diffTime)
		# flash1.draw()
		# flash2.draw()
		# mywin.flip()

		print(diffTime)
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
y = []
for h in possiblities:
	y.append(dic[h])

plt.plot(possiblities,y)
plt.show()









# if len(event.getKeys())>0:
# 	break
# event.clearEvents()

#mywin.close()

# now = ptb.GetSecs()
# mySound.play(when=now+0.5)  

# list of possible time differences between flash and bell
# time units is ms here
#print(li)