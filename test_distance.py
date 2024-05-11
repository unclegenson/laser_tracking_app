import numpy as np


X_axis = [12,12.1,4,12.4,12.7,13,14,19.3,21,24,26,32,39]
X_distances = []

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

print(reject_outliers(np.array(X_axis)))


def reject_outliers_2(data, m=2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return data[s < m]
print(reject_outliers_2(np.array(X_axis)))


for index in range(len(reject_outliers(np.array(X_axis)))):
    if index == 0:
        pass
    else:
        X_distances.append(round(X_axis[index] - X_axis[index-1],3))

print(X_distances)

for d in X_distances:
    if d >= 2 * sum(X_distances) / len(X_distances):
        print(d)

