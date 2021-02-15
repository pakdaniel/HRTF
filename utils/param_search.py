from keras.callbacks import EarlyStopping
from .split_dataset import split_dataset
from itertools import permutations

def add_position(position_pairs, positions, i):
    
    list1 = [positions[i]]
    if i == len(positions-1):
        return
    list2 = positions[i+1:]
    positions.extend([list(zip(each_permutation, list2)) for each_permutation in permutations(list1, len(list2))])

def get_all_pairs(positions):
    position_pairs = []
    for i in range(len(positions)):
        add_position(position_pairs, positions, i)
    return position_pairs

def grid_search(model, hrir_all):
    pairs = get_all_pairs(hrir_all[0].Source["Position"])
    callback = EarlyStopping(monitor='loss', patience=3)
    best_pair = None
    best_loss = None
    pairs_losses = []
    for pair in pairs:
        X_train, y_train, X_test, y_test = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = pair, channel = "left")
        model.compile(optimizer="adam")
        model.fit(X_train,y_train,X_test,y_test, verbose=1, num_epochs = 100, save_weights=False, callbacks=callback)
        print(f"{pair[0]}, {pair[1]}: {model.log.history['loss'][-1]}")
        if not best_loss:
            best_loss = model.log.history['loss'][-1]
            best_pair = pair
        elif model.log.history['loss'][-1] < best_loss:
            best_loss = model.log.history['loss'][-1]
            best_pair = pair
        pairs_losses.append((pair, model.log.history['loss'][-1]))
    
    print(f"Best pair is {best_pair} with {best_loss} loss")