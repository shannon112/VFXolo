import numpy as np
import cv2
import itertools

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

    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1 + w2
    nHeight = max(h1, h2)
    hdif = (h1 - h2) / 2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    matched_pairs = []
    for i in range(min(len(kpi), len(kpt))):
    	pt_a = (int(kpt[i,1]), int(kpt[i,0] + hdif)) #templete points
    	pt_b = (int(kpi[i,1] + w2), int(kpi[i,0])) #img points
    	#cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
        matched_pairs.append([pt_a,pt_b])
    return matched_pairs
    #cv2.imwrite('matches.jpg', newimg)
