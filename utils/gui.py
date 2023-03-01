
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

## Helpers for picture displays

def get_visualized_image_size(image_size, window_size):
    window_width, window_height = window_size[0], window_size[1]
    new_width = int(min(0.95 * (window_width / 2), image_size[0]))
    # new_height = int((new_width / image_size[0]) * image_size[1])
    new_height = int(min(0.55 * window_height, image_size[0]))

    return (new_width, new_height)

def resize_input_image(input_image_path, input_image_visualizer, window_size):
    if input_image_path.get() != "":
        input_image = Image.open(input_image_path.get())
        input_image = input_image.resize(get_visualized_image_size(input_image.size, window_size))
        photo_input_image = ImageTk.PhotoImage(input_image)
        input_image_visualizer.configure(image = photo_input_image)
        input_image_visualizer.photo_image = photo_input_image

def show_cropped_image(input_image_path, output_image_visualizer, window_size):
    if input_image_path.get() != "":
        output_image = process_image(input_image_path.get(), save_image = False)
        output_image = output_image.resize(get_visualized_image_size(output_image.size, window_size))
        photo_output_image = ImageTk.PhotoImage(output_image)
        output_image_visualizer.configure(image = photo_output_image)
        output_image_visualizer.image = photo_output_image

def get_default_cropped_image_name(image_path):
        splitted_input_image_name = os.path.basename(image_path).split(".")
        image_cropped_name = splitted_input_image_name[0] + "_cropped." + '.'.join(splitted_input_image_name[1:])

        return image_cropped_name

## Helpers for image browsing / saving

def browse_image(input_image_path, input_image_visualizer, window_size):
    # Open image
    file_image = filedialog.askopenfile(initialdir = "./", title = "Sélection d'une image",
                                        filetypes = (("PNG files", "*.png"),
                                                     ("JPEG files", "*.jpg *.jpeg")))
    # Update label and visualisation
    if file_image is not None:
        input_image_path.set(file_image.name)
        resize_input_image(input_image_path, input_image_visualizer, window_size)

def browse_output_dir(input_image_path, save_path):
    output_dir = filedialog.askdirectory(initialdir = "./", title = "Sélection de dossier")
    output_image_name = get_default_cropped_image_name(input_image_path.get())
    save_path.set(os.path.join(output_dir, output_image_name))

def save_cropped_image(input_image_path, save_path, is_saved):
    if (input_image_path.get() == ""):
        is_saved.set(f"Choisissez une image à traiter et un dossier de sauvegarde.")
    elif (save_path.get() == ""):
        is_saved.set(f"Choisissez un dossier de sauvegarde.")
    elif not os.path.isdir(os.path.dirname(save_path.get())):
        is_saved.set(f"Dossier de sauvegarde inexisant: {save_path.get()}.")
    else:
        is_saved.set("Sauvegarde en cours...")
        output_image = process_image(input_image_path.get(), save_path.get(), save_image = True)
        is_saved.set(f"L'image a été sauvegardé à: \n{save_path.get()}.")

