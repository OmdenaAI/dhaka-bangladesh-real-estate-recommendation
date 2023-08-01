import pandas as pd
import numpy as np

import tensorflow as tf

import matplotlib.pyplot as plt

from typing import List, Tuple


def mae(y_true, y_pred):
    """
        @param y_true: (real) labels
        @param y_pred: predicted labels
    """
    return tf.metrics.mean_absolute_error(y_true=y_true, y_pred = y_pred)

def mse(y_true, y_pred):
    """
        @param y_true: (real) labels
        @param y_pred: predicted labels
    """
    return tf.metrics.mean_squared_error(y_true=y_true, y_pred=y_pred)

# def plot_training_history(history:dict, plot_title:str, plot_xlabel:str="Epochs", plot_size:Tuple[int,int]=None,)->None:
#     # Looking at the content of the model training history
#     history_df = pd.DataFrame(history)
#     print("history_df.head()")
#     print(history_df.head())

#     # Model 9 performance
#     history_df.plot(figsize=plot_size) #(figsize=(8,6))

#     plt.xlabel(plot_xlabel)
#     plt.title(plot_title);


def plot_training_history(history:tf.keras.callbacks.History, plot_title:str, plot_xlabel:str="Epochs", plot_size:Tuple[int,int]=None,
                          metrics_to_plot:List[str]=None)->None:
    # Looking at the content of the model training history
    history_df = pd.DataFrame(history.history)
    print("history_df.head()")
    print(history_df.head())

    if metrics_to_plot is not None:
        history_df = history_df.loc[:, metrics_to_plot]

    # Model 9 performance
    history_df.plot(figsize=plot_size) #(figsize=(8,6))

    plt.xlabel(plot_xlabel)
    plt.title(plot_title);


def plot_predictions(train_X, train_labels,
                    test_X, test_labels,
                    predictions):
    """
        Plots training data, test data, and compares predictions to ground truth labels.
    """
    plt.figure( figsize=(10,7) )

    if train_X is not None and train_labels is not None:
        # Plot training data in blue 
        plt.scatter(train_X, train_labels, c="b", label="Training data")

    if test_X is not None and test_labels is not None:
        # Plot test data in green
        plt.scatter(test_X, test_labels, c="g", label="Test data")
    
    if test_X is not None and predictions is not None:
        # Plot prediction data
        plt.scatter(test_X,predictions,c="r", label="Predictions")

    #Show a legend
    plt.legend(); 
