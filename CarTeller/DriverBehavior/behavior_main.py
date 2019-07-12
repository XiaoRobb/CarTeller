# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.models import Model
from keras.layers import Dense, Dropout, Add, Input, BatchNormalization, Activation
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Flatten
import cv2

names = ["安全驾驶",
         "使用手机 - 右手",
         "打电话 - 右手",
         "使用手机 - 左手",
         "打电话 - 右手",
         "调广播",
         "喝水",
         "向后拿东西",
         "整理头发或化妆",
         "和乘客交流"]


def vgg_std16_model(img_rows, img_cols, color_type=3):
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(img_rows, img_cols,color_type)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1000, activation='softmax'))

    #model.load_weights('../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')

    # Code above loads pre-trained data and
    model.layers.pop()
    model.add(Dense(10, activation='softmax'))
    # Learning rate is changed to 0.001
    sgd = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def main_block(x, filters, n, strides, dropout):
    # Normal part
    x_res = Conv2D(filters, (3, 3), strides=strides, padding="same")(x)  # , kernel_regularizer=l2(5e-4)
    x_res = BatchNormalization()(x_res)
    x_res = Activation('relu')(x_res)
    x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
    # Alternative branch
    x = Conv2D(filters, (1, 1), strides=strides)(x)
    # Merge Branches
    x = Add()([x_res, x])

    for i in range(n - 1):
        # Residual conection
        x_res = BatchNormalization()(x)
        x_res = Activation('relu')(x_res)
        x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
        # Apply dropout if given
        if dropout: x_res = Dropout(dropout)(x)
        # Second part
        x_res = BatchNormalization()(x_res)
        x_res = Activation('relu')(x_res)
        x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
        # Merge branches
        x = Add()([x, x_res])

    # Inter block part
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x


def build_model(input_dims, output_dim, n, k, dropout=None):
    """ Builds the model. Params:
            - n: number of layers. WRNs are of the form WRN-N-K
                 It must satisfy that (N-4)%6 = 0
            - k: Widening factor. WRNs are of the form WRN-N-K
                 It must satisfy that K%2 = 0
            - input_dims: input dimensions for the model
            - output_dim: output dimensions for the model
            - dropout: dropout rate - default=0 (not recomended >0.3)
            - act: activation function - default=relu. Build your custom
                   one with keras.backend (ex: swish, e-swish)
    """
    # Ensure n & k are correct
    assert (n - 4) % 6 == 0
    assert k % 2 == 0
    n = (n - 4) // 6
    # This returns a tensor input to the model
    inputs = Input(shape=(input_dims))

    # Head of the model
    x = Conv2D(16, (3, 3), padding="same")(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # 3 Blocks (normal-residual)
    x = main_block(x, 16 * k, n, (1, 1), dropout)  # 0
    x = main_block(x, 32 * k, n, (2, 2), dropout)  # 1
    x = main_block(x, 64 * k, n, (2, 2), dropout)  # 2

    # Final part of the model
    x = AveragePooling2D((8, 8))(x)
    x = Flatten()(x)
    outputs = Dense(output_dim, activation="softmax")(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model


def behavior_tell(img):
    """
    驾驶员行为识别
    :param img: cv2图片
    :return: 返回预测的最高的行为名称和概率
    """
    img = cv2.resize(img, (224, 224))
    model = build_model((224, 224, 3), 10, 16, 4)
    model.load_weights('./weights.h5')
    model.compile("adam", "categorical_crossentropy", ['accuracy'])
    images = [img]
    output = model.predict(np.array(images), batch_size=1)
    pro = output.max()
    index = output.argmax()
    return names[index], pro


if __name__ == "__main__":
    img = cv2.imread("./test.jpg")
    name, pro = behavior_tell(img)
    print(name, pro)