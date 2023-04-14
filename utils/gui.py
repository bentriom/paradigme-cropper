
import traceback
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from utils.image_processing import *

## Event trackers

def resize_visualizer(event, window, input_image_path, frame_visualizer):
    if event.widget.master is None:
        if (window.winfo_width() != event.width or window.winfo_height() != event.height):
            window_width, window_height = event.width, event.height
            if input_image_path.get() != "":
                input_image_visualizer = frame_visualizer.winfo_children()[0]
                resize_input_image(input_image_path, input_image_visualizer, (window_width, window_height))

def show_error(self, *args):
    err = traceback.format_exception(*args)
    tk.messagebox.showerror(title = "Python Exception", message = err)

## Helpers for picture displays
## Not helpful for now

def get_visualized_image_size(image_size, window_size):
    window_width, window_height = window_size[0], window_size[1]
    new_width = int(min(0.95 * (window_width / 2), image_size[0]))
    # new_height = int((new_width / image_size[0]) * image_size[1])
    new_height = int(min(0.55 * window_height, image_size[0]))

    return (new_width, new_height)

def resize_input_image(input_image_path, input_image_visualizer, window_size):
    if input_image_path != "":
        input_image = Image.open(input_image_path)
        input_image = input_image.resize(get_visualized_image_size(input_image.size, window_size))
        photo_input_image = ImageTk.PhotoImage(input_image)
        input_image_visualizer.configure(image = photo_input_image)
        input_image_visualizer.photo_image = photo_input_image

def show_cropped_image(input_image_path, output_image_visualizer, window_size):
    if input_image_path != "":
        output_image = process_image(input_image_path, save_image = False)
        output_image = output_image.resize(get_visualized_image_size(output_image.size, window_size))
        photo_output_image = ImageTk.PhotoImage(output_image)
        output_image_visualizer.configure(image = photo_output_image)
        output_image_visualizer.image = photo_output_image

## Helpers for image browsing / saving

def get_default_cropped_image_name(image_path):
    splitted_input_image_name = os.path.basename(image_path).split(".")
    # image_cropped_name = splitted_input_image_name[0] + "." + '.'.join(splitted_input_image_name[1:])
    image_cropped_name = splitted_input_image_name[0] + ".png"

    return image_cropped_name

def browse_image(input_image_dir):
    # Open image
    input_dir = filedialog.askdirectory(initialdir = "./", title = "Sélection du dossier des images à cropper")
    # Update label and visualisation
    if input_dir is not None:
        input_image_dir.set(input_dir)

def browse_output_dir(save_dir):
    output_dir = filedialog.askdirectory(initialdir = "./", title = "Sélection du dossier de sauvegarde")
    if output_dir is not None:
        save_dir.set(output_dir)

def save_cropped_image(input_image_dir, x_margin, y_margin, save_dir, is_saved):
    if (x_margin.get() < 0) or (y_margin.get() < 0):
        tk.messagebox.showwarning(title = "Marges incorrectes",
                                  message = "Les marges doivent être positives.")
        is_saved.set("Changez les marges.")
        return
    if (input_image_dir.get() == ""):
        is_saved.set(f"Choisissez une image à traiter et un dossier de sauvegarde.")
    elif (save_dir.get() == ""):
        is_saved.set(f"Choisissez un dossier de sauvegarde.")
    elif not os.path.isdir(os.path.dirname(save_dir.get())):
        is_saved.set(f"Dossier de sauvegarde inexisant: {save_dir.get()}.")
    elif input_image_dir.get() == save_dir.get():
        tk.messagebox.showwarning(title = "Dossier de sauvegarde",
                                  message = "Le dossier de sauvegarde est le même que celui d'entrée.")
        is_saved.set(f"Choisissez un autre dossier de sauvegarde.")
    else:
        is_saved.set("Sauvegarde en cours...")
        for input_image_name in os.listdir(input_image_dir.get()):
            input_image_path = os.path.join(os.path.normcase(input_image_dir.get()), input_image_name)
            if not os.path.isfile(input_image_path):
                continue
            output_image_name = get_default_cropped_image_name(input_image_path)
            save_path = os.path.join(os.path.normcase(save_dir.get()), output_image_name)
            output_image = process_image(input_image_path, x_margin.get(), y_margin.get(),
                                         output_image_path = save_path, save_image = True)
        is_saved.set(f"Les images ont été sauvegardées à: \n{save_dir.get()}.")

