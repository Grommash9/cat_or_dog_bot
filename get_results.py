import os

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout


checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

train, _ = tfds.load('cats_vs_dogs', split=['train[:100%]'], with_info=True, as_supervised=True)

SIZE = 224


def resize_image(img, label):
  img = tf.cast(img, tf.float32)
  img = tf.image.resize(img, (SIZE, SIZE))
  img = img / 255.0
  return img, label


base_layers = tf.keras.applications.MobileNetV2(input_shape=(SIZE, SIZE, 3), include_top=False)
base_layers.trainable = False

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


model = tf.keras.Sequential([base_layers,
                             GlobalAveragePooling2D(),
                             Dropout(0.2),
                             Dense(1)])

model.load_weights(checkpoint_path)