
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot

import plot_db


def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    file_name = sys.argv[1]
    out_filename = sys.argv[2]
    outfile = open(out_filename, "w")
    training_data = pd.read_csv(file_name, names=['age', 'weight', 'height'])
    features = ['age', 'weight']
    n = training_data.shape[0]
    training_data['b'] = 1
    costs = []

    no_of_iterations = 100
    required_learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    learning_rate_list = required_learning_rates
    actual_height = training_data['height'].to_numpy()

    for feature in features:
        mean = training_data[feature].mean()
        std_deviation= training_data[feature].std()
        training_data[feature] = (training_data[feature] - mean)/float(std_deviation)
    features_for_training = features + ['b']

    for learning_rate in learning_rate_list:
        weights = np.zeros(training_data.shape[1] - 1)
        for i in range(no_of_iterations):
            predicted_height = np.dot(training_data[features_for_training].to_numpy(), weights)
            cost = (1/(2*float(n))) * np.sum(np.square(predicted_height - actual_height))
            for j in range(len(weights)):
                weights[j] = weights[j] - (1 / float(n)) * learning_rate * (
                            training_data[features_for_training[j]].to_numpy().dot(
                                predicted_height - actual_height))
        costs.append(cost)
        if learning_rate in required_learning_rates:
            outfile.write("{}, {}, {}, {}, {}".format(learning_rate, no_of_iterations, weights[2], weights[0], weights[1]))
            outfile.write("\n")
        print("learning rate:{}, cost:{}, weights:{}".format(learning_rate, cost, weights))
        weights_to_plot = [weights[2], weights[0], weights[1]]
        plot_db.visualize_3d(training_data, weights_to_plot, 'age', 'weight', 'height', (-2, 2), (-2, 2), (0, 2),
                             learning_rate, title="learning rate: {}, Iterations:{}, UNI: spa2138".format(learning_rate, no_of_iterations))
    print("minimum cost:{} at learning rate:{}".format(min(costs), learning_rate_list[costs.index(min(costs))]))

    new_learning_rate = 1.05
    new_no_of_iterations = 10000
    weights = np.zeros(training_data.shape[1] - 1)
    for i in range(new_no_of_iterations):
        predicted_height = np.dot(training_data[features_for_training].to_numpy(), weights)
        cost = (1/(2*float(n))) * np.sum(np.square(predicted_height - actual_height))
        for j in range(len(weights)):
            weights[j] = weights[j] - (1 / float(n)) * new_learning_rate * (
                training_data[features_for_training[j]].to_numpy().transpose().dot(
                    predicted_height - actual_height))
    weights_to_plot = [weights[2], weights[0], weights[1]]
    plot_db.visualize_3d(training_data, weights_to_plot, 'age', 'weight', 'height', (-2, 2), (-2, 2), (0, 2),
                         new_learning_rate,
                         title="learning rate: {}, Iterations:{}, UNI: spa2138".format(new_learning_rate, new_no_of_iterations))
    outfile.write("{}, {}, {}, {}, {}".format(new_learning_rate, new_no_of_iterations, weights[2], weights[0], weights[1]))
    print("new_learning_rate:{}, cost:{},  weights:{}".format(new_learning_rate, cost, weights))
    final_weights = [weights[2], weights[0], weights[1]]
    x_values = np.arange(len(learning_rate_list) - 2)
    cost_values = costs[:-2]
    pyplot.xticks(x_values, learning_rate_list[:- 2])
    pyplot.plot(x_values, cost_values)
    pyplot.xlabel('learning rate')
    pyplot.ylabel('cost')
    pyplot.title("Variation in cost wrt learning rate at 100 iterations")
    for i in range(len(x_values)):
        pyplot.annotate(cost_values[i].round(6), (x_values[i], cost_values[i]))
    pyplot.show()


if __name__ == "__main__":
    main()
