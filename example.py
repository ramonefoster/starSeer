from randomForest import RandomForest

rf = RandomForest('-22:32:54.07')
# rf.train()
ha, dec = rf.make_predict(ha="-2:45:43", dec=-54.23, temp=14)
print(ha, dec)