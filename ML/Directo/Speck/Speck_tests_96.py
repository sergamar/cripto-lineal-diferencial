import numpy as np
import keras as K
import matplotlib.pyplot as plt
import sys

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    n_rounds = int(sys.argv[1])
    print(n_rounds, "Round Direct Speck 96 dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    data = "dataset_" + str(n_rounds) + "R_96_dir_train_test.txt"

    cols_entrada = []
    for i in range(96*2):
        cols_entrada.append(i)

    x = np.loadtxt(data, usecols=cols_entrada[:96],
        delimiter=",", skiprows=0, dtype=np.uint8)
    y = np.loadtxt(data, usecols=cols_entrada[96:192],
        delimiter=",", skiprows=0, dtype=np.uint8)

    train_x = x[:int(round(len(x) * 0.7))]
    train_y = y[:int(round(len(y) * 0.7))]
    test_x = x[int(round(len(x) * 0.7)):]
    test_y = y[int(round(len(y) * 0.7)):]

    np.random.seed(0)
    model = K.models.Sequential()
    model.add(K.layers.Dense(units=2048, activation='relu'))
    model.add(K.layers.Dense(units=96, activation='sigmoid'))
    model.compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])

    csv_logger = K.callbacks.CSVLogger(str(n_rounds) + 'R_96_2048_mse_adam.csv', separator=';', append=False)

    print("Starting training \n")
    h = model.fit(train_x, train_y, batch_size=2000, epochs=200, verbose=1, validation_data = (test_x, test_y), shuffle=True, callbacks=[csv_logger])
    print("\nTraining finished \n")

    plt.plot(h.history['custom_accuracy'])
    plt.plot(h.history['val_custom_accuracy'])
    plt.title('Model Custom Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Accuracy')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('acc_' + str(n_rounds) + 'R_96_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['loss'])
    plt.plot(h.history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('loss_' + str(n_rounds) + 'R_96_2048_mse_adam.png', format='png')

    eval = model.evaluate(test_x, test_y, verbose=0)
    print("Evaluation: loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1]*100) )

    model.save('model_full_' + str(n_rounds) +'R_96_relu_adam_2048.h5')

if __name__=="__main__":
    main()