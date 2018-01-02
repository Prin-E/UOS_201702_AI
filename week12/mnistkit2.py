# -*- coding: utf-8 -*-

import os
import os.path as op
import struct as st
import numpy as np
import matplotlib.pyplot as plt

# MNIST 데이터 경로
_SRC_PATH = u'../data'
_TRAIN_DATA_FILE = _SRC_PATH + u'/train-images.idx3-ubyte'
_TRAIN_LABEL_FILE = _SRC_PATH + u'/train-labels.idx1-ubyte'
_TEST_DATA_FILE = _SRC_PATH + u'/t10k-images.idx3-ubyte'
_TEST_LABEL_FILE = _SRC_PATH + u'/t10k-labels.idx1-ubyte'

# MNIST 데이터 크기 (28x28)
_N_ROW = 28                 # 세로 28픽셀
_N_COL = 28                 # 가로 28픽셀
_N_PIXEL = _N_ROW * _N_COL

# MNIST 각 데이터 샘플을 간단히 다루기 위한 클래스
class mnist_sample_t:
    def __init__(self):
        self.data = np.array(0)
        self.label = 0
    
    def set(self, new_data_arr, new_label):
        # bias, 데이터
        self.data = np.append(1, new_data_arr)
        # 레이블 0~9
        self.label = new_label
    
def loadData(fn):
    fd = open(fn, 'rb')
    
    # header: 32bit integer (big-endian)
    magicNumber = st.unpack('>I', fd.read(4))[0]
    nData = st.unpack('>I', fd.read(4))[0]
    nRow = st.unpack('>I', fd.read(4))[0]
    nCol = st.unpack('>I', fd.read(4))[0]

    # data: unsigned byte
    dataArr = []
    for i in range(nData):
        dataRawList = fd.read(_N_PIXEL)
        dataNumList = st.unpack('B' * _N_PIXEL, dataRawList)
        dataArr.extend(dataNumList)
    
    fd.close()
    dataList = np.array(dataArr)
    dataList = dataList.astype('float') / 255.0
    dataList = dataList.reshape(-1, _N_ROW, _N_COL, 1)
    return dataList
    
def loadLabel(fn):
    fd = open(fn, 'rb')
    
    # header: 32bit integer (big-endian)
    magicNumber = st.unpack('>I', fd.read(4))[0]
    nData = st.unpack('>I', fd.read(4))[0]
    
    # data: unsigned byte
    labelArr = []
    for i in range(nData):
        dataLabel = st.unpack('B', fd.read(1))[0]
        for j in range(10):
            if j == dataLabel:
                labelArr.append(1)
            else:
                labelArr.append(0)

    fd.close()

    labelList = np.array(labelArr)
    labelList = labelList.reshape(-1, 10)
    return labelList

# 학습용 데이터 불러오기
def loadMNIST_Train():
    trDataList = loadData(_TRAIN_DATA_FILE)
    trLabelList = loadLabel(_TRAIN_LABEL_FILE)
    return trDataList, trLabelList

# 테스트용 데이터 불러오기
def loadMNIST_Test():
    tsDataList = loadData(_TEST_DATA_FILE)
    tsLabelList = loadLabel(_TEST_LABEL_FILE)
    return tsDataList, tsLabelList
