#Common functionalities for the whole project.
import os
import sys

import dill
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import seaborn as sns

from src.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix


def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        file_obj = open(file_path,"wb")
        dill.dump(obj,file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)

# Use grid search to find the best model hyperparameters and store their R2 scores in a dictionary
def evaluate_models(X_train, y_train, X_test,y_test,models, param):
    try:
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
            
def load_object(file_path):
    try:
        file_obj = open(file_path,"rb")
        return dill.load(file_obj)
        file_obj.close()
        
    except Exception as e:
        raise CustomException(e,sys)

def create_plot(y_test, y_pred, type, model_name, xlabel = "Actual Math Score", ylabel="Predicted Math Score", file_name = "Actual vs Predicted"):
    """
    A function to create a plot and save it to a file.
    """
    if type == "scatter":
        title = f"{model_name}'s Actual vs Predicted Values Scatterplot"
        plt.scatter(y_test, y_pred)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        directory = "./assets/images/"
        plt.savefig(f"{directory}{file_name}")
        
    elif type == "reg":
        title = f"{model_name}'s Actual vs Predicted Values Regplot"
        sns.regplot(x=y_test,y=y_pred,ci=None,color ='red');
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        directory = "./assets/images/"
        plt.savefig(f"{directory}{file_name}_regplot")