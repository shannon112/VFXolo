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
```For the images in folder, tne filenames should increase according to the view of landscape from the left side to the right side```
e.g.
```
DSC09994.jpg is the left side of landscape
DSC09995.jpg is the middle of landscape
DSC09996.jpg is the right side of landscape
```
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

## Structure
Files structure
```
├── project2_panoramas
│   ├── src       #source/executable code
│   ├── testing_src   #some testing code while developing
│   ├── raw_img     # 6000x4000 raw images, 5 collection
│   ├── result_img     # pano, aligned_pano, cropped_pano of each collection
│   ├── test_img     # small size image of raw_img
```

## Artifacts
**summerNight**:  
```tech: pano+crop, input_img: 12*1000x1500 from test_img/summerNight, output_img: 4354x1435```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/summerNight/2/cropped_pano.jpg" width="900">
**DEMO_parrington**:  
```tech: pano+align+crop, input_img: 18*384x512 from test_img/parrington, output_img: 4565x502```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/parrington/cropped_aligned_parrington.jpg" width="900">
**DEMO_grail**:  
```tech: pano+align+crop, input_img: 18*384x512 from test_img/grail, output_img: 4102x499```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/grail/cropped_aligned_grail.jpg" width="900">
**chasedByDog**:  
```tech: pano+crop, input_img: 10*1000x1500 from test_img/chasedByDog, output_img: 4421x1268```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/chasedByDog/4/cropped_pano.jpg" width="900">
**rainyNight**:  
```tech: pano+crop, input_img: 14*300x450 from test_img/rainyNight2, output_img: 1755x434```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/rainyNight2/cropped_final_bt_5_0.5.jpg" width="900">
**midnightStreet**:  
```tech: pano+crop, input_img: 12*533x800 from test_img/midnightStreet, output_img: 3823x728```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/midnightStreet/cropped_midnightStreet.jpg" width="900">
**dormitoryNight**:  
```tech: pano+crop, input_img: 6*533x800 from test_img/dormitoryNight, output_img: 1632x734```
<img src="https://github.com/shannon112/VFXolo/blob/test/project2_panorama/result_img/dormitoryNight/cropped_dormitoryNight.jpg" width="900">
