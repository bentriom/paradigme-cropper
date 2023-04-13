
import os
import rembg
import numpy as np
from PIL import Image

def process_image(input_image_path, x_margin, y_margin, output_image_path = "", save_image = False):
    image_removed_bg = remove_background(input_image_path)
    image_blank_bg = blank_background(image_removed_bg)
    image_output = new_margins(image_blank_bg, x_margin, y_margin)

    if save_image:
        assert os.path.isdir(os.path.dirname(output_image_path))
        # if os.path.basename(input_image_path).split(".")[-1] in ["jpg", "JPG", "jpeg", "JPEG"]:
        #     image_output = image_output.convert("RGB")
        image_output.save(output_image_path, "PNG")

    return image_output

def remove_background(input_image_path):
    assert os.path.isfile(input_image_path), f"Given input image is not a file: {input_image_path}"
    image_input = Image.open(input_image_path)
    image_output = rembg.remove(image_input)

    return image_output

def blank_background(image):
    blank_bg_image = Image.new("RGBA", image.size, "WHITE")
    blank_bg_image.paste(image, (0, 0), image)

    return blank_bg_image

def new_margins(image, x_margin, y_margin):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    image_array = np.asarray(image)
    full_white_x_coord = np.where([not (image_array[:, i, :] == [255, 255, 255, 255]).all()
                                   for i in range(image.size[0])])[0]
    full_white_y_coord = np.where([not (image_array[j, :, :] == [255, 255, 255, 255]).all()
                                   for j in range(image.size[1])])[0]
    coord_begin_image = np.asarray((np.min(full_white_x_coord), np.min(full_white_y_coord)))
    coord_end_image = np.asarray((np.max(full_white_x_coord), np.max (full_white_y_coord)))
    cropped_image = image.crop((coord_begin_image[0], coord_begin_image[1], coord_end_image[0], coord_end_image[1]))
    image_with_margins = Image.new("RGBA",
                                   (cropped_image.size[0]+2*x_margin, cropped_image.size[1]+2*y_margin), "WHITE")
    image_with_margins.paste(cropped_image, (x_margin, y_margin))

    return image_with_margins

