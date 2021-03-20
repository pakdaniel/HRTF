from keras.callbacks import EarlyStopping
from .split_dataset import split_dataset
from itertools import combinations, islice
from numpy import sum

def get_all_combs(positions, num):
    return list(combinations(positions[:, :2], num))


def grid_search(model = None, hrir_all = None, coord_sets = None, verbose=0, num_epochs = 100, num_positions = 2, notebook = False, start_from = 0, output_file = "log.txt"):
    if coord_sets is None:
        coord_sets = get_all_combs(hrir_all[0].Source["Position"], num_positions)
    callback = EarlyStopping(monitor='loss', patience=3)
    best_coord_set = None
    best_loss = None
    model.compile(optimizer="adam")
    weights = model.model.get_weights()
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

        with open(output_file, "at") as filehandle:
            filehandle.write("Index,Coords,Loss,Test Loss,Holdout\n")
    
    for i, coord_set in tqdm(islice(enumerate(coord_sets), start_from, None), total=len(coord_sets)):
        X_train, y_train, X_holdout, y_holdout, X_test, y_test, holdout_num = split_dataset(hrir_all, observer_of_interest = 0, positions_of_interest = coord_set, channel = "left")
        model.model.set_weights(weights)
        model.fit(X_train,y_train,X_test,y_test, verbose=verbose, num_epochs = num_epochs, save_weights=False, callbacks=callback)
        loss = (sum(model.predict(X_holdout) - y_holdout)**2)/len(y_holdout)
        test_loss = (sum(model.predict(X_test) - y_holdout)**2)/len(y_holdout)
        if not best_loss:
            best_loss = loss
            best_coord_set = coord_set
        elif loss < best_loss:
            best_loss = loss
            best_coord_set = coord_set
        # loss = model.log.history['loss'][-1]
        write_data = "{},{},{:.4f},{:.4f},{}".format(
            i,
            "[" + ", ".join(["({}, {})".format(int(item[0]), int(item[1])) for item in coord_set]) + "]",
            loss,
            test_loss,
            holdout_num
        )

        message = "{}/{}: {}:{:.4f}, {:.4f}, Holdout:{}; Best:{} with {:.4f}".format(
            i,
            len(coord_sets),
            "[" + ", ".join(["({}, {})".format(int(item[0]), int(item[1])) for item in coord_set]) + "]",
            loss,
            test_loss,
            holdout_num,
            "[" + ", ".join(["({}, {})".format(int(item[0]), int(item[1])) for item in best_coord_set]) + "]",
            best_loss
            )
        print(message)
        with open(output_file, "at") as filehandle:
            filehandle.write(f"{write_data}\n")

    print(f"Best coordinate set is {best_coord_set} with {best_loss} loss")