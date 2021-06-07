import numpy as np
import keras as K
import matplotlib.pyplot as plt

def custom_accuracy(y_act, y_pred):
    return K.backend.cast(K.backend.round(y_act), 'int32') == K.backend.cast(K.backend.round(y_pred), 'int32')

custom_functions = {
    'custom_accuracy': custom_accuracy
}

print("Loading data into memory \n")
test_data = "dataset_16R_iter_test.txt"

train_x_array = []
train_y_array = []
test_x_array = []
test_y_array = []

cols_entrada = []
for i in range(64*(17)):
    cols_entrada.append(i)

for i in range(17):
    test_x_array.append(np.loadtxt(test_data, usecols=cols_entrada[:(64*i)],
        delimiter=",", skiprows=0, dtype=np.uint8))
    test_y_array.append(np.loadtxt(test_data, usecols=cols_entrada[(64*i):(64*(i+1))],
        delimiter=",", skiprows=0, dtype=np.uint8))

full_accuracies = []
full_losses = []

model_array = []

for i in range(16):
    model = K.models.load_model('model_full_16R_' + str(i+1) + 'N_iter_2048_mse_adam.h5', custom_objects=custom_functions)
    model_array.append(model)

predicts = test_x_array[0]

for i in range(16):
    model_array[i].compile(loss='mse', optimizer='adam', metrics=[custom_accuracy])
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
