# Images Stitching(Panoramas)
A python implementation of **Images Stitching(Panoramas)[1]**.   
- feature detection[2] ```SIFT detector, SIFT discriptor```
- feature matching ```Brute force(2-norm distance), flann(kd-tree, knn-search)```
- image matching```RANSAC finding shift```
- blending```Linear filter on edge, Linear filter on overlapRegion, Naive overlap stitching```
- end to end alignment```Scattering y displacement```
- cropping  

Reference papers:    
```
[1] M. Brown, D. G. Lowe, Recognising Panoramas, ICCV 2003
[2] Matthew Brown, Richard Szeliski, Simon Winder, Multi-Image Matching using Multi-Scale Oriented Patches, CVPR 2005
```

## Instruction to run:  
1. Create a folder of images  
```For the images in folder, tne filenames should increase according to the view from left to right```
2. Create info.txt in the image folder  
```The focal lengths in info.txt are gotten from autostitch(win7 old ver.), and should list from top to bottom with filenames increasing.```
e.g.
```
DSC09994.jpg 628.57
DSC09995.jpg 631.311
...
```
3. Run the image stitching program at VFXolo/project2_panoramas e.g.
```
python2 src/main.py test_img/dormitoryNight
```
4. If you are not satisfied with the result, you can tune the parameters in ```constant.py```
