import numpy as np
from utils.acousticslib.domain_conversions import *
from sklearn.model_selection import train_test_split

# Just do the left, and we will just mirror them across the plane of symmetry afterward (so if there are 3 points we're testing for, this will become 6)


def split_dataset(dataset, observer_of_interest = 0, positions_of_interest = [(0,0)], channel = "left", input_type="HRIR", cut_after_samples = 127, random_state = 42):
  VALID_INPUT_TYPES = ["HRIR", "HRTF", "HRTF Mirror"]
  if input_type not in VALID_INPUT_TYPES:
    raise ValueError(f"Input type must be one of: {', '.join(VALID_INPUT_TYPES)}")

  if channel == "left":
    channel = 0
  elif channel == "right":
    channel = 1
  else:
    raise NotImplementedError


  hrir_train, hrir_test = train_test_split(list(zip(range(2, len(dataset)+1), dataset)), test_size = 0.2, shuffle=True, random_state = random_state)
  hrir_holdout = hrir_train.pop(observer_of_interest)
  holdout_num = hrir_holdout[0]
  X_holdout, y_holdout = hrir_holdout[1].split_HRIR_by_locations(positions_of_interest)

  if input_type == "HRIR":
    """
    Creates a training and testing set using just the HRIR information
    """
    
    X_holdout, y_holdout = X_holdout[:,channel,:].flatten().reshape((1, X_holdout.shape[0]*X_holdout.shape[2])), np.atleast_2d(y_holdout[:,channel,:].reshape((y_holdout.shape[0], y_holdout.shape[2])).flatten())
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    for hrir_set, X_set, y_set in zip([hrir_train, hrir_test], [X_train, X_test], [y_train, y_test]):
      for _, hrir in hrir_set:
        c,d = hrir.split_HRIR_by_locations(positions_of_interest)

        X_set.append(c[:, channel, :].flatten())
        y_set.append(d[:, channel, :].reshape((d.shape[0], d.shape[2])).flatten()) 
    

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

    dt = 1/hrir_holdout.SamplingRate
   
    X_holdout, freq = ts2ls(X_holdout[:,channel,:], dt)
    if input_type == "HRTF Mirror":
      X_holdout = X_holdout[:,127:]
    X_holdout_mag = np.abs(X_holdout)
    X_holdout_phase = np.angle(X_holdout, deg=False) + np.pi
    X_holdout_mag = X_holdout_mag.flatten().reshape(1,X_holdout_mag.shape[0]*X_holdout_mag.shape[1])
    X_holdout_phase = X_holdout_phase.flatten().reshape(1,X_holdout_phase.shape[0]*X_holdout_phase.shape[1])
    max_x_test = np.max(np.abs(X_holdout))
    min_x_test = np.min(np.abs(X_holdout))

    y_holdout, freq = ts2ls(y_holdout[:,channel,:], dt)
    if input_type == "HRTF Mirror":
      y_holdout = y_holdout[:,127:]
    y_holdout_mag = np.abs(y_holdout)
    y_holdout_phase = np.angle(y_holdout, deg=False) + np.pi
    y_holdout_mag = y_holdout_mag.flatten().reshape(1,y_holdout_mag.shape[0]*y_holdout_mag.shape[1])
    y_holdout_phase = y_holdout_phase.flatten().reshape(1,y_holdout_phase.shape[0]*y_holdout_phase.shape[1])
    max_y_holdout = np.max(np.abs(y_holdout))
    min_y_holdout = np.min(np.abs(y_holdout))

    X_holdout, y_holdout = np.concatenate((X_holdout_mag,X_holdout_phase), axis = 1), np.concatenate((y_holdout_mag,y_holdout_phase), axis = 1) 
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    max_c = []
    max_d = []

    for hrir_set, X_set, y_set in zip([hrir_train, hrir_test], [X_train, X_test], [y_train, y_test]):
      for _, hrir in hrir_set:


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

        X_set.append(c_new.flatten()) 
        y_set.append(d_new.flatten()) 
        max_c.append(c_mag)
        max_d.append(d_mag)    

  X_train = np.array(X_train)
  y_train = np.array(y_train)
  X_test = np.array(X_test)
  y_test = np.array(y_test)


  return X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num

  #def scale_dataset(X_train, y_train, X_holdout, y_holdout):
    
