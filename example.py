from starSeer.starSeer import StarSeer
from starSeer.utils import Utils

ss = StarSeer()

# Trains the model
score = ss.train()

# Coefficient of determination of the prediction
# The best possible score is 1.0
print("The Score of the trained Model is: ", score)

# ACCEPTS FLOAT VALUES OR STRING VALUES
coordinates = {
    "target_ha": 2.653,  # Stars Hour Angle
    "target_dec": '-54:20:39', # Stars Declination
    "temperature": 14, # Temperature
    "latitude": '-22:32:54.07', # Latitude of the Site
    "prev_ha": "00:00:00", # Hour Angle before Slew
    "prev_dec": '-22:32:54.07' # Declination before Slew
}

ha, dec = ss.make_predict(coordinates)
print(ha, dec) # Predicted, i.e, corrected coordinates (float)
print(Utils.hours_to_string(ha, 2), Utils.degrees_to_string(dec)) # Predicted, i.e, corrected coordinates (hh:mm:ss and dd:mm:ss)