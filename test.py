# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import sounddevice as sd
import soundfile
import os
import queue
import vosk
import sys


root = tkinter.Tk()
root.title('HDK ASR')
root.geometry('870x500')
root.resizable(False, False)

allowRecording = False 



q = queue.Queue() 



def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


modelpath = "model"
device_info = sd.query_devices(1,'input')
samplerate = int(device_info['default_samplerate'])
model = vosk.Model(modelpath)



def record():
	global allowRecording
	while allowRecording:
	    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=1, dtype='int16',
                            channels=1, callback=callback):
                rec = vosk.KaldiRecognizer(model, samplerate)
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        out = rec.Result()
                        txt_text.insert('1.0',format(out))
		


def start():
	global allowRecording
	allowRecording = True
	lbStatus['text'] = 'Recording...'
	threading.Thread(target=record).start()

def stop():
	global allowRecording
	allowRecording = False
	lbStatus['text'] = 'Ready'
    

def closeWindow():
	if allowRecording:
		tkinter.messagebox.showerror('Recording', 'Please stop recording before close the window.')
		return
	root.destroy()

btnStart = tkinter.Button(root, text='Start', command=start)
btnStart.place(x=30, y=20, width=100, height=20)
btnStop = tkinter.Button(root, text='Stop', command=stop)
btnStop.place(x=140, y=20, width=100, height=20)
lbStatus = tkinter.Label(root, text='Ready', anchor='w', fg='green')    
lbStatus.place(x=30, y=50, width=200, height=20)
txt_label = tkinter.Label(root, text="ASR：")
txt_label.place(x=10, y=70)

txt_text = tkinter.Text(root, width=120, height=30)
scroll = tkinter.Scrollbar()
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
scroll.config(command=txt_text.yview)
txt_text.config(yscrollcommand=scroll.set)
txt_text.place(x=10, y=100)
txt_text.insert('1.0', 'Begin')

root.protocol('WM_DELETE_WINDOW', closeWindow)

root.mainloop()