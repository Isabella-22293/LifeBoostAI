import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
import os

# =====================================================
# Transformaciones con Data Augmentation
# =====================================================
train_transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomResizedCrop(48, scale=(0.9, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

val_transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# =====================================================
# Dataset y división train/validación
# =====================================================
dataset = datasets.ImageFolder("data/emociones/train", transform=train_transform)
num_classes = len(dataset.classes)

val_size = int(0.2 * len(dataset))
train_size = len(dataset) - val_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Cambiar transform del conjunto de validación
val_dataset.dataset.transform = val_transform

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

print(f" Dataset dividido: {train_size} entrenamiento / {val_size} validación")
print(f"Clases detectadas: {dataset.classes}")

# =====================================================
# Modelo CNN
# =====================================================
class EmotionCNN(nn.Module):
    def __init__(self, num_classes=7):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# =====================================================
# Entrenamiento con validación
# =====================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EmotionCNN(num_classes=num_classes).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
epochs = 20
best_val_acc = 0

print("\n Entrenando modelo mejorado de emociones...\n")

for epoch in range(epochs):
    model.train()
    train_loss = 0
    correct_train = 0
    total_train = 0

    for imgs, labels in tqdm(train_loader, desc=f"Época {epoch+1}/{epochs}"):
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total_train += labels.size(0)
        correct_train += predicted.eq(labels).sum().item()

    train_acc = 100. * correct_train / total_train

    # -----------------------------
    # Validación
    # -----------------------------
    model.eval()
    val_loss = 0
    correct_val = 0
    total_val = 0
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, predicted = outputs.max(1)
            total_val += labels.size(0)
            correct_val += predicted.eq(labels).sum().item()

    val_acc = 100. * correct_val / total_val

    print(f"→ Época {epoch+1}/{epochs} | "
          f"Pérdida Entrenamiento: {train_loss/len(train_loader):.4f} | "
          f"Precisión Entrenamiento: {train_acc:.2f}% | "
          f"Precisión Validación: {val_acc:.2f}%")

    # Guardar mejor modelo
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), "models/emotion_model.pth")
        print(f" Nuevo mejor modelo guardado (Accuracy Validación: {val_acc:.2f}%)")

print("\n Entrenamiento finalizado. Mejor accuracy de validación:", best_val_acc)
