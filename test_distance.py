import numpy as np


X_axis = [12,12.1,12.8,12.2,12.3,12.4,12.6,12.7,45,15]


def reject_outliers(data, m = 3.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]
X_distances = []
X_axis = reject_outliers(np.array(X_axis))


for index in range(len(X_axis)):
    if index == 0:
        pass
    else:
        result = round(X_axis[index] - X_axis[index-1],3)
        if result != 0:
            X_distances.append(result)


for x_distance in X_distances:
    print(x_distance)
    if abs(x_distance) >=  2 * abs(sum(X_distances) / len(X_distances)):
        print('paresh',x_distance)

    elif abs(x_distance) <=  abs(sum(X_distances) / len(X_distances)) / 3:
        print('mane',x_distance)

