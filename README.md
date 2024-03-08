# Python Version: 3.11 #

### ALL LIBRARIES BELOW MUST BE INSTALLED USING PIP! ###

## Libraries used: ##

# Question 1 #
- Tkinter as tk
    -tkinter.filedialog -> askopenfilename as tk_file_path
- MatplotLib as mpl
    - matplotlib.pyplot as mpl_plt
    - matplotlib.figure -> Figure
    - matplotlib.backends.backend_tkagg -> FigureCanvasTkAgg
- Playsound
- OS

# Question 2 #t
- Tkinter as tk
    -tkinter.filedialog -> askopenfilename as tk_file_path
- Pillow

# Key GUI functions (Q1): #
- window = tk.Tk(), which initializes the main window of the app.
- tk.Frame(), container for other GUI components
- tk.Label(), text/image display
- tk.Button(), clickable button, bound to action using button.bind()
- component.pack(), used to certify order in parent container
- window.mainloop(), runs the main loop
- Figure(), the plot controller, used for displaying the data, figures, axes, and options for the display
- FigureCanvasTkAgg(), used for embedding, rendering, and integrating the figure in Tkinter
- Figure.add_subplot(), adds a subplot to the Figure
- subplot.plot(), used for plotting the data on a respective subplot


# Key GUI functions (Q2): #
- window = tk.Tk(), which initializes the main window of the app.
- tk.Frame(), container for other GUI components
- tk.Label(), text/image display
- tk.Button(), clickable button, bound to action using button.bind()
- component.pack(), used to certify order in parent container
- window.mainloop(), runs the main loop
- Image.open(), opens the specified image
- Image.thumbnail(size), resizes (crops) an image so it fits in a set of dimensions
- ImageTk.PhotoImage(), converts image from Pillow to a format that Tkinter can display.

# Video of program usage: IN FOLDER #

# Environment: MacOS Sonoma 14.2.1 ARM#