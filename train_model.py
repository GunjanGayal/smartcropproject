import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json   # NEW

# ---------------- Parameters ----------------
dataset_path = r"C:\SmartCropProject\dataset\plantvillage dataset\color"
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 10
MODEL_PATH = r"C:\SmartCropProject\plant_disease_model.h5"

# ---------------- Check dataset path ----------------
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset path not found: {dataset_path}")

# ---------------- Data Generator ----------------
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# ---------------- Classes ----------------
class_indices = train_data.class_indices
class_names = list(class_indices.keys())

print("Detected Classes:")
print(class_names)

# -------- NEW (class names save) --------
with open("class_names.json","w") as f:
    json.dump(class_names,f)

# ---------------- CNN Model ----------------
model = models.Sequential([

    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),

    layers.Dense(len(class_names), activation='softmax')
])

# ---------------- Compile ----------------
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ---------------- Train ----------------
print("\nStarting training...\n")

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ---------------- Save Model ----------------
model.save(MODEL_PATH)

print("\n✅ Model trained successfully!")
print(f"Model saved at: {MODEL_PATH}")