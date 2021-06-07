import numpy as np
import keras as K
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def recall(y_true, y_pred):
    true_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true * y_pred, 0, 1)))
    total_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true, 0, 1)))
    recall = true_positives / total_positives
    return recall

def precision(y_true, y_pred):
    true_positives = K.backend.sum(K.backend.round(K.backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.backend.sum(K.backend.round(K.backend.clip(y_pred, 0, 1)))
    precision = true_positives / predicted_positives
    return precision

def f1(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * ((p * r) / (p + r))

def main():
    print("4 Round Differential DES dataset using Keras/TensorFlow ")

    print("Loading data into memory \n")
    train_data = "dataset_4R_train.txt"
    test_data = "dataset_4R_test.txt"

    cols_entrada = []
    for i in range(64):
        cols_entrada.append(i)

    train_x = np.loadtxt(train_data, usecols=cols_entrada,
        delimiter=",",  skiprows=0, dtype=np.uint8)
    train_y = np.loadtxt(train_data, usecols=[64, 65],
        delimiter=",", skiprows=0, dtype=np.uint8)

    test_x = np.loadtxt(test_data, usecols=cols_entrada,
        delimiter=",",  skiprows=0, dtype=np.uint8)
    test_y = np.loadtxt(test_data, usecols=[64, 65],
        delimiter=",", skiprows=0, dtype=np.uint8)

    np.random.seed(0)
    model = K.models.Sequential()
    model.add(K.layers.Dense(units=2048, input_dim=64, activation='relu'))
    model.add(K.layers.Dense(units=2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', recall, precision, f1])

    print("Starting training \n")
    h = model.fit(train_x, train_y, batch_size=1000,
        epochs=300, verbose=1, validation_data=(test_x, test_y))
    print("\nTraining finished \n")

    plt.plot(h.history['accuracy'])
    plt.plot(h.history['val_accuracy'])
    plt.title('Acierto del modelo')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
    plt.savefig('acc_4R_2048_cce_adam_2048.png', format='png')

    plt.clf()

    plt.plot(h.history['loss'])
    plt.plot(h.history['val_loss'])
    plt.title('Pérdida del modelo')
    plt.xlabel('Época')
    plt.ylabel('Pérdida')
    plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
    plt.savefig('loss_4R_2048_cce_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['recall'])
    plt.plot(h.history['val_recall'])
    plt.title('Exhaustividad del modelo')
    plt.xlabel('Época')
    plt.ylabel('Exhaustividad')
    plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
    plt.savefig('rec_4R_2048_cce_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['precision'])
    plt.plot(h.history['val_precision'])
    plt.title('Precisión del modelo')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
    plt.savefig('prec_4R_2048_cce_adam.png', format='png')

    plt.clf()

    plt.plot(h.history['f1'])
    plt.plot(h.history['val_f1'])
    plt.title('F1 Score del modelo')
    plt.xlabel('Época')
    plt.ylabel('F1 Score')
    plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
    plt.savefig('f1_6R_2048_cce_adam.png', format='png')

    eval = model.evaluate(test_x, test_y, verbose=0)
    print("Evaluation: loss = %0.6f accuracy = %0.2f%% recall = %0.2f%% precision = %0.2f%% f1 = %0.2f\n" \
        % (eval[0], eval[1]*100, eval[2]*100, eval[3]*100, eval[4]) )

    pred_y = model.predict(test_x)
    pred_y = np.argmax(pred_y, axis=1)
    test_y = np.argmax(test_y, axis=1)


    print('Matriz de confusión')
    print(confusion_matrix(test_y, pred_y))

    model.save('model_full_4R.h5')

if __name__=="__main__":
    main()