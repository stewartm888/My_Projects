#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 21:16:07 2022

@author: fred
"""

import time
import pyautogui
import tkinter as tk

time.sleep(5)

pyautogui.moveTo(750, 400, duration = 1)

for x in range(5):
	pyautogui.click(button='right')
	time.sleep(.25)
	pyautogui.press("v")
	time.sleep(.25)
	pyautogui.hotkey("ctrl", "a")
	time.sleep(.25)
	pyautogui.hotkey("ctrl", "c")
	root = tk.Tk()
	root.withdraw()
	filename = root.clipboard_get()

	if filename.endswith('.png'):
		pyautogui.press('enter')
		time.sleep(2.5)
		pyautogui.press('esc')
		time.sleep(.5)
		pyautogui.press('right')
		time.sleep(1.5)
	else:
		pyautogui.press('enter')
		time.sleep(2)
		pyautogui.press('right')
		time.sleep(2)