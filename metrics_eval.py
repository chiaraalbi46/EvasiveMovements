""" Prove calcolo metriche ADE, FDE """

import numpy as np


def ADE(out, labels):  # Average Displacement Error
    distances = []
    for u in range(out.shape[0]):
        predicted = out[u].detach().numpy()
        real = labels[u].detach().numpy()

        dist_x = real[:, 0] - predicted[:, 0]  # [(xo - xo^), ..., (xn - xn^)]  # n= len_seq
        dist_y = real[:, 1] - predicted[:, 1]  # [(yo - yo^), ..., (yn - yn^)]
        # [sqrt((xo - xo^)^2 + (yo - yo^)^2), ..., sqrt((xn - xn^)^2 + (yn - yn^)^2)]
        dist = np.sqrt(dist_x ** 2 + dist_y ** 2)
        ad = np.mean(dist)  # media su real, predicted corrente  (10)
        # print("ad: ", ad)

        distances.append(ad)

    ADE = np.mean(distances)  # media su tutti i real, predicted di out, labels (20)

    return ADE


def FDE(out, labels):  # Final Displacement Error
    last_distances = []
    for u in range(out.shape[0]):
        predicted = out[u].detach().numpy()
        real = labels[u].detach().numpy()

        dist_last_x = real[:, 0][-1] - predicted[:, 0][-1]  # (xn - xn^)  # n= len_seq
        dist_last_y = real[:, 1][-1] - predicted[:, 1][-1]  # (yn - yn^)
        dist = np.sqrt(dist_last_x ** 2 + dist_last_y ** 2)  # sqrt((xn - xn^)^2 + (yn - yn^)^2)

        last_distances.append(dist)

    FDE = np.mean(last_distances)  # media su tutti i real, predicted di out, labels (20)

    return FDE



