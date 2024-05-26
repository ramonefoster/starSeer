from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import MinMaxScaler

import numpy as np
import pickle
import joblib

from starSeer.dataGen import DataManager
from starSeer.constants import *
from starSeer.utils import Utils

class StarSeer():
    @staticmethod
    def train():
        """
        Perform training of the neural network and save the generated model to a pickle file.

        Returns:
            float: The training score rounded to 2 decimal places.

        """       
        X, Y = DataManager.read_data()      
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        scaler_X = MinMaxScaler()
        scaler_Y = MinMaxScaler()

        # Fit and transform training data
        X_train_scaled = scaler_X.fit_transform(X_train)
        Y_train_scaled = scaler_Y.fit_transform(Y_train)

        # Transform testing data
        X_test_scaled = scaler_X.transform(X_test)
        Y_test_scaled = scaler_Y.transform(Y_test)

        scalers = {
            'scaler_X': scaler_X,
            'scaler_Y': scaler_Y
        }

        # Save the scalers dictionary
        joblib.dump(scalers, RNA_SCALER_PATH)

        X_train, X_test, Y_train, Y_teste = train_test_split(X, Y, test_size=0.2, random_state=42)
        with open(RNA_TRAINTEST_PATH, mode='wb') as f:
            pickle.dump([X_train_scaled, X_test_scaled, Y_train_scaled, Y_test_scaled], f)

        rf_regressor = RandomForestRegressor(max_depth=9, max_features=None, max_leaf_nodes=9,
                      n_estimators=25, random_state=42)

        rf_regressor.fit(X_train_scaled, Y_train_scaled)
        joblib.dump(rf_regressor, RNA_MODEL_PATH)
        score = rf_regressor.score(X_train_scaled, Y_train_scaled)
        return round(score, 2)

    @staticmethod
    def make_predict(coordinates : dict):
        """
        Make predictions using a trained model.

        Args:
            ha (float): Target's hour angle.
            dec (float): Target's declination.
            temp (float): Temperature in degrees Celsius.
            latitude (float): Latitude of the location.

        Returns:
            tuple: Predicted hour angle and declination.

        """
        if not Utils.check_exists(RNA_MODEL_PATH):
            return None, None
        
        for key, value in coordinates.items():
            if key == "target_ha":
                if not Utils.is_numeric(value):
                    coordinates[key] = Utils.hms_to_hours(value)
            elif key == "prev_ha":
                if not Utils.is_numeric(value):
                    coordinates[key] = Utils.hms_to_hours(value)
            else:
                if not Utils.is_numeric(value):
                    coordinates[key] = Utils.dms_to_degrees(value)
        
        # rf = joblib.load(RNA_MODEL_PATH)
        model = joblib.load(RNA_MODEL_PATH)
        scalers = joblib.load(RNA_SCALER_PATH)
        scaler_X = scalers['scaler_X']
        scaler_Y = scalers['scaler_Y']


        az, elevation = Utils.get_elevation_azimuth(coordinates["target_ha"], coordinates["target_dec"], coordinates["latitude"])

        dist_ha = coordinates["target_ha"] - coordinates["prev_ha"]
        dist_dec = coordinates["target_dec"] - coordinates["prev_dec"]
        pier_side = coordinates["target_ha"] > 0
        azimuth_sin = np.sin(np.radians(az))
        azimuth_cos = np.cos(np.radians(az))

        elevation_sin = np.sin(np.radians(elevation))
        elevation_cos = np.cos(np.radians(elevation))

        ah_star_sin = np.sin(np.radians(coordinates["target_ha"] * 15))
        ah_star_cos = np.cos(np.radians(coordinates["target_ha"] * 15))

        dec_star_sin = np.sin(np.radians(coordinates["target_dec"]))
        dec_star_cos = np.cos(np.radians(coordinates["target_dec"]))

        prev_ha_sin = np.sin(np.radians(coordinates["prev_ha"] * 15))
        prev_ha_cos = np.cos(np.radians(coordinates["prev_ha"] * 15))

        prev_dec_sin = np.sin(np.radians(coordinates["prev_dec"]))
        prev_dec_cos = np.cos(np.radians(coordinates["prev_dec"]))
      

        X_futuro = np.array([[az, elevation, coordinates["target_ha"] * 15, 
                                coordinates["target_dec"], 
                                dist_ha * 15, dist_dec, pier_side,
                                azimuth_sin, azimuth_cos,
                                elevation_sin, elevation_cos,
                                ah_star_sin, ah_star_cos,
                                dec_star_sin, dec_star_cos,
                                prev_ha_sin, prev_ha_cos,
                                prev_dec_sin, prev_dec_cos]])
        X_futuro_scaled = scaler_X.transform(X_futuro)

        Y_rna_prever_futuro_scaled = model.predict(X_futuro_scaled)
        Y_rna_prever_futuro = scaler_Y.inverse_transform(Y_rna_prever_futuro_scaled)

        fator_correct_ha = Y_rna_prever_futuro[0][0]
        fator_correct_dec = Y_rna_prever_futuro[0][1]

        new_ha = coordinates["target_ha"] - fator_correct_ha/15
        new_dec = coordinates["target_dec"] - fator_correct_dec

        return (new_ha, new_dec)

    @staticmethod
    def tunning_hp():
        """
        Perform hyperparameter tuning for a RandomForestRegressor model.

        Returns:
            RandomForestRegressor: The best model obtained from hyperparameter tuning.

        """        
        param_grid = {
            'n_estimators': [25, 50, 100, 150],
            'max_features': ['sqrt', 'log2', None],
            'max_depth': [3, 6, 9],
            'max_leaf_nodes': [3, 6, 9],
        }

        scalers = joblib.load(RNA_SCALER_PATH)
        scaler_X = MinMaxScaler()
        scaler_Y = MinMaxScaler()

        X_train, X_test, Y_train, Y_test = joblib.load(RNA_TRAINTEST_PATH)
        

        X_train_scaled = scaler_X.fit_transform(X_train)
        Y_train_scaled = scaler_Y.fit_transform(Y_train)

        # Create the MLPRegressor
        rf = RandomForestRegressor(random_state=42)

        # Set up GridSearchCV
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)

        # Fit GridSearchCV
        grid_search.fit(X_train_scaled, Y_train_scaled)

        # Get the best estimator
        best_rf = grid_search.best_estimator_

        # Make predictions using cross-validation to make the most out of the small dataset
        cv_scores = cross_val_score(best_rf, X_train_scaled, Y_train_scaled, cv=5, scoring='neg_mean_squared_error')

        # Print cross-validation scores
        print("Cross-Validation MSE Scores:", -cv_scores)
        print("Mean Cross-Validation MSE:", -np.mean(cv_scores))

        best_rf.fit(X_train_scaled, Y_train_scaled)

        return best_rf

