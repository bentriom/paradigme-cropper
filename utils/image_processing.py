
import os
import rembg
from PIL import Image

def process_image(input_image_path, output_image_path = "", save_image = False):
    image_removed_bg = remove_background(input_image_path)
    image_output = blank_background(image_removed_bg)

    if save_image:
        assert os.path.isdir(os.path.dirname(output_image_path))
        if os.path.basename(input_image_path).split(".")[-1] in ["jpg", "JPG", "jpeg", "JPEG"]:
            image_output = image_output.convert("RGB")
        image_output.save(output_image_path)

    return image_output

def remove_background(input_image_path):
    assert os.path.isfile(input_image_path), "Given input image is not a file"
    image_input = Image.open(input_image_path)
    image_output = rembg.remove(image_input)

    return image_output

def blank_background(image):
    blank_bg_image = Image.new("RGBA", image.size, "WHITE")
    blank_bg_image.paste(image, (0, 0), image)

    return blank_bg_image

