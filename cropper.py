
import tkinter as tk
import tkinter.ttk as ttk
from utils.image_processing import *
from utils.gui import *
from PIL import ImageTk, Image

# Main window instance
# window = tk.Toplevel()
window = tk.Tk()
window.title("Paradigm Cropper")
window.geometry("600x600")
window.minsize(200, 500)
main_frame = tk.Frame(window)
#scrollbar = tk.Scrollbar(main_frame, orient = "vertical", command = main_frame.after)
main_frame.pack(side = "left", fill = "y")

## Window's widgets
frame_input = tk.Frame(main_frame)
label_get_input = tk.Label(frame_input, text = "Selectionnez une image: ")
input_image_path = tk.StringVar(frame_input)
input_image_path.set("")
button_input_image = tk.Button(frame_input, text = "Naviguer...",
                               command = lambda: browse_image(input_image_path,
                                                              input_image_visualizer,
                                                              (window.winfo_width(), window.winfo_height())))
label_input_image = tk.Entry(main_frame, textvariable = input_image_path, width = 300, state = "disable")
frame_visualizer = tk.Frame(main_frame)
input_image_visualizer = tk.Label(frame_visualizer, image = None)
output_image_visualizer = tk.Label(frame_visualizer, image = None)
button_crop = tk.Button(main_frame, text = "Crop!",
                        command = lambda: show_cropped_image(input_image_path,
                                                             output_image_visualizer,
                                                             (window.winfo_width(), window.winfo_height())))
frame_save = tk.Frame(main_frame)
label_get_save_dir = tk.Label(frame_save, text = "Selectionnez où sauvegarder l'image traitée: ")
save_dir = tk.StringVar(frame_save)
save_dir.set("")
button_get_save_dir = tk.Button(frame_save, text = "Naviguer...", command = lambda : browse_output_dir(save_dir))
label_show_save_dir = tk.Entry(main_frame, textvariable = save_dir, width = 300, state = "disable")
button_go_save = tk.Button(main_frame, text = "Savegarder",
                           command = lambda: save_cropped_image(input_image_path, save_dir, is_saved))
is_saved = tk.StringVar(frame_save)
is_saved.set("")
label_is_saved = tk.Label(main_frame, textvariable = is_saved)

## Place widgets on the main_frame grid
# Frame input image
frame_input.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "W")
label_get_input.grid(row = 0, column = 0, sticky = "W")
button_input_image.grid(row = 0, column = 1, sticky = "W")
label_input_image.grid(row = 1, column = 0, padx = 10, sticky = "W")
# Frame picture visualizer
frame_visualizer.grid(row = 2, column = 0, padx = 10, sticky = "W")
input_image_visualizer.grid(row = 0, column = 0, sticky = "W")
output_image_visualizer.grid(row = 0, column = 1, padx = 5, sticky = "W")
button_crop.grid(row = 3, column = 0, padx = 10, sticky = "W")
# Frame save cropped image
frame_save.grid(row = 4, column = 0, padx = 10, sticky = "W")
label_get_save_dir.grid(row = 0, column = 0, sticky = "W")
button_get_save_dir.grid(row = 0, column = 1, sticky = "W")
label_show_save_dir.grid(row = 5, column = 0, sticky = "W")
button_go_save.grid(row = 6, column = 0, padx = 10, pady = 15, sticky = "W")
label_is_saved.grid(row = 7, column = 0, padx = 10, sticky = "W")

window.bind("<Configure>", lambda event: resize_visualizer(event, window, input_image_path, frame_visualizer))
window.mainloop()

