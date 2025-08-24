# model_training/train_model.py

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

# 1. Define Paths and Parameters
dataset_dir = 'brain_tumor_dataset'
img_height, img_width = 150, 150
batch_size = 32

# 2. Prepare the Data
# Use ImageDataGenerator to load images from directories and apply transformations
datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize pixel values to [0, 1]
    validation_split=0.2,    # Split data into 80% training and 20% validation
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',  # For two classes (yes/no)
    subset='training'     # Specify this is the training set
)

validation_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation' # Specify this is the validation set
)

# 3. Build the CNN Model
model = Sequential([
    # First convolutional block
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2, 2),

    # Second convolutional block
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    # Third convolutional block
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    # Flatten the results to feed into a dense layer
    Flatten(),

    # Dense layer for classification
    Dense(512, activation='relu'),
    # Dropout to prevent overfitting
    Dropout(0.5),
    # Output layer with a single neuron and sigmoid activation for binary classification
    Dense(1, activation='sigmoid')
])

# 4. Compile the Model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 5. Train the Model
print("Starting model training...")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=15,  # You can increase this for better accuracy, but it will take longer
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# 6. Save the Trained Model
# Save it in the main project directory so app.py can access it
model.save('../brain_tumor_model.h5')

print("Model training complete and model saved as brain_tumor_model.h5")