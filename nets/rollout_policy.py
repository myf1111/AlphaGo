#-*- coding: utf-8 -*-

from utils.base import *

from keras.models import Sequential
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.convolutional import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.optimizers import SGD
from keras.callbacks import Callback
from keras import backend as K

k = 32
bsize = 16
epoch = 350
lrate = 0.003

SAVE_FOLDER_NAME = "20160511_rollout"

POSTFIX = ".csv"
OTHER_TRAIN_FOLDER = "train_other_rollout/"
OTHER_TEST_FOLDER = "test_other_rollout/"

def hidden_layers(m, k):
    m.add(ZeroPadding2D(padding=(2, 2)))
    m.add(Convolution2D(k, 3, 3))
    m.add(Activation('relu'))
    
    return m

def load_dataset():
    FOLDER = list()
    FOLDER.append(OTHER_TRAIN_FOLDER)
    xs, ys = list(), list()
    for folder in FOLDER:
        file_names = get_file_names(folder, POSTFIX)
        for name in file_names:
            datas = list()
            cur_rows = list()
            csvfile =  open(folder+name)
            row_reader = csv.reader(csvfile)
            if name[-5] == 'x':
                for row in row_reader:
                    if len(row) == 0:
                        datas.append(cur_rows)
                        cur_rows = list()
                        continue
                    c = list()
                    for a in row:
                        c.append(a)
                    cur_rows.append(c)
                xs.append(datas)
                datas = list()
                fname = name[:len(name)-5]+"y.csv"
                f = open(folder + fname)
                rreader = csv.reader(f)
                for row in rreader:
                    for a in row:
                        datas.append(a)
                ys.append(datas)
    
    
    xs = np.asarray(xs, dtype=np.float)
    ys = np.asarray(ys, dtype=np.float)
    print "xs", xs.shape, "ys", ys.shape
    return xs, ys


class save_callback(Callback):

    def on_epoch_end(self, epoch, logs={}):
        self.model.save_weights(SAVE_FOLDER_NAME+"/rollout_policy_net_weights_"+str(epoch)+".h5")

if __name__ == "__main__":
    
    print "load dataset.."
    #train_x, train_y = load_dataset()
    print "..finish"
    
    print "make model.."
    model = Sequential()
    
    model.add(ZeroPadding2D(padding=(1, 1), input_shape=(38, 9, 9)))
    model.add(Convolution2D(k, 5, 5))
    model.add(Activation('relu'))
    
    for i in range(0, 2):
        model = hidden_layers(model, k)
    
    model.add(ZeroPadding2D(padding=(1, 1)))
    model.add(Convolution2D(1, 1, 1))
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(81))
    model.add(Activation('softmax'))
    
    print "..finish"
    
    json_string = model.to_json()
    open(SAVE_FOLDER_NAME+"/rollout_policy_net_model.json", "w").write(json_string)
    '''sgd = SGD(lr=lrate, decay=0.0, momentum=0.0, nesterov=False)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)   
    stop = save_callback()
    model.fit(train_x, train_y, batch_size=bsize, nb_epoch=epoch, callbacks=[stop], show_accuracy=True, verbose=2)'''
    
    
    
    