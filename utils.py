#!/usr/bin/env python2

import json
import numpy as np

CONFIG_FILE = './config.json'

def get_config():
    js = json.load(open(CONFIG_FILE))
    return js

def itq(data):
    bit = data.shape[1]
    # initialize with a random orthogonal rotation
    r = np.random.randn(bit, bit)
    u, s, v = np.linalg.svd(r)
    r = u
    # iterate 20 tiems
    for i in range(20):
        z = data.dot(r)
        ux = np.ones(z.shape) * -1
        ux[z >= 0] = 1;
        c = np.transpose(ux).dot(data)
        ub, s, ua = np.linalg.svd(c)
        r = ua.dot(np.transpose(ub))
    z = data.dot(r)
    b = np.zeros(z.shape)
    b[z >= 0] = 1
    print 'b', b.shape
    return b, r

def hamming_dist(a, b):
    c = a ^ b
    count = 0
    while c:
        count += 1
        c &= c - 1
    return count

if __name__ == '__main__':
    js = get_config()
    print js
