import numpy as np
import keras as K
import matplotlib.pyplot as plt
import sys

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    n_rounds = int(sys.argv[1])
    print(n_rounds, "AES with no MC dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    train_data = "dataset_noMC_" + str(n_rounds) + "R_train.txt"
    test_data = "dataset_noMC_" + str(n_rounds) + "R_test.txt"

    cols_entrada = []
    for i in range(128*2):
        cols_entrada.append(i)

    train_x = np.loadtxt(train_data, usecols=cols_entrada[:128],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    train_y = np.loadtxt(train_data, usecols=cols_entrada[128:],
        delimiter=",", skiprows=0, dtype=np.uint8)

    test_x = np.loadtxt(test_data, usecols=cols_entrada[:128],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    test_y = np.loadtxt(test_data, usecols=cols_entrada[128:],
        delimiter=",", skiprows=0, dtype=np.uint8)

    np.random.seed(0)

    model = K.models.Sequential()
    model.add(K.layers.Dense(units=2048, activation='relu'))
    model.add(K.layers.Dense(units=128, activation='sigmoid'))
    model.compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])

    csv_logger = K.callbacks.CSVLogger('noMC_' + str(n_rounds) + 'R_2048_mse_adam.csv', separator=';', append=False)

    print("Starting training \n")
    h = model.fit(train_x, train_y, batch_size=2000, epochs=200, verbose=1, validation_data = (test_x, test_y), shuffle=True, callbacks=[csv_logger])
    print("\nTraining finished \n")

    plt.plot(h.history['custom_accuracy'])
    plt.plot(h.history['val_custom_accuracy'])
    plt.title('Model Custom Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Accuracy')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('acc_noMC_' + str(n_rounds) + 'R_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['loss'])
    plt.plot(h.history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('loss_noMC_' + str(n_rounds) + 'R_2048_mse_adam.png', format='png')

    eval = model.evaluate(test_x, test_y, verbose=0)
    print("Evaluation: loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1]*100) )

    model.save('model_full_noMC_' + str(n_rounds) + '_relu_adam_2048.h5')

if __name__=="__main__":
    main()