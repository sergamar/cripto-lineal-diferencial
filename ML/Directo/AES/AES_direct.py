import numpy as np
import keras as K
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import sys

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    n_rounds = int(sys.argv[1])
    print(n_rounds, "Round Direct AES dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    train_data = "dataset_" + str(n_rounds) + "R_dir_train.txt"
    test_data = "dataset_" + str(n_rounds) + "R_dir_test.txt"

    cols_entrada = []
    for i in range(128*(n_rounds + 1)):
        cols_entrada.append(i)

    train_x = np.loadtxt(train_data, usecols=cols_entrada[:128],
        delimiter=",", skiprows=0, dtype=np.uint8)
    train_y = np.loadtxt(train_data, usecols=cols_entrada[128:256],
        delimiter=",", skiprows=0, dtype=np.uint8)

    test_x = np.loadtxt(test_data, usecols=cols_entrada[:128],
        delimiter=",", skiprows=0, dtype=np.uint8)
    test_y = np.loadtxt(test_data, usecols=cols_entrada[128:256],
        delimiter=",", skiprows=0, dtype=np.uint8)

    np.random.seed(0)

    kfold = KFold(n_splits=5, shuffle=True, random_state=0)
    scores = []
    i = 1

    print("Starting training \n")
    for foldtrain, foldtest in kfold.split(train_x, train_y):
        model = K.models.Sequential()
        model.add(K.layers.Dense(units=2048, activation='relu'))
        model.add(K.layers.Dense(units=128, activation='sigmoid'))
        model.compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])

        csv_logger = K.callbacks.CSVLogger('1R_2048_mse_adam_' + str(i) + 'fold.csv', separator=';', append=False)
        h = model.fit(train_x[foldtrain], train_y[foldtrain], batch_size=1000, epochs=150, verbose=0, validation_data = (train_x[foldtest], train_y[foldtest]), shuffle=True, callbacks=[csv_logger])
        print('Fold ' + str(i) + ' accuracy: ' + str(h.history['val_custom_accuracy'][-1]))

        scores.append(h.history['val_custom_accuracy'][-1])

        plt.plot(h.history['custom_accuracy'])
        plt.plot(h.history['val_custom_accuracy'])
        plt.title('Model Custom Accuracy Fold ' + str(i))
        plt.xlabel('Epoch')
        plt.ylabel('Custom Accuracy')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('acc_1R_2048_mse_adam_' + str(i) + 'fold.png', format='png')

        plt.clf()

        plt.plot(h.history['loss'])
        plt.plot(h.history['val_loss'])
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train', 'Test'], loc='upper right')
        plt.savefig('loss_1R_2048_mse_adam_' + str(i) + 'fold.png', format='png')

        plt.clf()

        i = i + 1
    print("\nTraining finished \n")

    print('5-Fold Validation Accuracy:')
    print('%.2f%% (+/- %.2f%%)' % (np.mean(scores)*100, np.std(scores)*100))

    print('--------------------------------')

    print('Test set metrics')

    eval = model.evaluate(test_x, test_y, verbose=0)
    print("Evaluation: loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1]*100) )

if __name__=="__main__":
    main()