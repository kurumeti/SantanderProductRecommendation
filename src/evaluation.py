'''
Functions for evaluation, taken mostly from competition website.

Created on 3.11.2016

@author: Jesse
'''
import numpy as np


    
def mapk(actual, predicted, k=7):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return(np.mean([apk(a,p,k) for a,p in zip(actual, predicted)]))

def apk(actual, predicted, k=7):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if actual is None or len(actual) == 0:
        return 0.0

    if predicted is None or len(predicted) == 0:
        return 0.0

    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    return(score / min(len(actual), k))

# This can be used as custom evaluation function for xgboost
def map7eval(preds, dtrain):
    actual = dtrain.get_label()
    actual = [[e] for e in actual]
    predicted = preds.argsort()[:,::-1][:,:7].tolist()
    #print(actual)
    #print(predicted)
    return("MAP@7",mapk(actual,predicted))
