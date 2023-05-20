from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import numpy as np
import pandas as pd
import pickle
import joblib

from pointCalculations import Calculations
from dataGen import DataManager

class RandomForest():
    def __init__(self, latitude):
        self.latitude = latitude
        self.manager = DataManager()
        self.calculator = Calculations()

    def train(self):
        """
        Realiza o Treinamento da Rede Neural, e guarda o modelo gerado em um arquivo pkl
        """
        X, Y = self.manager.read_data()
        X_train, X_test, Y_train, Y_teste = train_test_split(X, Y, test_size=0.2)
        with open('rf_train_test.pkl', mode='wb') as f:
            pickle.dump([X_train, X_test, Y_train, Y_teste], f)

        rf_regressor = RandomForestRegressor(max_depth=6, max_features='sqrt', max_leaf_nodes=9,
                        n_estimators=50)
        rf_regressor.fit(X_train.values, Y_train)
        joblib.dump(rf_regressor, 'RFmodel.pkl')
        score = rf_regressor.score(X_train,Y_train)
        return round(score, 2)

    def make_predict(self, ha=None, dec=None, temp=None):
        """
        :param ha: Angulo Horario do alvo ()
        :param dec: Declinacao do alvo 
        :param temp: Temperatura Graus Centigrados
        :return: ha e DEC previstos
        """
        rf = joblib.load('RFmodel.pkl')

        #PREVISAO
        temp = temp if isinstance(temp, (int, float)) else 15 
        ha, dec, az, elevation = self.calculator.get_elevation_azimuth(ha, dec, self.latitude)
        X_futuro = np.array([[az, elevation, ha, dec, temp]])
        Y_rna_prever_futuro = rf.predict(X_futuro)
        fator_correct_ha = Y_rna_prever_futuro[0][0]
        fator_correct_dec = Y_rna_prever_futuro[0][1]

        new_ha = ha-fator_correct_ha
        new_dec = dec-fator_correct_dec

        return (new_ha, new_dec)

    def tunning_hp(self):
        X, Y = self.manager.read_data()
        param_grid = {
            'n_estimators': [25, 50, 100, 150],
            'max_features': ['sqrt', 'log2', None],
            'max_depth': [3, 6, 9],
            'max_leaf_nodes': [3, 6, 9],
        }
        grid_search = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid)
        grid_search.fit(X, Y)
        best_params = grid_search.best_estimator_
        best_score = grid_search.best_score_

        return (best_params, best_score)

