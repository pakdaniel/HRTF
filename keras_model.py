# -*- coding: utf-8 -*-

from numpy import ceil
size = 25

import os
import sys
from utils.CustomSOFA import SOFA
HUTUBS_PATH = "/mnt/c/users/evanb/The Cooper Union for the Advancement of Science and Art/ME-Project-6-HRTF-Estimation - General/HUTUB"
HRIR_DIR = os.path.join(HUTUBS_PATH, "HRIRs")
ANTHROPOMETRIC_DIR = os.path.join(HUTUBS_PATH, "Antrhopometric measures")
HEADMESH_DIR = os.path.join(HUTUBS_PATH, "3D head meshes")

FIGS_DIR = os.path.join(HUTUBS_PATH, "figs")
WEIGHTS_DIR = os.path.join(HUTUBS_PATH, "model_weights")
for extra_dir in [FIGS_DIR, WEIGHTS_DIR]:
  if not os.path.exists(extra_dir):
    os.makedirs(extra_dir)

import pysofaconventions
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd 
from utils.acousticslib.plots import *

from utils.acousticslib.domain_conversions import *

PLOT_TEXT_COLOR = "black"; LEGEND_COLOR = "white"

def read_sofa(sofa_path):
    return SOFA(pysofaconventions.SOFAFile(sofa_path,'r'))
  

# Creating a list of all the measured HRIRs (Ordered numerically by file name)

#1 and 96 are repeated measurements of dummy head
#22 and 88 are repeated measurements of same human
hrir_paths = [os.path.join(HRIR_DIR, hrir_path) for hrir_path in os.listdir(HRIR_DIR) if "_measured.sofa" in hrir_path]
hrir_paths = sorted(hrir_paths, key=lambda x: int((x.split("/")[-1].split("_")[0][2:])))

try:
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp1_HRIRs_measured.sofa'))
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp22_HRIRs_measured.sofa'))
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp96_HRIRs_measured.sofa'))
except:
  raise ValueError("Was not able to remove unnecessary SOFA files from list")

hrir_all = [read_sofa(i) for i in hrir_paths]

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

def preprocessing_ss(data, scaling_type="StandardScaler"):
  """
  Scales the data COLUMNWISE! 
  """
  
  if scaling_type == "StandardScaler" or None:
    """
    X' = (X - avg(X))/std(X)
    """
    obj = StandardScaler().fit(data)
    data = obj.transform(data)
    
  elif scaling_type == "MinMaxScaler":
    """
    X' = (X-min(X))/(max(X)-min(X))
    """
    obj = MinMaxScaler().fit(data)
    data = obj.transform(data)

  return data, obj

from sklearn.decomposition import PCA

def PCA_component_number(data,n_components=99,threshold=0.9):
  """
  Determines the minimum number of components needed using a percent threshold on how much variance information should be contained
  """
  pca_object = PCA(n_components=n_components)
  pca_object.fit(data)
  total = 0
  for ee,evr in enumerate(pca_object.explained_variance_ratio_):
      total = total+evr
      if total<threshold:
          n_com = ee+1
          #print(total)
  n_com = n_com+1

  # print(np.sum(pca_test.explained_variance_ratio_))
  # print(pca_test.singular_values_)

  return n_com, pca_object

import tensorflow.keras as keras
import keras.backend as K 

def custom_loss_function(y_true,y_pred):
  """
  This will be LSD for HRTF (come back to this)
  """
  #print(20*K.log(y_true)-20*K.log(y_pred))
  loss = K.sqrt(K.mean((K.square(20*K.log(y_true+1)-20*K.log(y_pred+1)))))
  return loss

def min_max_scaling(X_train, y_train, X_test, y_test):
  """
  Scales only the amplitude information by X_i = (X_i - min(all X_i)) / max(all X_i)
  """
  X_train_1 = X_train[:,0:int(X_train.shape[1]/2)]
  y_train_1 = y_train[:,0:int(y_train.shape[1]/2)]
  X_test_1 = X_test[:,0:int(X_test.shape[1]/2)]
  y_test_1 = y_test[:,0:int(y_test.shape[1]/2)]

  max = [np.max(X_train_1), np.max(y_train_1), np.max(X_test_1), np.max(y_test_1)]
  max = np.max(max)

  min = [np.min(X_train_1), np.min(y_train_1), np.min(X_test_1), np.min(y_test_1)]
  min = np.min(min)

  X_train_1 = (X_train_1 - min)/max
  y_train_1 = (y_train_1 - min)/max
  X_test_1 = (X_test_1 - min)/max
  y_test_1 = (y_test_1 - min)/max

  X_train = np.concatenate((X_train_1, X_train[:,int(X_train.shape[1]/2):]), axis = 1)
  y_train = np.concatenate((y_train_1, y_train[:,int(y_train.shape[1]/2):]), axis = 1)
  X_test = np.concatenate((X_test_1, X_test[:,int(X_test.shape[1]/2):]), axis = 1)
  y_test = np.concatenate((y_test_1, y_test[:,int(y_test.shape[1]/2):]), axis = 1)


  return X_train, y_train, X_test, y_test

"""## Positions"""

test_file = "pp1_HRIRs_measured.sofa"
test_file_path = os.path.join(HRIR_DIR, test_file)
hrir = read_sofa(test_file_path)
pos = hrir.Source["Position"]

from utils.models import Model

class HRIRModel(Model):
  def __init__(self, input_shape, output_shape, model_name = "HRIRModel", load_from=None):
    Model.__init__(self, input_shape, output_shape, model_name, load_from)

  def initialize_model(self, input_shape, output_shape, model_name):
    input_layer = keras.layers.Input(shape = input_shape)    
    x = keras.layers.Dense(input_shape, activation="relu", kernel_initializer="he_uniform")(input_layer)    
    #x = keras.layers.Dense(input_shape*3, activation="relu", kernel_initializer="he_uniform")(x)
    #x = keras.layers.Dense(output_shape)(input_layer)
    x = keras.layers.Dense(output_shape)(x)    
    self.model = keras.models.Model(input_layer, x, name=model_name)

class HRIRPCAModel(Model):
  def __init__(self, input_shape, output_shape, model_name = "HRIRModel", load_from=None):
    Model.__init__(self, input_shape, output_shape, model_name, load_from)

  def initialize_model(self, input_shape, output_shape, model_name):
    input_layer = keras.layers.Input(shape = input_shape)    
    x = keras.layers.Dense(input_shape, activation="relu", kernel_initializer="he_uniform")(input_layer)    
    x = keras.layers.Dense(input_shape*10, activation="relu", kernel_initializer="he_uniform")(x)
    #x = keras.layers.Dense(output_shape)(input_layer)
    x = keras.layers.Dense(output_shape)(x)    
    self.model = keras.models.Model(input_layer, x, name=model_name)

"""## HRIR"""

from utils.param_search import grid_search
from utils.split_dataset import split_dataset

# import random
channel = "left"
save_weights = False
verbose = 1
num_epochs = 60
positions_of_interest = [(48,40),(132,40)] # array of (azimuth, elevation)

observer_of_interest = 0

X_train, y_train, X_test, y_test = split_dataset(hrir_all, observer_of_interest = observer_of_interest, positions_of_interest = positions_of_interest, channel = channel)

callback = keras.callbacks.EarlyStopping(monitor='loss', patience=3)


model = HRIRModel(X_train.shape[1],y_train.shape[1],model_name="subject_{}_{}_channel_at_{}".format(observer_of_interest, channel, "_and_".join(["{}_{}".format(azimuth, elevation) for azimuth, elevation in positions_of_interest])))
model.compile(optimizer="adam")
model.fit(X_train,y_train,X_test,y_test, verbose=verbose, num_epochs = num_epochs, save_weights=save_weights, weights_dir=WEIGHTS_DIR,callbacks=callback)

from utils.param_search import grid_search
grid_search(model=model, hrir_all=hrir_all)