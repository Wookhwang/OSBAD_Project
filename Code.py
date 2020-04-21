from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 예측 실행
# seed 값 생성
# 현재 4로 할때가 가장 정확한  Accuracy: 0.7188 이 나온다.
np.random.seed(4)
tf.random.set_seed(4)

df =pd.read_csv('P3.csv', names = ["Man", "Women","20", "30", "40", "50", "60","Win"], encoding='utf-8')

sns.pairplot(df, hue='Candidate');
plt.show()

dataset = df.values
X = dataset[:, 0:7].astype(float)
Y_Obj = dataset[:,7]

e = LabelEncoder()
e.fit(Y_Obj)
Y = e.transform(Y_Obj)
Y_encoded = tf.keras.utils.to_categorical(Y)

model = Sequential()
model.add(Dense(8, input_dim=7, activation='relu'))
model.add(Dense(6, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

model.fit(X, Y_encoded, epochs=50, batch_size=1)

print("\n Accuracy: %.4f" % (model.evaluate(X, Y_encoded)[1]))

