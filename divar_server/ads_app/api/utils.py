
# This is a prebuilt AI model that classifies car photos into classes. 
# but I didn't use it in my projet code because it's not developed for Iranian cars or cars being used in Iran mostly.
# ---------------------------------------------------------------------

import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import urllib.request
import os

def predict_image(image_file):
    # Load the pre-trained MobileNetV2 model
    model = models.mobilenet_v2(pretrained=True)
    model.eval()

    url = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
    filename = 'imagenet_classes.txt'

    # Check if the file already exists
    if not os.path.exists(filename):
        try:
            # Download the file only if it doesn't exist yet
            urllib.request.urlretrieve(url, filename)
            print("Downloaded ImageNet class labels.")
        except Exception as e:
            print(f"Error downloading ImageNet class labels: {e}")
            return  # Exit the function if the download fails
        
    with open(filename) as f:
        classes = [line.strip() for line in f.readlines()]
    
    # Preprocessing for the image
    transform = transforms.Compose([
        transforms.Resize(256),  # Resize to 256 pixels
        transforms.CenterCrop(224),  # Crop the center 224x224 square
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize(  # Normalize the image (based on ImageNet's stats)
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Load and prepare the image
    img = Image.open(image_file)
    img = img.convert('RGB')  # Ensure image is in RGB mode
    img_t = transform(img)  # Apply transformations
    batch_t = torch.unsqueeze(img_t, 0)  # Add batch dimension (batch size of 1)

    # Perform the prediction
    with torch.no_grad():
        out = model(batch_t)

    
    # Get the predicted class index
    _, index = torch.max(out, 1)
    predicted_class = classes[index[0]]
    print(predicted_class)

    vehicle_classes = ['car', 'ambulance', 'truck', 'motorcycle']
    if any(vehicle in predicted_class.lower() for vehicle in vehicle_classes):
        return True
    else:
        return False