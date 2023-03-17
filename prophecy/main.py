from get_data import WeatherEnergy
from feature_processing import FeaturePreprocessing
import tensorflow as tf
#df = WeatherEnergy(
#    limit=-1, offset=0, refine='Hauts-de-France', city=['Heudicourt', 'Bucy-les-Pierrepont', 'Riencourt'], years=10, target='eolien'
#    ).merged()
#df_processed = FeaturePreprocessing(df).get_period_day()

new_data = FeaturePreprocessing(new_data).get_period_day()

new_model = tf.keras.models.load_model('saved_model/my_model')

print(new_model.summary())
new_model.predict(new_data)
