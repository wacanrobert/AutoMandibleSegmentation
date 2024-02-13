import SimpleITK as sitk
from PIL import Image
import numpy as np
import os

def convert_images_to_nrrd(png_folder, nrrd_output_path):
    # Get a list of all PNG files in the specified folder
    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]

    # Load the first PNG image to extract voxel spacing information
    first_png_path = os.path.join(png_folder, png_files[0])
    first_png_image = Image.open(first_png_path)
    first_png_array = np.array(first_png_image)
    first_itk_image = sitk.GetImageFromArray(first_png_array)

    # Get the voxel spacing from the first image
    voxel_spacing = first_itk_image.GetSpacing()

    # Initialize an empty list to store SimpleITK images
    itk_images = []

    # Load each PNG image, convert to NumPy array, and create SimpleITK image
    for png_file in png_files:
        png_image_path = os.path.join(png_folder, png_file)
        png_image = Image.open(png_image_path)
        png_array = np.array(png_image)
        itk_image = sitk.GetImageFromArray(png_array)

        # Set voxel spacing for each image
        itk_image.SetSpacing(voxel_spacing)

        itk_images.append(itk_image)

    # Concatenate the list of images into a single 3D image
    itk_3d_image = sitk.JoinSeries(itk_images)

    # Save the 3D image as NRRD
    sitk.WriteImage(itk_3d_image, nrrd_output_path)

# Specify the folder containing PNG images and the output NRRD file
png_folder = 'jpgtodicom/jpg'
nrrd_output_path = 'jpgtodicom/output/img.nrrd'

# Run the conversion function
convert_images_to_nrrd(png_folder, nrrd_output_path)
