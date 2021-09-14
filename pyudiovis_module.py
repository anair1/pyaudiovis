import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython

get_ipython().run_line_magic('matplotlib', 'tk')

CHNK = 1024 * 4
FORM = pyaudio.paInt16
CHAN = 1
RATE = 44100

fig, ax = plt.subplots(1, figsize=(15, 7))
p = pyaudio.PyAudio()

strm = p.open(
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
    fig.canvas.draw()
    fig.canvas.flush_events()
    frame_count += 1