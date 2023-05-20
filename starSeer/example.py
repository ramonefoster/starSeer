from randomForest import RandomForest
from utils import Utils

u = Utils()
rf = RandomForest('-22:32:54.07')

# rf.train()
ha, dec = rf.make_predict(ha="02:45:43", dec=54.23, temp=14)
print(ha, dec)
print(u.hours_to_string(ha, 2), u.degrees_to_string(dec))