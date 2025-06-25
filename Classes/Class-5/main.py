import tensorflow as tf
from keras import layers, models

import matplotlib.pyplot as plt

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize the data to range 0-1
x_train, x_test = x_train / 255.0, x_test / 255.0

# Build the model
model = models.Sequential([
layers.Flatten(input_shape=(28, 28)), # Flatten 28x28 images to 784 values
layers.Dense(128, activation='relu'), # Hidden layer with 128 neurons
layers.Dense(10, activation='softmax') # Output layer for 10 digits (0-9)
])

# Compile the model
model.compile(
optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy']
)

# Train the model
model.fit(x_train, y_train, epochs=1)

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc}")

# Make predictions
predictions = model.predict(x_test)

# Display the first image and its prediction
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.title(f"Predicted: {predictions[0].argmax()}")
plt.axis('off')
plt.show()
