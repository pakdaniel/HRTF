from keras.callbacks import EarlyStopping
from .split_dataset import split_dataset
from itertools import combinations
from numpy import sum

def get_all_pairs(positions):
    return combinations(positions[:, :2], 2)


def grid_search(model = None, hrir_all = None, verbose=0, num_epochs = 100):
    pairs = get_all_pairs(hrir_all[0].Source["Position"])
    callback = EarlyStopping(monitor='loss', patience=3)
    best_pair = None
    best_loss = None
    pairs_losses = []
    model.compile(optimizer="adam")
    weights = model.model.get_weights()
    for pair in pairs:
        X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = pair, channel = "left")
        model.model.set_weights(weights)
        model.fit(X_train,y_train,X_test,y_test, verbose=verbose, num_epochs = num_epochs, save_weights=False, callbacks=callback)
        y_predict = model.predict(X_holdout)
        loss = (sum(y_predict - y_holdout)**2)/len(y_predict)
        # loss = model.log.history['loss'][-1]
        print("{}, {}: {:.4f}; Holdout: {}; current best is {} with {:.4f}".format(pair[0], pair[1], loss, holdout_num, best_pair, best_loss))
        if not best_loss:
            best_loss = loss
            best_pair = pair
        elif loss < best_loss:
            best_loss = loss
            best_pair = pair
        pairs_losses.append((pair, loss))
    
    print(f"Best pair is {best_pair} with {best_loss} loss")
    