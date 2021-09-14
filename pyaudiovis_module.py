# Importing relevant libraries
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.animation as animation
import pyaudio
import struct
import numpy as np

mpl.use('TkAgg')  # Matplotlib backend 'Tkinter'

audio_chunk = 1024 * 4  # 4096 audio samples/frame
audio_format = pyaudio.paInt16  # 16 bit
num_channels = 1  # Single Channel: Mono
sample_rate = 44100  # Samples/s 44100 KHz

fig, ax = plt.subplots()

p = pyaudio.PyAudio()  # PyAudio object

# Stream object outlines parameters for processing audio through input
audio_stream = p.open(
    format=audio_format,
    channels=num_channels,
    rate=sample_rate,
    input=True,
    output=True,
    frames_per_buffer=audio_chunk
)


# Animate function for real-time updating waveform plot
def animate(i):
    # Plot customizations
    plt.title('Waveform Visualizer')
    x = np.arange(0, 2 * audio_chunk, 2)
    line, = ax.plot(x, np.random.rand(audio_chunk))
    ax.set_ylim(-250, 500)
    ax.set_xlim(0, audio_chunk * 2)

    while True:
        # Read audio data from audio_chunk and store in data variable until input overflow
        data = audio_stream.read(audio_chunk, exception_on_overflow=False)
        # Store struct values in np array so plotted values do not cut off at 0
        data_int = np.array(struct.unpack(str(2 * audio_chunk) + 'B', data), dtype='b')[::2] + 128
        line.set_ydata(data_int)
        plt.setp(line, color='g', linewidth=0.5)
        ax.set_facecolor('xkcd:black')
        fig.canvas.draw()
        fig.canvas.flush_events()


# Animate the plot with 1ms interval between frames
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
