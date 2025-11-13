import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import json

transform = transforms.Compose([
    transforms.Resize((64,64)),
    transforms.ToTensor()
])

train_dataset = datasets.ImageFolder("data/comida/train", transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(train_dataset.classes))

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

print("Entrenando modelo de comida...")

for epoch in range(4):
    for imgs, labels in train_loader:
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/4 completada")

torch.save(model.state_dict(), "models/food_model.pth")

with open("models/food_labels.json", "w") as f:
    json.dump(train_dataset.classes, f)

print("Modelo guardado en models/food_model.pth y food_labels.json")
