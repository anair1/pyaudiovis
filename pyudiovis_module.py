import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

56

CHNK = 1024 * 4
FORM = pyaudio.paInt16
CHAN = 1
RATE = 44100

fig, ax = plt.subplots(1, figsize=(15, 7))
p = pyaudio.PyAudio()

info=p.get_host_api_info_by_index(0)
numdevs=info.get('deviceCount')
for i in range(0, numdevs):
    if(p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels'))>0:
        print("Input Device ID ", i, "-", p.get_device_info_by_host_api_device_index(0,i).get('name'))

audio_in=input("\n\nSelect input by Device ID: ")

strm = p.open(
    input_device_index=int(audio_in),
    format=FORM,
    channels=CHAN,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHNK
)

x = np.arange(0, 2 * CHNK, 2)
line, = ax.plot(x, np.random.rand(CHNK), '-', lw=2)
ax.set_ylim(-255, 255)
ax.set_xlim(0, 2*CHNK)
plt.setp(ax, xticks=[0, CHNK, 2 * CHNK], yticks=[0, 128, 255])

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    data = strm.read(CHNK)
    data_int = np.array(struct.unpack(str(2 * CHNK) + 'B', data), dtype='b')[::2] + 128
    line.set_ydata(data_int)
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count+=1
    except TclError:
        frame_rate = frame_count / (time.time() - start_time)

        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break