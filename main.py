# Updated main.py with additional comments

# Import necessary libraries
import numpy as np
import tensorflow as tf

# Define a function to create a model

def create_model():
    # Create a sequential model
    model = tf.keras.Sequential()
    # Add layers to the model
    model.add(tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)))  # Input layer
    model.add(tf.keras.layers.Dense(10, activation='softmax'))  # Output layer
    return model

# Compile the model
model = create_model()
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()