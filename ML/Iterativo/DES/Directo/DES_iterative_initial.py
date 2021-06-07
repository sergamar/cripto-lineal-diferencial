import numpy as np
import keras as K
import matplotlib.pyplot as plt

def custom_loss(y_act, y_pred):
    return K.backend.sum(K.backend.square(K.backend.cast(K.backend.round(y_act), 'int32') - K.backend.cast(K.backend.round(y_pred), 'int32')), 1)

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

def main():
    print("2 Round Iterative DES dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    train_data = "dataset_2R_iter_train.txt"
    test_data = "dataset_2R_iter_test.txt"

    cols_entrada = []
    for i in range(192):
        cols_entrada.append(i)

    train_x_array = []
    train_y_array = []
    test_x_array = []
    test_y_array = []

    train_x_1 = np.loadtxt(train_data, usecols=cols_entrada[:64],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    train_y_1 = np.loadtxt(train_data, usecols=cols_entrada[64:128],
        delimiter=",", skiprows=0, dtype=np.uint8)

    test_x_1 = np.loadtxt(test_data, usecols=cols_entrada[:64],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    test_y_1 = np.loadtxt(test_data, usecols=cols_entrada[64:128],
        delimiter=",", skiprows=0, dtype=np.uint8)

    train_x_2 = np.loadtxt(train_data, usecols=cols_entrada[64:128],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    train_y_2 = np.loadtxt(train_data, usecols=cols_entrada[128:],
        delimiter=",", skiprows=0, dtype=np.uint8)

    test_x_2 = np.loadtxt(test_data, usecols=cols_entrada[64:128],
        delimiter=",",  skiprows=0, dtype=np.uint8)
    test_y_2 = np.loadtxt(test_data, usecols=cols_entrada[128:],
        delimiter=",", skiprows=0, dtype=np.uint8)

    np.random.seed(0)
    model_1 = K.models.Sequential()
    model_1.add(K.layers.Dense(units=2048, activation='relu'))
    model_1.add(K.layers.Dense(units=64, activation='sigmoid'))
    model_1.compile(loss='mse', optimizer='adam', metrics=[custom_loss, custom_accuracy])

    csv_logger = K.callbacks.CSVLogger('2R_1stN_iter_2048_mse_adam.csv', separator=';', append=False)

    print("Starting training first network \n")
    h = model_1.fit(train_x_1, train_y_1, batch_size=2000, epochs=200, verbose=1, validation_data = (test_x_1, test_y_1), shuffle=False, callbacks=[csv_logger])
    print("\nTraining finished first network \n")

    plt.plot(h.history['custom_accuracy'])
    plt.plot(h.history['val_custom_accuracy'])
    plt.title('Model 1 Custom Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Accuracy')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('acc_2R_1stN_iter_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['custom_loss'])
    plt.plot(h.history['val_custom_loss'])
    plt.title('Model 1 Custom Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('custom_loss_2R_1stN_iter_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['loss'])
    plt.plot(h.history['val_loss'])
    plt.title('Model 1 Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('loss_2R_1stN_iter_2048_mse_adam.png', format='png')

    plt.clf()

    eval = model_1.evaluate(test_x_1, test_y_1, verbose=0)
    print("Evaluation model 1: loss = %0.6f custom_loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1], eval[2]*100) )

    model_1.save('model_full_2R_1stN_iter_2048_mse_adam.h5')


    model_2 = K.models.Sequential()
    model_2.add(K.layers.Dense(units=2048, activation='relu'))
    model_2.add(K.layers.Dense(units=64, activation='sigmoid'))
    model_2.compile(loss='mse', optimizer='adam', metrics=[custom_loss, custom_accuracy])

    csv_logger = K.callbacks.CSVLogger('2R_2ndN_iter_2048_mse_adam.csv', separator=';', append=False)

    print("Starting training second network \n")
    h = model_2.fit(train_x_2, train_y_2, batch_size=2000, epochs=200, verbose=1, validation_data = (test_x_2, test_y_2), shuffle=False, callbacks=[csv_logger])
    print("\nTraining finished second network \n")

    plt.plot(h.history['custom_accuracy'])
    plt.plot(h.history['val_custom_accuracy'])
    plt.title('Model 2 Custom Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Accuracy')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('acc_2R_2ndN_iter_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['custom_loss'])
    plt.plot(h.history['val_custom_loss'])
    plt.title('Model 2 Custom Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Custom Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('custom_loss_2R_2ndN_iter_2048_mse_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['loss'])
    plt.plot(h.history['val_loss'])
    plt.title('Model 2 Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.savefig('loss_2R_2ndN_iter_2048_mse_adam.png', format='png')

    eval = model_2.evaluate(test_x_2, test_y_2, verbose=0)
    print("Evaluation model 2: loss = %0.6f custom_loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1], eval[2]*100) )

    model_2.save('model_full_2R_2ndN_iter_2048_mse_adam.h5')

    predicts_1stN = model_1.predict(test_x_1)
    predicts_1stN = K.backend.cast(K.backend.round(predicts_1stN), 'int32')
    eval = model_2.evaluate(predicts_1stN, test_y_2, verbose=0)
    print("Full evaluation: loss = %0.6f custom_loss = %0.6f custom_accuracy= %0.2f%%\n" \
        % (eval[0], eval[1], eval[2]*100) )

if __name__=="__main__":
    main()