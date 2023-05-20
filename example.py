from starSeer.randomForest import RandomForest
from starSeer.utils import Utils

u = Utils()
rf = RandomForest('-22:32:54.07', r"C:\Users\ramon\OneDrive\Área de Trabalho\StarSeer\starSeer\dataset.csv")

rf.train()
ha, dec = rf.make_predict(ha="02:45:43", dec=54.23, temp=14)
print(ha, dec)
print(u.hours_to_string(ha, 2), u.degrees_to_string(dec))