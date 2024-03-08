import tkinter as tk
from tkinter.filedialog import askopenfilename as tkfname
from PIL import Image, ImageTk

byte_dict = {
    b'II': 'little',
    b'MM': 'big'
}

def display_selected_tiff(event):
    file_path = tkfname(filetypes=[("TIF files", "*.tif")])
    if not file_path:
        return
    print("Selected file:", file_path)

    # Here we are going to check if the file is a valid TIFF file.
    with open(file_path, 'rb') as file:
        file.seek(0)
        byte_order = byte_dict[file.read(2)]
        file.seek(2)
        if int.from_bytes(file.read(2), byte_order) != 42:
            print("This is not a valid TIFF file.")
            return
    file.close()
    
    # Use the pillow library to open the image.
    img = Image.open(file_path)
    
    # Since we are told we have a max image size of 704x576, we will resize the image to fit, according to the parameters for Q2
    size = (704, 576)
    img.thumbnail(size)
    
    # Convert the image to a format Tkinter can use the image, and display it.
    img_display = ImageTk.PhotoImage(img)
    image_label.config(image=img_display)
    image_label.image = img_display # Keep a reference to the image so it doesn't get destroyed by Python's garbage collector.


window = tk.Tk()
window.title("CMPT 365 Assignment 1 Question 2")
window.geometry("800x800")

header_label = tk.Label(window, text="CMPT 365 Assignment 1 Question 2", font='Arial 21 bold')
header_label.pack()

top_label = tk.Label(window, text="Select a .tif file to open")
top_label.pack()

file_button = tk.Button(window, text="Open File")
file_button.bind("<Button-1>", display_selected_tiff)
file_button.pack()

# Create a label to display the image (aka, this is where we are going to display the image).
image_label = tk.Label(window)
image_label.pack()

exit_frame = tk.Frame(window, pady=3)
exit_button = tk.Button(exit_frame, text="Exit", command=window.quit)
exit_button.pack()
exit_frame.pack(fill=tk.X)

window.mainloop()



# def display_selected_tiff(event):
#     file_path = tkfname(filetypes=[("TIF files", "*.tif")])
#     if not file_path:
#         return
#     print("Selected file:", file_path)
#     with open(file_path, 'rb') as file:
#         file.seek(0)
#         byte_order = byte_dict[file.read(2)]
#         print("Byte order:", byte_order)    
#         file.seek(2)
#         if int.from_bytes(file.read(2), byte_order) != 42:
#             print("This is not a valid TIFF file.")
#             return
#         file.seek(4)
#         offset = int.from_bytes(file.read(4), byte_order)
#         file.seek(offset)
#         num_entries = int.from_bytes(file.read(2), byte_order)
#         print("Number of entries:", num_entries)
#         for i in range(num_entries):
#             tag_id = int.from_bytes(file.read(2), byte_order)
#             data_type = int.from_bytes(file.read(2), byte_order)
#             num_values = int.from_bytes(file.read(4), byte_order)
#             value_or_offset = int.from_bytes(file.read(4), byte_order)
#             file.seek(4, 1)  # Skip over unused bytes
#             print(f"Tag ID: {tag_id}, Data Type: {data_type}, Num Values: {num_values}, Value/Offset: {value_or_offset}")
# This was the function I created prior to changing the code to utilize the Pillow Library. I am keeping it here for reference.