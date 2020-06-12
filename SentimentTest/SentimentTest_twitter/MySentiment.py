import json
import nltk
import numpy as np
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics

class Sentiment:
    def __init__(self, file_name):
        with open(file_name, encoding='UTF8') as json_file:
            self.train_docs = json.load(json_file)
        tokens = [t for d in self.train_docs for t in d[0]]

        text = nltk.Text(tokens, name='NMSC')
        print(text)
        self.selected_words = [f[0] for f in text.vocab().most_common(100)]

    def make_model(self, model_name):
        train_x = [self.term_frequency(d) for d, _ in self.train_docs]
        train_y = [c for _, c in self.train_docs]

        x_train = np.asarray(train_x).astype('float32')
        y_train = np.asarray(train_y).astype('float32')

        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(100,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                      loss=losses.binary_crossentropy,
                      metrics=[metrics.binary_accuracy])
        model.fit(x_train, y_train, epochs=10, batch_size=512)
        results = model.evaluate(x_train, y_train)
        print(results)
        model.save(model_name)

    def term_frequency(self, doc):
        return [doc.count(word) for word in self.selected_words]







