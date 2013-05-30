#!/usr/bin/env python

import os
import utils
from PIL import Image
from PIL import ImageOps
import numpy as np
import leargist
import pickle
import heapq

class ImgBase:
    def __init__(self):
        self.dir = utils.get_config()['ImageBase']['Path']

    def build_index(self):
        if self.is_index_built():
            # index has been built, just load it
            self.load_data()
            return

        feature_num = 960
        bit = 64
        # store the original feature matrix
        data = np.ndarray(shape = (0, feature_num), dtype = np.float32)
        names = []
        for name in os.listdir(self.dir):
            file_path = os.path.join(self.dir, name)
            # don't recursively search file
            if os.path.isfile(file_path):
                im = Image.open(file_path)
                des = leargist.color_gist(im)
                data = np.vstack((data, des))
                names.append(name)
        # apply PCA
        self.mean = data.mean(axis = 0)
        data -= self.mean
        u, s, v = np.linalg.svd(np.cov(np.transpose(data)))
        self.pca = u[:, :bit]
        data = data.dot(self.pca)
        # use ITQ to get the best rotation
        codes, self.rotation = utils.itq(data)
        # convert 0-1 codes matrix  to integer
        int_codes = np.zeros(shape = (codes.shape[0], 1), dtype = np.uint64)
        for i in range(codes.shape[1]):
            col = codes[:, i].astype(np.uint64).reshape(codes.shape[0], 1) * (2 << i)
            int_codes = int_codes + col
        self.cache = zip(int_codes.flatten().tolist(), names)
        self.save_data()

    def search(self, img_path):
        im = Image.open(img_path)
        #im = ImageOps.fit(im, (64, 64))
        des = leargist.color_gist(im)
        code_vec = (des - self.mean).dot(self.pca).dot(self.rotation)
        code = 0
        for i in range(code_vec.shape[0]):
            if code_vec[i] >= 0:
                code += 2 << i
        iter = []
        for item in self.cache:
            dist = utils.hamming_dist(code, item[0])
            iter.append((dist, os.path.join(self.dir, item[1])))
        # Find 64 similar images
        n = 64
        res = heapq.nsmallest(n, iter)
        return [item[1] for item in res]


        
    def is_index_built(self):
        return os.path.exists(utils.get_config()['ImageBase']['Index'])

    def save_data(self):
        pickle.dump(self.cache, open(utils.get_config()['ImageBase']['Index'], 'wb'))
        pickle.dump([self.mean, self.pca, self.rotation], \
                    open(utils.get_config()['ImageBase']['Meta'], 'wb'))

    def load_data(self):
        self.cache = pickle.load(open(utils.get_config()['ImageBase']['Index']))
        self.mean, self.pca, self.rotation = pickle.load( \
                    open(utils.get_config()['ImageBase']['Meta']))


if __name__ == '__main__':
    base = ImgBase()
    base.build_index()
    res = base.search('./images/1549.png')
    for i in res:
        print i



