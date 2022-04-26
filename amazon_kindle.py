
# INSTRUCTIONS
## Have two tabs open in Google Chrome. 
### The left tab should be an Amazon Kindle Reader with a novel loaded. 
### The right tab should be a Google Doc. Make sure the doc is saved.
## Run this file, then quickly open the browser to the Kindle Reader

# DETAILS
## When you right click on a page in the Kindle Reader, "Search Images with Google Lens" should be the 7th option from the top
## Reader settings should be single column and fairly large font (ie, fewer words per page)
## This has been tested on screen of the following dimensions: width=1920, height=1080


import time
import pyautogui

time.sleep(4)

for x in range(10):
	pyautogui.moveTo(500, 500, duration = 1)
	pyautogui.click(button='right')
	pyautogui.moveRel(50, 170, duration = 1)
	pyautogui.click()
	pyautogui.moveTo(220, 160, duration = 1)
	pyautogui.dragTo(1794, 1000, duration = 1.5)
	time.sleep(22)
	
	#Text button
	pyautogui.moveTo(601, 1003, duration = 1)
	pyautogui.click()

	#Select all text button
	time.sleep(7)
	pyautogui.moveTo(1530, 725, duration = 1)
	pyautogui.click()

	#Copy text button
	time.sleep(3)
	pyautogui.moveTo(1225, 248, duration = 1)
	pyautogui.click()

	#Exit tab
	time.sleep(1)
	pyautogui.hotkey("ctrl", "w")

	#Next tab
	time.sleep(1)
	pyautogui.hotkey("ctrl", "tab")


	#Paste text
	time.sleep(1)
	pyautogui.hotkey("ctrl", "v")
	pyautogui.press("enter")

	#Save text
	time.sleep(1)
	pyautogui.hotkey("ctrl", "s")

	#Return to book
	time.sleep(.3)
	pyautogui.hotkey("ctrl", "shift","tab")

	#Turn page
	time.sleep(.3)
	pyautogui.press('right') 



"""
	#pyautogui.press("s")
	#pyautogui.press('enter')


	time.sleep(1)
	pyautogui.press('right') 

for x in range(5):
	time.sleep(1)
	pyautogui.moveTo(220, 160, duration = 1)
	time.sleep(1)
	pyautogui.moveTo(1794, 1000, duration = 1)
	print(pyautogui.position()) 
"""


#pyautogui.moveTo(500, 500, duration = 1)
#pyautogui.click(button='right')

#pyautogui.hotkey("ctrlleft", "a")






#pyautogui.hotkey("alt", "tab")


""" 
time.sleep(3)

# moves mouse to 1000, 1000.
pyautogui.dragRel(100, 0, duration = 1)
 
# drags mouse 100, 0 relative to its previous position,
# thus dragging it to 1100, 1000
pyautogui.dragRel(0, 100, duration = 1)
pyautogui.dragRel(-100, 0, duration = 1)
pyautogui.dragRel(0, -100, duration = 1)
"""
