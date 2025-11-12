import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

# Modelo idéntico al entrenamiento
class EmotionNet(nn.Module):
    def __init__(self, num_classes=7):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(48*48, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
    def forward(self, x):
        return self.fc(x)

model = EmotionNet()
model.load_state_dict(torch.load("models/emotion_model.pth", map_location='cpu'))
model.eval()

labels = ['angry','disgust','fear','happy','sad','surprise','neutral']

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48,48)),
    transforms.ToTensor()
])

def predict_emotion(image: Image.Image):
    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(img)
        pred = torch.argmax(output, dim=1).item()
    return labels[pred]
