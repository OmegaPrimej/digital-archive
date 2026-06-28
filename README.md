# Model.py
**BollywoodVideoGen Model README & Scripts**
**Model Overview:**
Generate Bollywood-style music videos using text prompts.
**Files Included:**
1. **`requirements.txt`**
```
tensorflow==2.8.0
opencv-python==4.5.5
moviepy==1.0.3
numpy==1.21.4
```
2. **`model.py`**
```python
import tensorflow as tf
from tensorflow import keras
from keras.layers import *
class BollywoodVideoGen(keras.Model):
    def __init__(self):
        super(BollywoodVideoGen, self).__init__()
        self.encoder = keras.layers.LSTM(128)
        self.decoder = keras.layers.LSTM(128)
        self.dense = keras.layers.Dense(256)
    def call(self, inputs):
        encoded = self.encoder(inputs)
        decoded = self.decoder(encoded)
        output = self.dense(decoded)
        return output
```
3. **`data_loader.py`**
```python
import numpy as np
import cv2
def load_data(video_path, caption_path):
    cap = cv2.VideoCapture(video_path)
    captions = open(caption_path, 'r').readlines()
    return cap, captions
```
4. **`trainer.py`**
```python
from model import BollywoodVideoGen
from data_loader import load_data
def train(model, data_loader):
    for epoch in range(10):
        for video, captions in data_loader:
            with tf.GradientTape() as tape:
                output = model(video)
                loss = tf.reduce_mean(tf.square(output - captions))
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

**BOLLYWOOD VIDEO GENERATOR INSTALLER**
 Select installation option: 
```
------------------------------------------
|  **1. FULL INSTALLATION COMPLETE**     |
|  **2. MINIMAL INSTALLATION ESSENTIALS** |
|  **3. CUSTOM INSTALLATION CHOOSE OWN**  |
|  **4. DOWNLOAD BOLLYWOOD DATASET NOW**  |
|  **5. USE LOCAL DATASET ALREADY OWNED** |
|  **6. CHANGE INSTALL LOCATION CUSTOM**  |
|  **7. CHANGE INSTALL USER PERMISSIONS** |
|  **8. START INSTALLATION LET'S DANCE**  |
|  (left only 9 unchanged for exit)
------------------------------------------
```
Type number to select option 😄
