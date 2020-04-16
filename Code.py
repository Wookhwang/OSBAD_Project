from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import tensorflow as tf

# 데이터 값 로드
dataset = np.loadtxt("ThoraricSurgery.csv", delimiter=",")


