import numpy as np
import cv2
import itertools
import math

def sift_matching(templatename, imagename, kpt,dt,kpi,di, cutoff):

    img = cv2.imread(imagename)
    template = cv2.imread(templatename)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(np.asarray(di, np.float32), flann_params)
    idx, dist = flann.knnSearch(np.asarray(dt, np.float32), 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]

    kpi_cut = []
    for i, dis in itertools.izip(idx, dist):
    	if dis < cutoff:
    		kpi_cut.append(kpi[i])
    	else:
    		break

    kpt_cut = []
    for i, dis in itertools.izip(indices, dist):
    	if dis < cutoff:
    		kpt_cut.append(kpt[i])
    	else:
    		break

    #if scanning view from left turn to right
    matched_pairs = []
    matched_x_max_thres = 240
    matched_x_min_thres = 60
    matched_y_abs_thres = 20

    for i in range(np.array(kpi_cut).shape[0]):
        distance_x = kpt_cut[i][1] - kpi_cut[i][1]
        distance_y = abs(kpt_cut[i][0] - kpi_cut[i][0])
        if distance_y<matched_y_abs_thres and distance_x < matched_x_max_thres and distance_x > matched_x_min_thres:
            pt_a = (int(kpt_cut[i][1]), int(kpt_cut[i][0]))
            pt_b = (int(kpi_cut[i][1]), int(kpi_cut[i][0]))
            matched_pairs.append([pt_a,pt_b])
    print matched_pairs
    return matched_pairs
