import numpy as np
import keras as K
import matplotlib.pyplot as plt
import sys

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    n_rounds = int(sys.argv[1])
    print(n_rounds, "Round Iterative DES dataset using Keras/TensorFlow ")

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
            delimiter=",", skiprows=0, dtype=np.float32))
        train_y_array.append(np.loadtxt(train_data, usecols=cols_entrada[(64*(i + 1)):(64*(i + 2))],
            delimiter=",", skiprows=0, dtype=np.float32))

        test_x_array.append(np.loadtxt(test_data, usecols=cols_entrada[(64*i):(64*(i + 1))],
            delimiter=",", skiprows=0, dtype=np.float32))
        test_y_array.append(np.loadtxt(test_data, usecols=cols_entrada[(64*(i + 1)):(64*(i + 2))],
            delimiter=",", skiprows=0, dtype=np.float32))

    for (i, t) in enumerate(train_x_array):
        train_x_array[i] = t.reshape(t.shape[0], 1, t.shape[1])
    for (i, t) in enumerate(test_x_array):
        test_x_array[i] = t.reshape(t.shape[0], 1, t.shape[1])
    print(train_x_array[0].shape())

    model_array = []
    par_accuracies = []
    par_losses = []

    full_accuracies = []
    full_losses = []

    np.random.seed(0)

    for i in range(n_rounds):
        model = K.models.Sequential()
        model.add(K.layers.SimpleRNN(16))
        model.add(K.layers.Dense(units=64, activation='sigmoid'))
        model.compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])

        csv_logger = K.callbacks.CSVLogger(str(n_rounds) + 'R_' + str(i+1) +'N_iter_RNN.csv', separator=';', append=False)

        print('Starting training, network ' + str(i+1) + '\n')
        h = model.fit(train_x_array[i], train_y_array[i], batch_size=2000, epochs=200, verbose=1, validation_data = (test_x_array[i], test_y_array[i]), shuffle=False, callbacks=[csv_logger])
        print('\nTraining finished network ' + str(i+1) + '\n')

        plt.plot(h.history['custom_accuracy'])
        plt.plot(h.history['val_custom_accuracy'])
        plt.title('Model ' + str(i+1) + ' Custom Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Custom Accuracy')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('acc_' + str(n_rounds) + 'R_' + str(i+1) + 'N_iter_RNN.png', format='png')

        plt.clf()

        plt.plot(h.history['loss'])
        plt.plot(h.history['val_loss'])
        plt.title('Model ' + str(i+1) + ' Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train', 'Test'], loc='upper right')
        plt.savefig('loss_' + str(n_rounds) + 'R_' + str(i+1) + 'N_RNN.png', format='png')

        plt.clf()

        eval = model.evaluate(test_x_array[i], test_y_array[i], verbose=0)
        print('Evaluation model ' + str(i+1) +': loss = %0.6f custom_accuracy= %0.2f%%\n' \
            % (eval[0], eval[1]*100) )

        model.save('model_full_' + str(n_rounds) + 'R_' + str(i+1) + 'N_RNN.h5')
        model_array.append(model)
        par_accuracies.append(eval[1]*100)
        par_losses.append(eval[0])

    print('Partial Accuracies: ')
    for acc in par_accuracies:
        print(acc)
    print('Partial Losses: ')
    for loss in par_losses:
        print(loss)
    
    predicts = test_x_array[0]

    for i in range(16):
        eval = model_array[i].evaluate(predicts, test_y_array[i], verbose=0)
        predicts = model_array[i].predict(test_x_array[i])
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