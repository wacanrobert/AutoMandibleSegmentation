import numpy as np
import pydicom
from PIL import Image
import os

def get_names(path):
    names = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in ['.dcm']:
                names.append(filename)
    return names

def convert_dcm_image(input_path, output_directory, name):
    dicom_path = os.path.join(input_path, name)
    im = pydicom.dcmread(dicom_path)

    im_array = im.pixel_array.astype(float)

    #im_array = im.pixel_array.astype(float)

    # Handle NaN values by setting them to 0
    im_array = np.nan_to_num(im_array)

    # Check if rescaling is necessary
    if im_array.min() < 0 or im_array.max() > 255:
        # Rescale to [0, 255] if necessary
        rescaled_image = ((im_array - im_array.min()) / (im_array.max() - im_array.min())) * 255
    else:
        # No rescaling needed
        rescaled_image = im_array
        # Set all non-black pixels to white
        threshold = 1  # Adjust this threshold based on your image characteristics
        rescaled_image[rescaled_image < threshold] = 0  # Set dark pixels to black
        rescaled_image[rescaled_image >= threshold] = 255  # Set other pixels to white
        

    final_image = np.uint8(rescaled_image)  # integers pixels

    final_image = Image.fromarray(final_image)

    output_path = os.path.join(output_directory, name + '.jpg')
    final_image.save(output_path)

def convert_dcm_image_two(input_path, output_directory, name):
    dicom_path = os.path.join(input_path, name)
    im = pydicom.dcmread(dicom_path)

    im_array = im.pixel_array.astype(float)

    # Handle NaN values by setting them to 0
    im_array = np.nan_to_num(im_array)

    # Check if rescaling is necessary
    if im_array.min() < 0 or im_array.max() > 255:
        # Rescale to [0, 255] if necessary
        rescaled_image = ((im_array - im_array.min()) / (im_array.max() - im_array.min())) * 255
    else:
        # No rescaling needed
        rescaled_image = im_array
        # Set all non-black pixels to white
        threshold = 1  # Adjust this threshold based on your image characteristics
        rescaled_image[rescaled_image < threshold] = 0  # Set dark pixels to black
        rescaled_image[rescaled_image >= threshold] = 255  # Set other pixels to white

    final_image = np.uint8(rescaled_image)  # integers pixels

    final_image = Image.fromarray(final_image)

    output_path = os.path.join(output_directory, name + '.jpg')
    final_image.save(output_path)

input_path = 'input_dicom/dicom'
output_directory = 'data/newjpg'  # Specify your desired output directory

input_path_two = 'input_dicom/dicommask'
output_directory_two = 'data/newjpgmask'

names = get_names(input_path)
for name in names:
    convert_dcm_image(input_path, output_directory, name)

names_two = get_names(input_path_two)
for name_two in names_two:
    convert_dcm_image_two(input_path_two, output_directory_two, name_two)