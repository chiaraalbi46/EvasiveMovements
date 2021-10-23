""" Prove calcolo metriche ADE, FDE """

import numpy as np
import pickle


# idee
# TODO: vedere se mettere da altre parti

def ADE(out, labels):  # Average Displacement Error
    distances = []
    for u in range(out.shape[0]):
        predicted = out[u].detach().numpy()
        real = labels[u].detach().numpy()

        dist_x = real[:, 0] - predicted[:, 0]  # [(xo - xo^), ..., (xn - xn^)]  # n= len_seq
        # print("dist_x: ", dist_x)
        dist_y = real[:, 1] - predicted[:, 1]  # [(yo - yo^), ..., (yn - yn^)]
        # print("dist_y: ", dist_y)
        dist = dist_x ** 2 + dist_y ** 2  # [(xo - xo^)^2 + (yo - yo^)^2, ..., (xn - xn^)^2 + (yn - yn^)^2]
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
        # print("dist_x: ", dist_x)
        dist_last_y = real[:, 1][-1] - predicted[:, 1][-1]  # (yn - yn^)
        # print("dist_y: ", dist_y)
        dist = dist_last_x ** 2 + dist_last_y ** 2  # (xn - xn^)^2 + (yn - yn^)^2

        last_distances.append(dist)

    FDE = np.mean(last_distances)  # media su tutti i real, predicted di out, labels (20)

    return FDE


# f = open('store.pckl', 'wb')
# pickle.dump([im, gs], f)
# f.close()

# f1 = open('store1.pckl', 'rb')
# out, labels = pickle.load(f1)
# f1.close()
#
# f = open('store.pckl', 'rb')
# real0, predicted0 = pickle.load(f)
# f.close()
#
# dist_x = real0[:, 0] - predicted0[:, 0]
# # print("dist_x: ", dist_x)
# dist_y = real0[:, 1] - predicted0[:, 1]
# # print("dist_y: ", dist_y)
# dist = dist_x ** 2 + dist_y ** 2  # np.sqrt()
# print("dist_mean out 0: ", np.mean(dist))
#
# distance = []
# da = 0
# for u in range(len(out)):
#     predicted = out[u].detach().numpy()
#     real = labels[u].detach().numpy()
#     if u == 0:
#         predo = predicted
#         realo = real
#     s = 0
#     for k in range(len(real)):
#         rx = real[:, 0][k]
#         px = predicted[:, 0][k]
#         dx = rx - px
#
#         ry = real[:, 1][k]
#         py = predicted[:, 1][k]
#         dy = ry - py
#
#         d = dx ** 2 + dy ** 2
#         s = s + d
#
#     s_mean = s / len(real)  # np.mean(dist) ok
#     if u == 0:
#         print("s_mean 0: ", s_mean)
#     da = da + s_mean
#     distance.append(s_mean)
#
# da_mean = da / len(out)
# print("da_mean: ", da)
# distance_mean = np.mean(distance)
# print("distance_mean: ", distance_mean)
#
# ade = ADE(out, labels)
# print("ade: ", ade)


