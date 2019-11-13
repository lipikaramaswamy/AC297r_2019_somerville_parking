# imports
import tensorflow as tf
import pandas as pd
import numpy as np
import glob
import sys
sys.path.append('../')
from generator import generator_two_inputs
from metrics import sensitivity, specificity


def load_model(model_path):
	'''
	Loads in a previously stored Keras model object in HDF5 format.

	Parameters
	----------
	model_path : str

	Returns
	-------
	model : Keras model object
	'''

	model = tf.keras.models.load_model(model_path, 
		custom_objects={'sensitivity':sensitivity, 'specificity':specificity})
	return model

def predict(model, data, y_column='temp_label',
	aerial_dir='../data/training/aerial_images/', gsv_dir='../data/training/street_view_images/',
	gsv_image_dim = (128,128, 3), aer_image_dim = (128,128, 4)):
	'''
	Generates model predictions for data.

	Parameters
	----------
	model : Keras model object
	data : pd.DataFrame
	y_column : str
	aerial_dir : str
	gsv_dir : str
	gsv_image_dim : tuple 
	aer_image_dim : tuple

	Returns
	-------
	preds : np.array
	'''

	preds = model.predict_generator(generator_two_inputs(data, aerial_dir = aerial_dir, gsv_dir = gsv_dir, 
		batch_size = data.shape[0], gsv_image_dim = gsv_image_dim, aer_image_dim = aer_image_dim,
		y_column = y_column),
	steps = 1)

	return preds

def create_parcel_df(aerial_dir='../data/training/aerial_images/', 
	gsv_dir='../data/training/sv_images/'):
	'''
	Creates dataframe to pass into predict function for all parcels in Somerville.

	Parameters
	----------
	aerial_dir : str
	gsv_dir : str

	Returns
	-------
	df : pd.DataFrame
	'''

	# get all file names
	aerial_files = glob.glob(aerial_dir + '*.png') 
	gsv_files = glob.glob(gsv_dir + '*.jpg') 

	# strip them of extension so we can match them
	aerial_files_raw = [x.split('/')[-1].replace('_aerial.png', '') for x in aerial_files]
	gsv_files_raw = [x.split('/')[-1].replace('.jpg', '') for x in gsv_files]

	# merge on street name
	# keep all records
	aerial_df = pd.DataFrame(aerial_files_raw, columns=['aerial_ADDR'])
	gsv_df = pd.DataFrame(gsv_files_raw, columns=['gsv_ADDR'])
	df = aerial_df.merge(gsv_df, how='outer', left_on='aerial_ADDR', right_on='gsv_ADDR')

	return df

if __name__ == '__main__':

	# # load model
	# model_path = '../models/basicmodel.h5'
	# model = load_model(model_path)

	# # load data
	# data = pd.read_csv('../labels/training_labels_updated.csv')
	# print(data.dtypes)
	# data['temp_label'] = data['final_label'].apply(lambda x: np.round(x)).astype('int').astype('str')

	# # sample data for illustrative purposes
	# addresses_gsv_filename = ['1_ESSEX_ST.jpg', '8_GILMAN_ST.jpg', '9_MELVILLE_RD.jpg','10_CENTRAL_ST.jpg',
 #                         '14_MANSFIELD_ST.jpg']
	# pred_sample = data[data.gsv_filename.isin(addresses_gsv_filename)]
	
	# # get model predictions
	# preds = predict(model, pred_sample)

	# # print results
	# print('Predictions\n', preds)
	# print(f"\nThere are {preds.sum()} drvieways.")

	df = create_parcel_df()


