import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("dataset.csv")
data.fillna(0, inplace=True)
X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values
Y = Y.reshape(-1,1)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(12, activation="relu"),
    tf.keras.layers.Dense(50, activation="relu"),
    tf.keras.layers.Dense(20, activation="relu"),
    tf.keras.layers.Dense(4, activation="softmax"),
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
              loss="sparse_categorical_crossentropy", 
              metrics=["accuracy"])

history = model.fit(X_train, Y_train, epochs=300)
model.evaluate(X_test, Y_test)
model.save("snake_model.h5")