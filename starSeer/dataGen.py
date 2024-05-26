import pandas as pd
import csv
import numpy as np
from starSeer.utils import Utils
from starSeer.constants import *

class DataManager():
    @staticmethod
    def read_data():
        """
        Read the CSV file and extract the variables of interest.

        Returns:
            X (pandas.DataFrame): Dataframe containing the selected input variables.
            Y (pandas.DataFrame): Dataframe containing the selected output variables.
            X : "azimuth", "elevation", "ah_star", "dec_star", "prev_ha", "prev_dec"
            Y: "err_ah", "err_dec"
        """
        if not Utils.check_exists(RNA_CSV_PATH):
            return None, None
        
        dataframe = pd.read_csv(RNA_CSV_PATH)

        # Apply noise to original dataset
        noisy_df = Utils.add_noise(dataframe)

        # Concatenate original and noisy data
        augmented_df = pd.concat([dataframe, noisy_df])
    
        augmented_df.loc[:, "ah_star"] = augmented_df["ah_star"] * 15
        augmented_df.loc[:, "prev_ha"] = augmented_df["prev_ha"] * 15
        # Feature engineering: create new columns
        augmented_df.loc[:, "dist_ha"] = augmented_df["ah_star"] - augmented_df["prev_ha"]
        augmented_df.loc[:, "dist_dec"] = augmented_df["dec_star"] - augmented_df["prev_dec"]
        augmented_df.loc[:, "pier_side"] = augmented_df["ah_star"] > 0

        # Trigonometric transformations
        augmented_df['azimuth_sin'] = np.sin(np.radians(augmented_df['azimuth']))
        augmented_df['azimuth_cos'] = np.cos(np.radians(augmented_df['azimuth']))

        augmented_df['elevation_sin'] = np.sin(np.radians(augmented_df['elevation']))
        augmented_df['elevation_cos'] = np.cos(np.radians(augmented_df['elevation']))

        augmented_df['ah_star_sin'] = np.sin(np.radians(augmented_df['ah_star']))
        augmented_df['ah_star_cos'] = np.cos(np.radians(augmented_df['ah_star']))

        augmented_df['dec_star_sin'] = np.sin(np.radians(augmented_df['dec_star']))
        augmented_df['dec_star_cos'] = np.cos(np.radians(augmented_df['dec_star']))

        augmented_df['prev_ha_sin'] = np.sin(np.radians(augmented_df['prev_ha']))
        augmented_df['prev_ha_cos'] = np.cos(np.radians(augmented_df['prev_ha']))

        augmented_df['prev_dec_sin'] = np.sin(np.radians(augmented_df['prev_dec']))
        augmented_df['prev_dec_cos'] = np.cos(np.radians(augmented_df['prev_dec']))

        # Select augmented features (X) and target (Y)
        augmented_X = augmented_df[["azimuth", "elevation", "ah_star", "dec_star", 
                                    "dist_ha", "dist_dec", "pier_side",
                                    "azimuth_sin", "azimuth_cos",
                                    "elevation_sin", "elevation_cos",
                                    "ah_star_sin", "ah_star_cos",
                                    "dec_star_sin", "dec_star_cos",
                                    "prev_ha_sin", "prev_ha_cos",
                                    "prev_dec_sin", "prev_dec_cos"]]
        
        augmented_df["err_ah"] = augmented_df["err_ah"] * 15
        augmented_Y = augmented_df[["err_ah", "err_dec"]]
        

        return augmented_X, augmented_Y
    
    @staticmethod
    def create_file():
        """Cria novo arquivo CSV com Header"""
        headerList = ['ah_star', 'dec_star', 'ah_scope', 'dec_scope', 'err_ah', 'err_dec', 'elevation', 'azimuth', 'temperature', 'prev_ha', 'prev_dec']

        with open(RNA_CSV_PATH, 'w') as file:
            dw = csv.DictWriter(file, delimiter=',', 
                                fieldnames=headerList)
            dw.writeheader()
            file.close()

    @staticmethod
    def save_dataframe(ah_star, dec_star, ah_scope, dec_scope, azimuth, elevation, temperature, prev_ha, prev_dec):
        """
        Save data to a CSV file.

        Parameters:
            ah_star (float): Real star hour angle.
            dec_star (float): Real star declination.
            ah_scope (float): Telescope hour angle.
            dec_scope (float): Telescope declination.
            azimuth (float): Telescope azimuth.
            elevation (float): Telescope elevation.
            temperature (float): Internal dome temperature.
            prev_ha (float): Telescope HA position before slewing to target
            prev_dec (float): Telescope DEC position before slewing to target

        """
        if not Utils.check_exists(RNA_CSV_PATH):
            DataManager.create_file()
        
        err_ah = ah_star - ah_scope
        err_dec = dec_star - dec_scope

        d = {'ah_star': [ah_star], 'dec_star': [dec_star],
            'ah_scope': [ah_scope], 'dec_scope': [dec_scope],
            'err_ah': [err_ah], 'err_dec': [err_dec], 
            'elevation':[elevation], 'azimuth': [azimuth], 
            'temperature': [temperature], 'prev_ha': [prev_ha], 'prev_dec': [prev_dec] }

        df = pd.DataFrame.from_dict(data=d)
        df.to_csv((RNA_CSV_PATH), mode='a', index=False, header=False)


