import pandas as pd
import numpy as np
import sys
import plot_db


def main():
    '''YOUR CODE GOES HERE'''
    file_name = sys.argv[1]
    out_filename = sys.argv[2]
    outfile = open(out_filename, "w")
    training_data = pd.read_csv(file_name, names=['feature1', 'feature2', 'label'])
    weights = np.zeros(training_data.shape[1])
    training_data['b'] = 1

    while True:
        previous_weights = weights.copy()
        for index, row in training_data.iterrows():
            features = np.asarray([row['feature1'], row['feature2'], row['b']])
            label = row['label']
            prediction = np.dot(features, weights)
            if prediction*label <= 0:
                weights[0] = weights[0] + label * features[0]
                weights[1] = weights[1] + label * features[1]
                weights[2] = weights[2] + label * features[2]
        outfile.write("{}, {}, {}".format(weights[0], weights[1], weights[2]))
        outfile.write('\n')
        if previous_weights[0] == weights[0] and previous_weights[1] == weights[1] and previous_weights[2] == weights[
            2]:
            break
    plot_db.visualize_scatter(training_data, 'feature1', 'feature2', 'label', weights=weights, title="Perceptron Decision Boundary (UNI: spa2138)")

if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()