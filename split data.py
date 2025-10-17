import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import random

# Set random seed for reproducibility
random.seed(42)

# Original dataset paths
TRAIN_DIR = "Jute_Pest_Dataset/train"
VALID_DIR = "Jute_Pest_Dataset/val"
TEST_DIR = "Jute_Pest_Dataset/test"

# New dataset paths
NEW_TRAIN_DIR = "Jute_Pest_Dataset_Split/train"
NEW_VALID_DIR = "Jute_Pest_Dataset_Split/val"
NEW_TEST_DIR = "Jute_Pest_Dataset_Split/test"

def collect_all_images(base_dirs):
    """Collect all images from all directories organized by class"""
    all_images = {}
    
    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            print(f"Warning: {base_dir} does not exist, skipping...")
            continue
            
        # Get all class folders
        class_folders = [f for f in os.listdir(base_dir) 
                        if os.path.isdir(os.path.join(base_dir, f))]
        
        for class_name in class_folders:
            class_path = os.path.join(base_dir, class_name)
            
            # Initialize class list if not exists
            if class_name not in all_images:
                all_images[class_name] = []
            
            # Get all image files
            images = [os.path.join(class_path, f) 
                     for f in os.listdir(class_path)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            
            all_images[class_name].extend(images)
    
    return all_images

def split_and_copy_images(all_images, train_dir, valid_dir, test_dir, 
                          train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    """Split images into train/val/test and copy to new directories"""
    
    # Create output directories
    for directory in [train_dir, valid_dir, test_dir]:
        os.makedirs(directory, exist_ok=True)
    
    print("\nSplitting dataset with ratio 70-15-15...")
    print("="*60)
    
    for class_name, images in all_images.items():
        print(f"\nProcessing class: {class_name}")
        print(f"Total images: {len(images)}")
        
        # Shuffle images
        random.shuffle(images)
        
        # Calculate split sizes
        total = len(images)
        train_size = int(total * train_ratio)
        valid_size = int(total * valid_ratio)
        
        # Split images
        train_images = images[:train_size]
        valid_images = images[train_size:train_size + valid_size]
        test_images = images[train_size + valid_size:]
        
        print(f"  Train: {len(train_images)}")
        print(f"  Valid: {len(valid_images)}")
        print(f"  Test: {len(test_images)}")
        
        # Copy images to new directories
        for img_list, target_dir in [(train_images, train_dir),
                                      (valid_images, valid_dir),
                                      (test_images, test_dir)]:
            class_dir = os.path.join(target_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            
            for img_path in img_list:
                img_name = os.path.basename(img_path)
                target_path = os.path.join(class_dir, img_name)
                shutil.copy2(img_path, target_path)
    
    print("\n" + "="*60)
    print("Dataset split completed successfully!")

def main():
    print("Starting dataset redistribution...")
    print("="*60)
    
    # Collect all images from original directories
    original_dirs = [TRAIN_DIR, VALID_DIR, TEST_DIR]
    all_images = collect_all_images(original_dirs)
    
    if not all_images:
        print("Error: No images found in the specified directories!")
        return
    
    print(f"\nFound {len(all_images)} classes:")
    for class_name, images in all_images.items():
        print(f"  {class_name}: {len(images)} images")
    
    # Split and copy images
    split_and_copy_images(all_images, NEW_TRAIN_DIR, NEW_VALID_DIR, NEW_TEST_DIR)
    
    print(f"\nNew dataset saved to:")
    print(f"  Train: {NEW_TRAIN_DIR}")
    print(f"  Valid: {NEW_VALID_DIR}")
    print(f"  Test: {NEW_TEST_DIR}")

if __name__ == "__main__":
    main()