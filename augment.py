import os
import cv2
import numpy as np
np.bool = bool 
from imgaug import augmenters as iaa
from tqdm import tqdm

# Path to the parent folder containing all subfolders
parent_folder_path = 'images'  # Replace with your parent folder path

# Augmentation configurations
augmenters = iaa.SomeOf((2, 4), [  # Apply 2 to 4 augmentations from the list
    iaa.Fliplr(0.5),              # Horizontal flip with 50% probability
    iaa.Affine(rotate=(-45, 45)), # Rotate between -45 to 45 degrees
    iaa.Multiply((0.8, 1.2)),     # Random brightness adjustment
    iaa.GaussianBlur(sigma=(0, 1.0)),  # Add Gaussian blur
    iaa.AdditiveGaussianNoise(scale=(10, 30)),  # Add Gaussian noise
    iaa.Sharpen(alpha=(0.2, 0.5), lightness=(0.8, 1.2)),  # Sharpen the image
    iaa.Crop(percent=(0, 0.1)),   # Random cropping
    iaa.LinearContrast((0.75, 1.5)),  # Change contrast
    iaa.SomeOf((0, 1), [           # Optional grayscale conversion
        iaa.Grayscale(alpha=1.0)   # Convert to grayscale with 100% probability
    ])
])

def augment_images_in_subfolders(parent_folder):
    # Get all subfolders (ids) in the parent folder
    subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
    if not subfolders:
        print(f"No subfolders found in '{parent_folder}'.")
        return

    for subfolder in subfolders:
        subfolder_path = os.path.join(parent_folder, subfolder)
        images = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not images:
            print(f"No valid images found in subfolder: {subfolder}")
            continue

        print(f"Processing {len(images)} images in subfolder: {subfolder}")
        for img_name in tqdm(images, desc=f"Augmenting {subfolder}"):
            img_path = os.path.join(subfolder_path, img_name)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Warning: Could not read image {img_name}")
                continue

            # Generate 50 augmented versions of the image
            for i in range(1, 51):
                aug_img = augmenters(image=img)
                save_name = f"{os.path.splitext(img_name)[0]}_aug{i}.jpg"
                save_path = os.path.join(subfolder_path, save_name)
                cv2.imwrite(save_path, aug_img)

            # Optional: Add grayscale version (this is a custom augmentation added separately)
            grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayscale_path = os.path.join(subfolder_path, f"{os.path.splitext(img_name)[0]}_grayscale.jpg")
            cv2.imwrite(grayscale_path, grayscale_img)

    print("Augmentation complete!")

# Call the function to augment images
augment_images_in_subfolders(parent_folder_path)
