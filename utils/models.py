import tensorflow.keras as keras
import os

class Model:
  def __init__(self, input_shape, output_shape, model_name = "Model", load_from=None):
    self.model_name = model_name
  
    if load_from:
      self.load_model(load_from)
    else:
      self.initialize_model(input_shape, output_shape, model_name)

  def initialize_model(self, input_shape, output_shape, model_name):
    raise NotImplementedError
      
  def compile(self, verbose=False, optimizer_name=None, optimizer=None, loss="mse", optimizer_args = None):
    if not (optimizer_name or optimizer):
      optimizer_name = "sgd"

    if optimizer_name:      
      if optimizer == "sgd":
        optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0, nesterov=False, name="SGD")
      elif optimizer == "adam":
        optimizer = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07)

    self.model.compile(
        loss=loss,
        optimizer=optimizer
    )

    if verbose:
      self.model.summary()
    
  def fit(self, X_train, y_train, X_val, y_val, num_epochs = 50, verbose=0, save_weights = False, weights_dir = None, callbacks = []):
    
    if save_weights:
      if not (weights_dir):
        raise ValueError("Output directory must be specified to save weights")
      callbacks.append(
        keras.callbacks.ModelCheckpoint(os.path.join(weights_dir, "{}-weights.h5".format(self.model_name)),
            monitor="val_loss",
            save_best_only=True,
            verbose=1)
        )

    self.log = self.model.fit(
        X_train, y_train,
        epochs = num_epochs,
        verbose = bool(verbose),
        validation_data = (X_val, y_val),
        callbacks = callbacks
    )
  
  def predict(self, *args, **kwargs):
    return self.model.predict(*args, **kwargs)

  def load_weights(self, *args, **kwargs):
    self.model.load_weights(*args, **kwargs)

  def save_weights(self, *args, **kwargs):
    self.model.save_weights(*args, **kwargs)

  def load_model(self, model_path):
    with open(model_path, "r") as json_file:
      model_json = json_file.read()
    self.model = keras.models.model_from_json(model_json)
    
  def save_model(self, model_path):
    model_json = self.model.to_json()
    with open(model_path, "w") as json_file:
      json_file.write(model_json)