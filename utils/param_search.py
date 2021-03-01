from keras.callbacks import EarlyStopping
from .split_dataset import split_dataset
from itertools import combinations
from numpy import sum

def get_all_combs(positions, num):
    return combinations(positions[:, :2], num)


def grid_search(model = None, hrir_all = None, verbose=0, num_epochs = 100, num_positions = 2, notebook = False):
    coord_sets = get_all_combs(hrir_all[0].Source["Position"], num_positions)
    callback = EarlyStopping(monitor='loss', patience=3)
    best_coord_set = None
    best_loss = None
    coord_sets_losses = []
    model.compile(optimizer="adam")
    weights = model.model.get_weights()
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm
    
    for i, coord_set in tqdm(enumerate(coord_sets), total=len(coord_sets)):
        X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = coord_set, channel = "left")
        model.model.set_weights(weights)
        model.fit(X_train,y_train,X_test,y_test, verbose=verbose, num_epochs = num_epochs, save_weights=False, callbacks=callback)
        y_predict = model.predict(X_holdout)
        loss = (sum(y_predict - y_holdout)**2)/len(y_predict)
        if not best_loss:
            best_loss = loss
            best_coord_set = coord_set
        elif loss < best_loss:
            best_loss = loss
            best_coord_set = coord_set
        # loss = model.log.history['loss'][-1]
        print("{}/{}: {}: {:.4f}; Holdout: {}; current best is {} with {:.4f}".format(
            i,
            len(coord_sets),
            "[" + ", ".join(["({}, {})".format(item[0], item[1]) for item in coord_set]) + "]",
            loss,
            holdout_num,
            "[" + ", ".join(["({}, {})".format(item[0], item[1]) for item in best_coord_set]) + "]",
            best_loss
            )
        )

        coord_sets_losses.append((coord_set, loss))
    
    print(f"Best coordinate set is {best_coord_set} with {best_loss} loss")
    return coord_sets_losses