import numpy as np
import keras as K
import matplotlib.pyplot as plt
import sys

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    n_rounds = int(sys.argv[1])
    print(n_rounds, "Round Reverse Iterative DES dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    train_data = "dataset_" + str(n_rounds) + "R_iter_train.txt"
    test_data = "dataset_" + str(n_rounds) + "R_iter_test.txt"

    cols_entrada = []
    for i in range(64*(n_rounds + 1)):
        cols_entrada.append(i)

    train_x_array = []
    train_y_array = []
    test_x_array = []
    test_y_array = []

    for i in range(n_rounds + 1):
        train_x_array.append(np.loadtxt(train_data, usecols=cols_entrada[(64*i):(64*(i + 1))],
            delimiter=",", skiprows=0, dtype=np.uint8))
        train_y_array.append(np.loadtxt(train_data, usecols=cols_entrada[(64*(i + 1)):(64*(i + 2))],
            delimiter=",", skiprows=0, dtype=np.uint8))

        test_x_array.append(np.loadtxt(test_data, usecols=cols_entrada[(64*i):(64*(i + 1))],
            delimiter=",", skiprows=0, dtype=np.uint8))
        test_y_array.append(np.loadtxt(test_data, usecols=cols_entrada[(64*(i + 1)):(64*(i + 2))],
            delimiter=",", skiprows=0, dtype=np.uint8))

    model_array = []
    par_accuracies = []
    par_losses = []

    full_accuracies = []
    full_losses = []

    np.random.seed(0)

    for i in range(n_rounds):
        model = K.models.Sequential()
        model.add(K.layers.Dense(units=2048, input_dim=64, activation='relu'))
        model.add(K.layers.Dense(units=64, activation='sigmoid'))
        model.compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])

        csv_logger = K.callbacks.CSVLogger(str(n_rounds) + 'R_' + str(i+1) +'N_rev_2048_mse_adam.csv', separator=';', append=False)

        print('Starting training, network ' + str(i+1) + '\n')
        h = model.fit(train_y_array[n_rounds - 1 - i], train_x_array[n_rounds - 1 - i], batch_size=2000, epochs=200, verbose=1, validation_data = (test_y_array[n_rounds - 1 - i], test_x_array[n_rounds - 1 - i]), shuffle=False, callbacks=[csv_logger])
        print('\nTraining finished network ' + str(i+1) + '\n')

        plt.plot(h.history['custom_accuracy'])
        plt.plot(h.history['val_custom_accuracy'])
        plt.title('Model ' + str(i+1) + ' Custom Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Custom Accuracy')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('acc_' + str(n_rounds) + 'R_' + str(i+1) + 'N_rev_2048_mse_adam.png', format='png')

        plt.clf()

        plt.plot(h.history['loss'])
        plt.plot(h.history['val_loss'])
        plt.title('Model ' + str(i+1) + ' Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train', 'Test'], loc='upper right')
        plt.savefig('loss_' + str(n_rounds) + 'R_' + str(i+1) + 'N_rev_2048_mse_adam.png', format='png')

        plt.clf()

        eval = model.evaluate(test_y_array[n_rounds - 1 - i], test_x_array[n_rounds - 1 - i], verbose=0)
        print('Evaluation model ' + str(i+1) +': loss = %0.6f custom_accuracy= %0.2f%%\n' \
            % (eval[0], eval[1]*100) )

        model.save('model_full_' + str(n_rounds) + 'R_' + str(i+1) + 'N_rev_2048_mse_adam.h5')
        model_array.append(model)
        par_accuracies.append(eval[1]*100)
        par_losses.append(eval[0])

    print('Partial Accuracies: ')
    for acc in par_accuracies:
        print(acc)
    print('Partial Losses: ')
    for loss in par_losses:
        print(loss)

    predicts = test_y_array[n_rounds - 1]

    for i in range(n_rounds):
        eval = model_array[i].evaluate(predicts, test_x_array[n_rounds - i - 1], verbose=0)
        predicts = model_array[i].predict(test_y_array[n_rounds - i - 1])
        predicts = K.backend.cast(K.backend.round(predicts), 'int32')
        full_accuracies.append(eval[1]*100)
        full_losses.append(eval[0])

    print('Full Accuracies: ')
    for acc in full_accuracies:
        print(acc)
    print('Full Losses: ')
    for loss in full_losses:
        print(loss)

if __name__=="__main__":
    main()