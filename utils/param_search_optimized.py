import numpy as np
from sklearn.cluster import KMeans
from itertools import combinations, product
from keras.callbacks import EarlyStopping
from utils.split_dataset import split_dataset
from utils.models import Model
import tensorflow.keras as keras
from colorama import init, Fore, Style
from datetime import datetime 

def sph2cart(coords):
    alpha = coords[0]*(np.pi/180)
    beta = coords[1]*(np.pi/180)
    r = coords[2]

    x = r * np.cos(alpha) * np.cos(beta)
    y = r * np.sin(alpha) * np.cos(beta)
    z = r * np.sin(beta)
    return np.array([x, y, z]).T

def closest_node(node, nodes, threshold=1):
    """
    Returns the threshold # of point in nodes such that it minimizes the L2 norm with node.
    Note: numpy.argpartition returns the smallest threshold arguments.
    """
    node = sph2cart(node)
    temp = []
    for i in nodes:
      new_nodes = sph2cart(i)
      temp.append(new_nodes)
    dist = np.sum((temp - node)**2, axis=1)
    a = np.argpartition(dist,threshold)

    if threshold == 1:
      return nodes[a[0]]
    else:
      return nodes[a[0:threshold]]

def sections_split(positions, n_sections, phase_shift=0):
  '''
  Subdivides locations by ranges of azimuths
  '''
  deg = 360/n_sections
  deg = float(deg)
  sections = []
  for i in range(n_sections):
    temp = []
    for j in positions:
      if j[0] >= i*deg + phase_shift and j[0] < (i+1)*deg + phase_shift:
        temp.append(j)
    sections.append(np.array(temp))  
  return sections 


def gridsearch_optimized(model = None, hrir_all = None, n_sections=4, n_clusters=None, iterations=2, spread=3, output_file = "log.txt", random_state = 1):

  """
  positions - list of speaker locations. MUST BE IN SPHERICAL!
  n_sections - number of paritions to be made in positions dataset
  n_clusters - amount of clusters in each n_sections
  iterations - how many points you want to look from the center of a cluster
  spread - how many points you want to search for from a centroid that minimizes the Euclidean Distance
  random_state - used for KMeans clustering algorithm, usually will return centroids that are really close when run
  """
  positions = hrir_all[0].Source["Position"]
  
  channel = "left" #############
  observer_of_interest = 0 ############
  callback = keras.callbacks.EarlyStopping(monitor='loss', patience=3) ########

  sections = sections_split(positions, n_sections)

  model.compile(optimizer="adam")
  weights = model.model.get_weights()
  '''
  centers - center of each cluster
  closest_points - closest point from positions relative to centers
  '''
  pairs_losses = [] #gives the best pairs for the first iteration

  print(Fore.RED + "Evaluating Model at Centroids" + Fore.RESET)
  now = datetime.now()

  with open(output_file, "at") as filehandle:
    filehandle.write("\n")
    filehandle.write(f"{now}\n")
    filehandle.write("Evaluating Model at Centroids \n")

  for section in sections:
    kmeans = KMeans(n_clusters=n_clusters, copy_x=True, n_jobs=-1, random_state=random_state)
    kmeans.fit(section)
    center = kmeans.cluster_centers_

    val = []
    for i in center:
      val.append(closest_node(i,positions,threshold=1))

    val = [tuple(elem[0:2]) for elem in val] #removes 1.47

    comb = combinations(val,iterations) #4 C 2 = 6
    comb = list(comb) 
    comb = [list(elem) for elem in comb] #list of list of tuples

    print(comb)

    best_pair = None
    best_loss = None

    for count, pair in enumerate(comb):
      
      X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = pair, channel = "left", random_state = random_state)
      model.model.set_weights(weights)
      model.fit(X_train,y_train,X_test,y_test, verbose=False, num_epochs = 50, save_weights=False, callbacks=callback)
      y_predict = model.predict(X_holdout)
      loss = (np.sum(y_predict - y_holdout)**2)/len(y_predict)
      #print(pair[0], pair[1], loss, holdout_num)
      
      if best_loss is None:
        best_loss = loss 
        best_pair = pair 

      elif loss < best_loss:
        best_loss = loss 
        best_pair = pair

      message = f"Location:{pair}, Loss:{loss}"
      print(message)

      with open(output_file, "at") as filehandle:
        filehandle.write(f"{message}\n")

      #print(Fore.RESET)
      if count == len(comb)-1:
        pairs_losses.append(best_pair)
        #print(Fore.RED + f"{pairs_losses}")

  #print(pairs_losses)
  #print(Fore.RESET)
  print("_______________________________________________________________________________________________")

  overall_best_loc = []

  for count, section in enumerate(sections):
    """
    Note: pairs_losses will be sorted by ascending azimuth
    """
    print(Fore.RED + "New Section" + Fore.RESET)
    
    with open(output_file, "at") as filehandle:
        filehandle.write("New Section \n")

    final_best_pair = None
    final_best_loss = None 
    best_points = pairs_losses[count]
    temp_store = []
    for point in best_points:
      point = list(point)
      point.append(1.47)
      point = tuple(point)
      a = closest_node(point,section,threshold=spread+1) #returns back point and the spread nearest points in a list
      a = a.tolist()
      a = [tuple(elem[0:2]) for elem in a]
      temp_store.append(a)
      print(temp_store)
    d = list(product(*temp_store))
    e = [list(i) for i in d]

    #print(e) ####################
    #print(e[0])
    for count_, pair_ in enumerate(e):
      print(pair_)
      X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = pair_, channel = "left", random_state = random_state)
      model.model.set_weights(weights)
      model.fit(X_train,y_train,X_test,y_test, verbose=False, num_epochs = 50, save_weights=False, callbacks=callback)
      y_predict = model.predict(X_holdout)
      loss_ = (np.sum(y_predict - y_holdout)**2)/len(y_predict) #why is this elementwise??? it should overall

      if final_best_loss is None:
        final_best_loss = loss_ 
        final_best_pair = pair_

      elif loss_ < final_best_loss:
        final_best_loss = loss_
        final_best_pair = pair_ 
  
      message = f"Iteration:{count_}, Location:{pair_}, Loss:{loss_}"
      print(message)

      with open(output_file, "at") as filehandle:
        filehandle.write(f"{message}\n")
      
      if count_ == len(e)-1:
        overall_best_loc.append(final_best_pair)
        #print(f"{final_pairs_losses}")

  print(Fore.BLUE + "BEST POSITIONS ARE" + Fore.RESET + f" {overall_best_loc}")
  with open(output_file, "at") as filehandle:
    filehandle.write("BEST POSITIONS ARE \n")
    filehandle.write(f"{overall_best_loc} \n" )

  return overall_best_loc
