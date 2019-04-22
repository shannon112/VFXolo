# Images Stitching(Panoramas)
A python implementation of **Images Stitching(Panoramas)[1]**.   
- SIFT feature detection[2]
- feature matching[2]
- image matching
- bundle adjustment
- blending
Reference papers:    
```
[1] M. Brown, D. G. Lowe, Recognising Panoramas, ICCV 2003
[2] Matthew Brown, Richard Szeliski, Simon Winder, Multi-Image Matching using Multi-Scale Oriented Patches, CVPR 2005
```
Instruction to run:  
- Usages:    
```python2 my_hdr.py PHOTO_NAME RESOLUTION ALIGNMENT```  
PHOTO_NAME: you can choose "robot_power" or "robotics_corner"   
RESOLUTION: you can choose "1" or "0" for 1800*1200 or 900*600   
ALIGNMENT: you can choose "1" or "0" for mine or built-in method

- examples:   
```python2 my_hdr.py robot_corner 0 0```  
```python2 my_hdr.py robot_power 1 1```  
Noted that HD would take 3~5min to finish

