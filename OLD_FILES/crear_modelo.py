from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.layers.core import Dense, Activation
from keras.layers.advanced_activations import PReLU
from keras.optimizers import SGD , Adam, RMSprop
def cnn_modelo(alto,ancho):
    im_shape = (alto,ancho,12)
    model = Sequential()
    print((None,*im_shape))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=im_shape))
    print(model.output_shape)
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=im_shape))
    print(model.output_shape)
    model.add(Conv2D(128, (3, 3), activation='relu', input_shape=im_shape))
    print(model.output_shape)
    #model.add(Conv2D(64, (3, 3), activation='relu'))
    #print(model.output_shape)
    #model.add(MaxPool2D((2, 2)))
    #print(model.output_shape)
    #model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.2))
    model.add(Flatten())
    print(model.output_shape)
    #model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    #print(model.output_shape)
    #model.add(Conv2D(128, (3, 3), activation='relu'))
    #print(model.output_shape)
    model.add(Dense(alto*ancho))
    print(model.output_shape)
    model.add(PReLU())
    #model.add(Dense(alto*ancho))
    #model.add(PReLU())
    model.add(Dense(alto*ancho))
    print(model.output_shape)
    model.compile(optimizer='adam', loss='mse')
    return model
def save_model(model):
    with open("model.json", "w") as json_file:
        json_file.write(model.to_json())
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")