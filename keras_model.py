# -*- coding: utf-8 -*-

import os
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
import numpy as np
import pandas as pd
from utils.acousticslib.domain_conversions import *

def read_sofa(sofa_path):
    return SOFA(pysofaconventions.SOFAFile(sofa_path,'r'))

hrir_paths = [os.path.join(HRIR_DIR, hrir_path) for hrir_path in os.listdir(HRIR_DIR) if "_measured.sofa" in hrir_path]
hrir_paths = sorted(hrir_paths, key=lambda x: int((x.split("/")[-1].split("_")[0][2:])))

try:
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp1_HRIRs_measured.sofa'))
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp22_HRIRs_measured.sofa'))
  hrir_paths.remove(os.path.join(HRIR_DIR, 'pp96_HRIRs_measured.sofa'))
except:
  raise ValueError("Was not able to remove unnecessary SOFA files from list")

hrir_all = [read_sofa(i) for i in hrir_paths]



import tensorflow.keras as keras
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

model = HRIRModel(X_train.shape[1],y_train.shape[1],model_name="subject_{}_{}_channel_at_{}".format(observer_of_interest, channel, "_and_".join(["{}_{}".format(azimuth, elevation) for azimuth, elevation in positions_of_interest])))
from utils.param_search import grid_search
grid_search(model=model, hrir_all=hrir_all)