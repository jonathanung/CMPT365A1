import tkinter as tk
from tkinter.filedialog import askopenfilename as tk_file_path
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as mpl_plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from playsound import playsound
import os

def read_8_bit(file):
    raw = file.read()
    data = []
    for i in range(0, len(raw), 3):
        sample = raw[i:i+1]
        data.append(int.from_bytes(sample, 'little'))
    return np.array(data).astype(np.int8)

def read_16_bit(file):
    raw = file.read()
    data = []
    for i in range(0, len(raw), 3):
        sample = raw[i:i+2]
        data.append(int.from_bytes(sample, 'little'))
    return np.array(data).astype(np.int16)

def read_24_bit(file):
    raw = file.read()
    data = []
    for i in range(0, len(raw), 3):
        sample = raw[i:i+3] #read 3 bytes from sample
        sample += b'\x00' #add 1 byte padding to make 32 bits
        data.append(int.from_bytes(sample, 'little')) #append to list as 32 bits
    return np.array(data).astype(np.int32)

def read_32_bit(file):
    raw = file.read()
    data = []
    for i in range(0, len(raw), 3):
        sample = raw[i:i+4]
        data.append(int.from_bytes(sample, 'little'))
    return np.array(data).astype(np.int32)

def parse_wav_data(event):
    file_path = tk_file_path(filetypes=[("WAV files", "*.wav")])
    if not file_path:
        return
    mpl_plt.clf()
    left_channel_display.clear()
    right_channel_display.clear()
    #https://docs.fileformat.com/audio/wav/
    """
    Using the file format specification, parse the wav file and display the data.
    This way of parsing the data is not the most efficient, but it is the most readable.
    We can see how the data is being stored in the file, which allows us to 
    parse the data correctly. We use the 'rb' flag to read the file in binary mode.
    """
    with open(file_path, 'rb') as file:
        file.seek(0) #check if file is a wav file
        if(file.read(4).decode('utf-8')) != "RIFF":
            print("This is not a wav file.")
            top_label.config(text="This is not a wav file.", fg="red")
            return
        file.seek(22) #check for stereo
        if(int.from_bytes(file.read(2), 'little')) != 2:
            print("This is not a stereo wav file.")
            top_label.config(text="This is not a stereo wav file.", fg="red")
            return
        file.seek(24) #get sampling rate
        sampling_rate =  int.from_bytes(file.read(4), 'little')
        file.seek(34) #get sampling depth
        sampling_depth = int.from_bytes(file.read(2), 'little')
        file.seek(44)
        if sampling_depth == 8:
            data = read_8_bit(file)
        elif sampling_depth == 16:
            data = read_16_bit(file)
        elif sampling_depth == 24:
            data = read_24_bit(file)
        elif sampling_depth == 32:
            data = read_32_bit(file)
        left = data [0::2]
        right = data [1::2]
    file.close()
    time = np.linspace(0, len(left) / sampling_rate, num=len(left))

    display_data(time, left, right, sampling_depth)

    top_label.config(text="Current File: " + file_path, fg="white")
    footer_label.config(text="Samples: " + str(len(left)) + ", Sampling Frequency: " + str(sampling_rate) + ", Sampling Depth: " + str(sampling_depth))
    global current_file
    current_file = file_path
    footer_button.config(state=tk.NORMAL)

def display_data(time, left, right, sampling_depth):
    left_channel_display.plot(time, left, color='green')
    left_channel_display.set_title('Left Channel Data')
    left_channel_display.set_xlabel('Time (in seconds)')
    left_channel_display.set_ylabel('Amplitude (in bits)')
    left_channel_display.set_ylim(2**sampling_depth * -0.5, 2**sampling_depth * 0.5)
    
    right_channel_display.plot(time, right, color='green')
    right_channel_display.set_title('Right Channel Data')
    right_channel_display.set_xlabel('Time (in seconds)')
    right_channel_display.set_ylabel('Amplitude (in bits)')
    right_channel_display.set_ylim(2**sampling_depth * -0.5, 2**sampling_depth * 0.5)

    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def play_current(event):
    global current_file
    if current_file and os.path.exists(current_file):
        try:
            playsound(current_file)
        except Exception as e:
            top_label.config(text=f"Error playing sound: {e}", fg="red")
    else:
        top_label.config(text="No file selected or file does not exist.", fg="red")


current_file = ""

window = tk.Tk()
window.title("CMPT 365 Assignment 1 Question 1")
window.geometry("1200x800")

header_frame = tk.Frame(window, pady=3)
header_label = tk.Label(header_frame, text="CMPT 365 Assignment 1 Question 1", fg="white")
header_label['font'] = 'Arial 21 bold'
header_label.pack()
header_frame.pack(fill=tk.X)

top_frame = tk.Frame(window, pady=3)
top_label = tk.Label(top_frame, text="Select a .wav file to open", fg="white")
top_label.pack()

file_button = tk.Button(top_frame, text="Open File")
file_button.bind("<Button-1>", parse_wav_data)
file_button.pack(padx=0, pady=0)

top_frame.pack(fill=tk.X)

bottom_frame = tk.Frame(window, pady=3, bg="white")

#matplotlib figure initialization
mpl_plt.fig = Figure(figsize=(12, 6))
canvas = FigureCanvasTkAgg(mpl_plt.fig, master=bottom_frame)
mpl_plt.fig.subplots_adjust(hspace=0.5)
left_channel_display = mpl_plt.fig.add_subplot(2, 1, 1)
right_channel_display = mpl_plt.fig.add_subplot(2, 1, 2)
display_data([], [], [], 0)

bottom_frame.pack(fill=tk.BOTH , expand=True, padx=10, pady=10)

footer_frame = tk.Frame(window, pady=3)
footer_label = tk.Label(footer_frame, text="Samples: 0, Sampling Frequency: 0, Sampling Depth: 0", fg="white")
footer_button = tk.Button(footer_frame, text="Play Sound", state=tk.DISABLED)
footer_button.bind("<Button-1>", play_current)
footer_button.pack()
footer_label.pack()
footer_frame.pack(fill=tk.X)

exit_frame = tk.Frame(window, pady=3)
exit_button = tk.Button(exit_frame, text="Exit", command=window.quit)
exit_button.pack()
exit_frame.pack(fill=tk.X)

window.mainloop()