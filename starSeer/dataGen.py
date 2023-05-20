import pandas as pd
import csv
from pathlib import Path

class DataManager():
    def __init__(self, path):
        self.path = path       

    def read_data(self):
        """
        Le o arquivo CSV e separa as variaveis de interesse.
        :return: Dataframes X, Y
        """
        dataframe = pd.read_csv(self.path)

        X = dataframe[["azimuth", "elevation", "ah_star", "dec_star", "temperature"]]
        Y = dataframe[["err_ah", "err_dec"]]

        return X, Y

    def create_file(self):
        """Cria novo arquivo CSV com Header"""
        headerList = ['ah_star', 'dec_star', 'ah_scope', 'dec_scope', 'err_ah', 'err_dec', 'elevation', 'azimuth', 'temperature']

        with open(self.path, 'w') as file:
            dw = csv.DictWriter(file, delimiter=',', 
                                fieldnames=headerList)
            dw.writeheader()
            file.close()

    def save_dataframe(self, ah_star, dec_star, ah_scope, dec_scope, azimuth, elevation, temperature):
        """
        Salva dados no arquivo CSV.
        :param ah_star: Angulo Horario real da estrela
        :param dec_star: Declinacao real da estrela
        :param ah_scope: Angulo Horario do telescopio
        :param dec_scope: Declinacao do telescopio
        :param azimuth: Azimuth do telescopio
        :param elevation: Elevacao do telescopio
        :param temperatura: Temperatura interna da cupula
        """
        path_file = Path(self.path)
        if not path_file.is_file():
            self.create_file()

        err_ah = ah_star - ah_scope
        err_dec = dec_star - dec_scope

        d = {'ah_star': [ah_star], 'dec_star': [dec_star],
            'ah_scope': [ah_scope], 'dec_scope': [dec_scope],
            'err_ah': [err_ah], 'err_dec': [err_dec], 
            'elevation':[elevation], 'azimuth': [azimuth], 'temperature': [temperature] }

        df = pd.DataFrame.from_dict(data=d)
        df.to_csv(self.path, mode='a', index=False, header=False)


