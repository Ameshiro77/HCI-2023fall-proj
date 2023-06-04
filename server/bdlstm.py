#!/usr/bin/env python
# coding: utf-8

# # Bidirectional LSTM for non-intrusive reduced order model of a SEIR model in an idealised town

# In[5]:

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from eofs.standard import Eof
from sklearn.model_selection import train_test_split
from tensorflow import keras as tf

plt.rcParams.update({'font.size': 8})  # 更新参数
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('axes', labelsize=18)


# Functions required to: scale and unscaled data, and to obtain lag-n data to train

# In[6]:

def scalerThetis(x, xmin, xmax, min, max):
    scale = (max - min) / (xmax - xmin)
    xScaled = scale * x + min - xmin * scale
    return xScaled


def inverseScalerThetis(xscaled, xmin, xmax, min, max):
    scale = (max - min) / (xmax - xmin)
    xInv = (xscaled / scale) - (min / scale) + xmin
    return xInv


def lookBack(X, look_back=1):
    # look_back = 10
    X_lb = np.empty((X.shape[0] - look_back + 1, look_back, X.shape[1]))
    # X_test = np.empty((look_back, X_test.shape[1], X_train.shape[0] - look_back + 1))
    ini = 0
    fin = look_back
    for i in range(X.shape[0] - look_back + 1):
        X_lb[i, :, :] = (X[ini:fin, :])
        ini = ini + 1
        fin = fin + 1
    return X_lb


# In[8]:
import os
import numpy as np

# Load data
directory = 'num/'
filename = 'group-output-time.csv'

file_dir = 'num'
files = os.listdir(file_dir)
df1 = np.genfromtxt(directory + files[0])
df1 = np.reshape(df1, (360, 1))

for e in files[1:]:
    df2 = np.genfromtxt(directory + e)
    df2 = np.reshape(df2, (360, 1))
    df1 = np.hstack([df1, df2])
print(df1)
arr = df1[:, 23:31]


# csv = np.genfromtxt(directory + filename)

ntime = 360
ngroups = 8
ngridx = 1
ngridy = 1

# csv = np.sum(csv, axis=1)
# csv = np.reshape(csv, (ntime * 8, 10))
# csv = np.sum(csv, axis=1)
#
# csv = np.reshape(csv, (ntime, 8))

groups_names = ['shanxi', 'shanxis_num', 'sichuan_num', 'tianjin_num', 'xinjiang_num', 'xizang_num', 'yunnan_num', 'zhejiang_num']
    # 'anhui', 'beijing', 'chongqing', 'fujian', 'gansu', 'guangdong', 'guangxi', 'guizhou', 'hainan',
    #             'hebei', 'heilongjiang', 'henan', 'hubei', 'hunan', 'jiangsu', 'jiangxi', 'jilin', 'liaoning',
    #             'neimenggu', 'ningxia', 'qinghai', 'shandong', 'shanghai', 'shanxi','shanxis', 'sichuan','tianjin',
    #             'xinjiang','xizang','yunnan','zhejiang']


csv1 = np.reshape(arr, (ntime, ngroups, ngridx, ngridy))
csv2 = arr
# In[ ]:

# 数据标准化
#Mask out areas where
mask = csv2[340, :].copy()  # 500行所有元素
mask = [np.where(mask == 0, 0, 1)]
mask = np.array(mask)
# mask = [[1,1,1,1,1,1,1,1]]
modeldata = np.zeros((csv2.shape[0], np.count_nonzero(mask)))
for i in range(csv2.shape[0]):
    test = csv2[i, :]
    modeldata[i, :] = test[np.where(mask == 1)[1]]
# 把原数据中所有不为零的数据提取出来，放到modeldata里面（数组大小360x160）
modeldata = csv2
# In[ ]:


# Normalising per variable
sS = modeldata[:, 0]
sE = modeldata[:, 1]
sI = modeldata[:, 2]
sR = modeldata[:, 3]

mS = modeldata[:, 4]
mE = modeldata[:, 5]
mI = modeldata[:, 6]
mR = modeldata[:, 7]
# 求平均值
sSmean = np.mean(modeldata[:, 0], axis=0)
sEmean = np.mean(modeldata[:, 1], axis=0)
sImean = np.mean(modeldata[:, 2], axis=0)
sRmean = np.mean(modeldata[:, 3], axis=0)

mSmean = np.mean(modeldata[:, 4], axis=0)
mEmean = np.mean(modeldata[:, 5], axis=0)
mImean = np.mean(modeldata[:, 6], axis=0)
mRmean = np.mean(modeldata[:, 7], axis=0)
# 计算标准差
sSsigma = np.std(modeldata[:, 0])
sEsigma = np.std(modeldata[:, 1])
sIsigma = np.std(modeldata[:, 2])
sRsigma = np.std(modeldata[:, 3])

mSsigma = np.std(modeldata[:, 4])
mEsigma = np.std(modeldata[:, 5])
mIsigma = np.std(modeldata[:, 6])
mRsigma = np.std(modeldata[:, 7])

sSn = (sS - sSmean) / sSsigma
sSn = np.reshape(sSn, (360, 1))
sEn = (sE - sEmean) / sEsigma
sEn = np.reshape(sEn, (360, 1))
sIn = (sI - sImean) / sIsigma
sIn = np.reshape(sIn, (360, 1))
sRn = (sR - sRmean) / sRsigma
sRn = np.reshape(sRn, (360, 1))

mSn = (mS - mSmean) / mSsigma
mSn = np.reshape(mSn, (360, 1))
mEn = (mE - mEmean) / mEsigma
mEn = np.reshape(mEn, (360, 1))
mIn = (mI - mImean) / mIsigma
mIn = np.reshape(mIn, (360, 1))
mRn = (mR - mRmean) / mRsigma
mRn = np.reshape(mRn, (360, 1))
# Concatenate normalised data

modeldataNorm = np.hstack([sSn, sEn, sIn, sRn, mSn, mEn, mIn, mRn])
modeldataNorm = np.reshape(modeldataNorm, (360, 8))

# In[ ]:


# modeldataNorm = (modeldata - meandata)/sigmadata
targetVariance = 0.999
solver = Eof(modeldataNorm)
varianceCumulative = np.cumsum(solver.varianceFraction())  # 累计方差
pcs = solver.pcs()  # 获取PC序列（360x8）
eofs = solver.eofs()
trun = 8
pcs_trun = pcs[:, :trun]
eofs_trun = eofs[:trun, :]

x = np.arange(1, 9)
y1 = solver.eigenvalues()[:8]  # 计算特征值
y2 = varianceCumulative[:8]  # 取累计方差的前十五列

# In[ ]:

# 对特征值和归一化累计方差和进行绘图
fig, ax1 = plt.subplots(figsize=[20, 10])  # 设置子图的高度和宽度为20，10

ax2 = ax1.twinx()  # 生成共享x轴的第二个轴
ax1.bar(x, y1)
ax1.semilogy()
ax1.bar(x, y1)

ax1.semilogy()
ax2.plot(x, y2, 'g-o', linewidth=5, markersize=10)
plt.xlim(0, 8)
plt.xticks(np.arange(1, 9))

ax1.set_xlabel('X data')

ax1.set_ylabel('Eigenvalues', color='orange')
ax2.set_ylabel('Cumulative variance', color='g')
plt.xlabel('Component')

# In[ ]:


# Reconstruct per variable重构每个变量
trun_data = np.matmul(pcs_trun, eofs_trun)  # 两个矩阵的乘积(360x8)
sStrun = trun_data[:, 0] * sSsigma + sSmean
sStrun = np.reshape(sStrun, (360, 1))
sEtrun = trun_data[:, 1] * sEsigma + sEmean
sEtrun = np.reshape(sEtrun, (360, 1))
sItrun = trun_data[:, 2] * sIsigma + sImean
sItrun = np.reshape(sItrun, (360, 1))
sRtrun = trun_data[:, 3] * sRsigma + sRmean
sRtrun = np.reshape(sRtrun, (360, 1))

mStrun = trun_data[:, 4] * mSsigma + mSmean
mStrun = np.reshape(mStrun, (360, 1))
mEtrun = trun_data[:, 5] * mEsigma + mEmean
mEtrun = np.reshape(mEtrun, (360, 1))
mItrun = trun_data[:, 6] * mIsigma + mImean
mItrun = np.reshape(mItrun, (360, 1))
mRtrun = trun_data[:, 7] * mRsigma + mRmean
mRtrun = np.reshape(mRtrun, (360, 1))
# 截尾数据
truncated_data = np.hstack([sStrun, sEtrun, sItrun, sRtrun, mStrun, mEtrun, mItrun, mRtrun])
trun_dataf = np.matmul(pcs, eofs)
sStrunf = trun_dataf[:, 0] * sSsigma + sSmean
sStrunf = np.reshape(sStrunf, (360, 1))
sEtrunf = trun_dataf[:, 1] * sEsigma + sEmean
sEtrunf = np.reshape(sEtrunf, (360, 1))
sItrunf = trun_dataf[:, 2] * sIsigma + sImean
sItrunf = np.reshape(sItrunf, (360, 1))
sRtrunf = trun_dataf[:, 3] * sRsigma + sRmean
sRtrunf = np.reshape(sRtrunf, (360, 1))

mStrunf = trun_dataf[:, 4] * mSsigma + mSmean
mStrunf = np.reshape(mStrunf, (360, 1))
mEtrunf = trun_dataf[:, 5] * mEsigma + mEmean
mEtrunf = np.reshape(mEtrunf, (360, 1))
mItrunf = trun_dataf[:, 6] * mIsigma + mImean
mItrunf = np.reshape(mItrunf, (360, 1))
mRtrunf = trun_dataf[:, 7] * mRsigma + mRmean
mRtrunf = np.reshape(mRtrunf, (360, 1))

recon_data = np.hstack([sStrunf, sEtrunf, sItrunf, sRtrunf, mStrunf, mEtrunf, mItrunf, mRtrunf])

truncated_masked = np.zeros((csv2.shape[0], csv2.shape[1]))
recon_masked = np.zeros((csv2.shape[0], csv2.shape[1]))

for i in range(csv2.shape[0]):
    test = np.zeros(csv2.shape[1])
test[np.where(mask == 1)[1]] = truncated_data[i, :]
truncated_masked[i, :] = test
test = np.zeros(csv2.shape[1])
test[np.where(mask == 1)[1]] = recon_data[i, :]
recon_masked[i, :] = test
# 回到原数据格式
trun_shaped = np.reshape(truncated_masked, (ntime, ngroups, ngridx, ngridy))
recon_shaped = np.reshape(recon_masked, (ntime, ngroups, ngridx, ngridy))

# In[ ]:

# In[ ]:


# PCS every m time-steps
initial_time_step = 0
stepBetween = 1  # 时间间隔为10个时间步长（即10000秒）
pcs_stag = pcs_trun[initial_time_step:, :]
pcs_stag = pcs_stag[0:pcs_stag.shape[0]:stepBetween, :]  # 每10个时间步长取一次数据
n_stag_time = pcs_stag.shape[0]

# Staggered original dataset
csv_stag = csv1[initial_time_step:, :, :, :]
csv_stag = csv_stag[0:csv_stag.shape[0]:stepBetween, :, :, :]

# LSTM model
min_ls = np.min(pcs_stag, 0)  # 每一列的最小值
max_ls = np.max(pcs_stag, 0)  # 每一列的最大值
min = 0
max = 1

look_backX = 8
look_backY = 1
ls_scaled = scalerThetis(pcs_stag, min_ls, max_ls, min, max)  # 归一化（388*8）

lsX = np.squeeze(ls_scaled[:-look_backY, :])  # 去掉最后一行
lsy = np.squeeze(ls_scaled[look_backY:, :])  # 去掉第一行
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(lsX, lsy, test_size=0.15, shuffle=False, random_state=42)

y_train = y_train[look_backX - 1:]
y_test = y_test[look_backX - 1:]

y_train = lookBack(y_train, look_backY)
y_test = lookBack(y_test, look_backY)

X_train = lookBack(X_train, look_backX)
X_test = lookBack(X_test, look_backX)
X_all = lookBack(lsX, look_backX)

# In[ ]:


# Create and fit the LSTM network
np.random.seed(42)

# start_time = time()
input_lstm = tf.Input((X_train.shape[1], X_train.shape[2]))
# 双向LSTM
lstm_1 = tf.layers.Bidirectional(tf.layers.LSTM(64, return_sequences=False))(input_lstm)
dropout_1 = tf.layers.Dropout(0.5)(lstm_1)
bn_1 = tf.layers.BatchNormalization()(lstm_1)
rv_1 = tf.layers.RepeatVector(look_backY)(bn_1)
# 时间分布层主要用来对输入的数据的时间维度进行切片。在每个时间步长，依次输入一项，并且依次输出一项。
dense_1 = tf.layers.TimeDistributed(tf.layers.Dense(X_train.shape[2], activation='sigmoid'))(rv_1)

lstm_model = tf.Model(input_lstm, dense_1)
lstm_model.summary()
# 编译网络
lstm_model.compile(loss='mean_squared_error', metrics=['mae'], optimizer='nadam')
# 训练网络
history = lstm_model.fit(X_train, y_train, epochs=500, batch_size=8, verbose=2, validation_data=(X_test, y_test),
                         shuffle=True)

fig = plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

# In[2]:


if look_backY == 1:
    predLSTM = lstm_model.predict(X_all)
    predLSTM = np.squeeze(predLSTM)

else:
    timesRepeat = int(np.ceil((X_all.shape[0] - look_backX) / look_backY) + 1)
    predLSTM = np.empty((0, trun))
    for i in range(timesRepeat):
        temp = np.squeeze(lstm_model.predict(np.expand_dims(X_all[i * look_backY, :, :], 0)))
        predLSTM = np.append(predLSTM, temp, axis=0)

predLSTM = inverseScalerThetis(predLSTM, min_ls, max_ls, min, max)
fig = plt.figure()
# Comparison between PCS and predPCS
for i in range(pcs_stag.shape[1]):
    plt.subplot(3, 5, i + 1)
    plt.plot(np.arange(look_backX, n_stag_time), pcs_stag[look_backX:, i])
    plt.plot(np.arange(look_backX, n_stag_time), predLSTM[:, i])

# predLSTM = np.matmul(predLSTM, eofs_trun)*sigmadata + meandata
predLSTM_masked = np.zeros((predLSTM.shape[0], csv2.shape[1]))
trun_dataL = np.matmul(predLSTM, eofs_trun)
sStrunL = trun_dataL[:, 0] * sSsigma + sSmean
sEtrunL = trun_dataL[:, 1] * sEsigma + sEmean
sItrunL = trun_dataL[:, 2] * sIsigma + sImean
sRtrunL = trun_dataL[:, 3] * sRsigma + sRmean

sStrunL = np.reshape(sStrunL, (352, 1))
sEtrunL = np.reshape(sEtrunL, (352, 1))
sItrunL = np.reshape(sItrunL, (352, 1))
sRtrunL = np.reshape(sRtrunL, (352, 1))

mStrunL = trun_dataL[:, 4] * mSsigma + mSmean
mEtrunL = trun_dataL[:, 5] * mEsigma + mEmean
mItrunL = trun_dataL[:, 6] * mIsigma + mImean
mRtrunL = trun_dataL[:, 7] * mRsigma + mRmean

mStrunL = np.reshape(mStrunL, (352, 1))
mEtrunL = np.reshape(mEtrunL, (352, 1))
mItrunL = np.reshape(mItrunL, (352, 1))
mRtrunL = np.reshape(mRtrunL, (352, 1))

predLSTM = np.hstack([sStrunL, sEtrunL, sItrunL, sRtrunL, mStrunL, mEtrunL, mItrunL, mRtrunL])
for i in range(predLSTM.shape[0]):
    test = np.zeros(csv2.shape[1])
    test[np.where(mask == 1)[1]] = predLSTM[i, :]
    predLSTM_masked[i, :] = test
for i in range(predLSTM_masked.shape[0]):
    for j in range(predLSTM_masked.shape[1]):
        if predLSTM_masked[i, j] < 0:
            predLSTM_masked[i, j] = 0
        # predLSTM_masked[i, j] = eval(predLSTM_masked[i, j])
predLSTM_shaped = np.reshape(predLSTM_masked, (n_stag_time - look_backX, ngroups, ngridx, ngridy))

# Fixed point over time
fig = plt.figure(figsize=(20, 8))  # 在绘图之前，创建一个Figure对象
for i in range(8):  # 8个图
    plt.subplot(4, 2, i + 1)  # 生成Axes轴
    # x = range(0, 47, 1)
    x = pd.date_range(start='2022/03/07', end='2022/06/21', freq='D')
    plt.plot(np.arange(8, 360), csv_stag[look_backX:, i, 0, 0])
    plt.plot(np.arange(8, 360), predLSTM_shaped[:, i, 0, 0])

    np.savetxt('results_num/'+groups_names[i]+'.csv', predLSTM_shaped[:, i, 0, 0], delimiter = ',')
    plt.axvline(x=n_stag_time * 0.85, color='g')
    plt.title(groups_names[i])
    plt.legend(['Ground truth', 'Prediction'])
plt.tight_layout()
plt.show()

# In[ ]:
