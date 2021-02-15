import numpy as np
from ..acousticslib.domain_conversions import *


def split_dataset(dataset, observer_of_interest = 0, positions_of_interest = [(0,0)], channel = "left", input_type="HRIR", cut_after_samples = 127):
  VALID_INPUT_TYPES = ["HRIR", "HRTF", "HRTF Mirror"]
  if input_type not in VALID_INPUT_TYPES:
    raise ValueError(f"Input type must be one of: {', '.join(VALID_INPUT_TYPES)}")

  if channel == "left":
    channel = 0
  elif channel == "right":
    channel = 1
  else:
    raise NotImplementedError

  if input_type == "HRIR" or None:
    """
    Creates a training and testing set using just the HRIR information
    """

    hrir_train = dataset.copy()
    hrir_holdout = hrir_train.pop(observer_of_interest)

    X_test, y_test = hrir_holdout.split_HRIR_by_locations(positions_of_interest)
    X_test, y_test = X_test[:,channel,:].flatten().reshape((1, X_test.shape[0]*X_test.shape[2])), np.atleast_2d(y_test[:,channel,:].reshape((y_test.shape[0], y_test.shape[2])).flatten())
    X_train = []
    y_train = []

    for hrir in hrir_train:
      c,d = hrir.split_HRIR_by_locations(positions_of_interest)

      X_train.append(c[:, channel, :].flatten())
      y_train.append(d[:, channel, :].reshape((d.shape[0], d.shape[2])).flatten()) 
    

  elif "HRTF" in input_type:
    """
    The "HRIR Mirror" mode is to contain only the zero frequency information and the positive frequency information.
    As all of the HRIRs are length 256, the converted HRTF will also be length 256.
    Since 256 is an even number, the only parts that will be mirrored are the first 127 points (negative frequencies).
    The points of interest are when f=0 Hz, where it will be a real number, and the last point, which will have no corresponding
    mirror in the negative frequencies. Therefore 256 = 127 + 1 + 127 + 1. Once the HRTF is found for the right side, 
    the left side will be mirrored according such that the abs(HRTF) is an even function and angle(HRTF) is an odd function.
    Some lines in this function, where index splicing occurs, should be changed for an odd length HRIR/HRTF, but for now it will 
    remain fixed.

    The output will contain the magnitude information and the phase information. Phase is from [0, 2pi].
    The arrays will be structured in the format of [All Magnitudes| All Phase]
    """
    
    hrir_train = dataset.copy()
    hrir_holdout = hrir_train.pop(observer_of_interest)
    dt = 1/hrir_holdout.SamplingRate

    X_test, y_test = hrir_holdout.split_HRIR_by_locations(positions_of_interest)
    
    X_test, freq = ts2ls(X_test[:,channel,:], dt)
    if input_type == "HRTF Mirror":
      X_test = X_test[:,127:]
    X_test_mag = np.abs(X_test)
    X_test_phase = np.angle(X_test, deg=False) + np.pi
    X_test_mag = X_test_mag.flatten().reshape(1,X_test_mag.shape[0]*X_test_mag.shape[1])
    X_test_phase = X_test_phase.flatten().reshape(1,X_test_phase.shape[0]*X_test_phase.shape[1])
    max_x_test = np.max(np.abs(X_test))
    min_x_test = np.min(np.abs(X_test))

    y_test, freq = ts2ls(y_test[:,channel,:], dt)
    if input_type == "HRTF Mirror":
      y_test = y_test[:,127:]
    y_test_mag = np.abs(y_test)
    y_test_phase = np.angle(y_test, deg=False) + np.pi
    y_test_mag = y_test_mag.flatten().reshape(1,y_test_mag.shape[0]*y_test_mag.shape[1])
    y_test_phase = y_test_phase.flatten().reshape(1,y_test_phase.shape[0]*y_test_phase.shape[1])
    max_y_test = np.max(np.abs(y_test))
    min_y_test = np.min(np.abs(y_test))

    X_test, y_test = np.concatenate((X_test_mag,X_test_phase), axis = 1), np.concatenate((y_test_mag,y_test_phase), axis = 1) 
    X_train = []
    y_train = []
    max_x_train = 0
    max_y_train = 0
    min_x_train = 1
    min_y_train = 1
    max_c = []
    max_d = []

    for hrir in hrir_train:

      c,d = hrir.split_HRIR_by_locations(positions_of_interest)
      c, freq = ts2ls(c[:, channel, :], dt)
      if input_type == "HRTF Mirror":
        c = c[:,127:]

      c_mag = np.abs(c)
      c_phase = np.angle(c, deg=False) + np.pi
      c_mag = c_mag.flatten().reshape(1,c_mag.shape[0]*c_mag.shape[1])
      c_phase = c_phase.flatten().reshape(1,c_phase.shape[0]*c_phase.shape[1])
      c_new = np.concatenate((c_mag, c_phase), axis = 1)
      
      
      d, freq = ts2ls(d[:, channel, :], dt)
      if input_type == "HRTF Mirror":
        d = d[:,127:]

      d_mag = np.abs(d)
      d_phase = np.angle(d, deg=False) + np.pi
      d_mag = d_mag.flatten().reshape(1,d_mag.shape[0]*d_mag.shape[1])
      d_phase = d_phase.flatten().reshape(1,d_phase.shape[0]*d_phase.shape[1])
      d_new = np.concatenate((d_mag, d_phase), axis = 1)

      X_train.append(c_new.flatten()) 
      y_train.append(d_new.flatten()) 
      max_c.append(c_mag)
      max_d.append(d_mag)    

  X_train = np.array(X_train)
  y_train = np.array(y_train)


  return X_train, y_train, X_test, y_test

  #def scale_dataset(X_train, y_train, X_test, y_test):
    
