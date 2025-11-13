import os
import shutil

data_dir = "data/comida/food-101/food-101"
images_dir = os.path.join(data_dir, "images")
meta_dir = os.path.join(data_dir, "meta")

train_txt = os.path.join(meta_dir, "train.txt")
test_txt = os.path.join(meta_dir, "test.txt")

train_output = os.path.join("data/comida/train")
test_output = os.path.join("data/comida/test")

# Crear carpetas
os.makedirs(train_output, exist_ok=True)
os.makedirs(test_output, exist_ok=True)

# Leer clases
with open(os.path.join(meta_dir, "classes.txt"), "r") as f:
    classes = [c.strip() for c in f.readlines()]

# Crear subcarpetas por clase
for cls in classes:
    os.makedirs(os.path.join(train_output, cls), exist_ok=True)
    os.makedirs(os.path.join(test_output, cls), exist_ok=True)

# Mover imágenes a train
with open(train_txt, "r") as f:
    for line in f:
        image = line.strip() + ".jpg"
        src = os.path.join(images_dir, image)
        dst = os.path.join(train_output, image.split("/")[0])
        shutil.copy(src, dst)

# Mover imágenes a test
with open(test_txt, "r") as f:
    for line in f:
        image = line.strip() + ".jpg"
        src = os.path.join(images_dir, image)
        dst = os.path.join(test_output, image.split("/")[0])
        shutil.copy(src, dst)

print("Dataset organizado correctamente!")
