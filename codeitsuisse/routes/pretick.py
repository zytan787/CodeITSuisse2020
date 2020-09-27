import logging
import json
import numpy as np

# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler, FunctionTransformer
# from sklearn.linear_model import LinearRegression

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


class InputPipeline:

    def __init__(self, data, n_list):
        self.n_list = n_list
        self.target_column = 3
        self.original_features = data[:, [0, 1, 2, 4]]
        self.original_labels = data[:, self.target_column].flatten()
        self.X_train, self.X_test = self.preprocess()
        self.y_train = np.array(self.original_labels[2:])

    def preprocess(self):
        total = len(self.original_labels[:])
        all_mean = list()
        all_std = list()
        max_n = max(self.n_list)
        for i in range(1, total):
            mean_n = list()
            std_n = list()
            if i < max_n:
                l = self.original_labels[0:i]
            else:
                l = self.original_labels[i - max_n:i]
            for n in self.n_list:
                mean_n += [np.mean(l[-n:])]
                std_n += [np.std(l[-n:])]
            all_mean.append(mean_n)
            all_std.append(std_n)
        all_data = np.hstack((all_mean, all_std))
        return all_data[:-1], all_data[-1:]

    def get_train_input(self):
        return self.X_train, self.y_train

    def get_test_input(self):
        return self.X_test


@app.route('/pre-tick', methods=['POST'])
def preTick():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))
    data = data.decode('utf-8').split("\n")[1:]
    for i in range(len(data)):
        data[i] = list(map(float, data[i].strip().split(",")))
    data = np.array(data)

    input_pipeline = InputPipeline(data, [5, 10, 15, 20, 30, 40, 50])
    X_train, y_train = input_pipeline.get_train_input()
    X_test = input_pipeline.get_test_input()
    print(X_train.shape, y_train.shape, X_test.shape)

    linear_regressor = LinearRegression()
    linear_regressor.fit(X_train, y_train)
    prediction = linear_regressor.predict(X_test)[0]

    logging.info("My result :{}".format(prediction))
    return json.dumps(prediction)



