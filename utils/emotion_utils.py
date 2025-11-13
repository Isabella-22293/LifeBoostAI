import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import cv2
import numpy as np

# =====================================================
# Modelo convolucional de emociones
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
# Cargar modelo entrenado
# =====================================================
model = EmotionCNN()
model.load_state_dict(torch.load("models/emotion_model.pth", map_location="cpu"))
model.eval()

# Labels en inglés y diccionario a español
labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_MAP = {
    "angry": "enojado",
    "disgust": "asco",
    "fear": "miedo",
    "happy": "feliz",
    "sad": "triste",
    "surprise": "sorpresa",
    "neutral": "neutral"
}

# =====================================================
# Transformaciones de imagen
# =====================================================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# =====================================================
# Función para detectar y extraer la cara de la imagen
# =====================================================
def extract_face(image: Image.Image):
    img_cv = np.array(image.convert('RGB'))  # PIL -> OpenCV
    gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces) == 0:
        return None  # fallback si no detecta cara
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    face = Image.fromarray(face)
    return face

# =====================================================
# Función de predicción mejorada
# =====================================================
def predict_emotion(image: Image.Image):
    """Predice la emoción de una imagen facial (selfie o foto real)."""
    face = extract_face(image)
    if face is None:
        return "neutral"  # si no detecta cara

    img_tensor = transform(face).unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        pred_idx = torch.argmax(output, dim=1).item()
        emotion_en = labels[pred_idx]
        return EMOTION_MAP[emotion_en]
