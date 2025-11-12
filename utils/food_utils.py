import torch
from torchvision import models, transforms
from PIL import Image
import json

# Cargar etiquetas
with open("models/food_labels.json", "r") as f:
    labels = json.load(f)

# Modelo ResNet18
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(labels))
model.load_state_dict(torch.load("models/food_model.pth", map_location='cpu'))
model.eval()

transform = transforms.Compose([
    transforms.Resize((64,64)),
    transforms.ToTensor()
])

def predict_food(image: Image.Image):
    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(img)
        pred = torch.argmax(output, 1).item()
    return labels[pred]
