# Composite HDR images from multiple exposures
A python implementation of **images alignment[1]**, **HDR[2]**, **tone mapping[3][4][5][6]**(Using cv2).   
Reference papers:    
```
[1] Greg Ward, Fast Robust Image Registration for Compositing High Dynamic Range Photographs from Hand-Held Exposures, jgt 2003.  
[2] Paul E. Debevec, Jitendra Malik, Recovering High Dynamic Range Radiance Maps from Photographs, SIGGRAPH 1997.  
[3] Rafal Mantiuk , Karol Myszkowski , Hans-Peter Seidel, A perceptual framework for contrast processing of high dynamic range images, Proceedings of the 2nd symposium on Applied perception in graphics and visualization, August 26-28, 2005, A Coroña, Spain
[4] E. Reinhard and K. Devlin, "Dynamic range reduction inspired by photoreceptor physiology," in IEEE Transactions on Visualization and Computer Graphics, vol. 11, no. 1, pp. 13-24, Jan.-Feb. 2005.
[5] Frédo Durand , Julie Dorsey, Fast bilateral filtering for the display of high-dynamic-range images, ACM Transactions on Graphics (TOG), v.21 n.3, July 2002
[6] Drago, F., Myszkowski, K., Annen, T., and Chiba, N. 2003. Adaptive logarithmic mapping for displaying high contrast scenes. Computer Graphics Forum 22, 3 (Sept.), 419--426.
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

## Process:
#### 0. Setting my camera 
```
Dimensions: 6000x4000
Device make: SONY
Device model: SLT-A77V
Color space: RGB
Color profile: sRGB IEC61966-2.1
Focal length: 18mm
Alpha channel: No
Red eye: No
Metering mode: Center-weighted average
F number: f/16
Exposure program: Manual
Exposure time: from 1/3000 to 1/2
```
#### 1. Collected images
exposures = [1/3000, 1/2000, 1/1500, 1/1000, 1/750, 1/500, 1/350, 1/250, 1/200, 1/125, 1/90, 1/60, 1/45, 1/30, 1/20, 1/15, 1/10, 1/8, 1/6, 1/4, 1/3, 0.5'']
```
Display numbers: /raw_img/img_shutter_display.txt      # raw
Float numbers: /raw_img/img_shutter_float.txt         # Usable
```
Scene1: Robotics_Corner
```
Raw images 6000*4000: stored at /raw_img/Robotics_Corner    # raw from camera
Use images 1800*1200: stored at /use_img/Robotics_Corner   # used for final production
Test images 900*600: stored at /test_img/Robotics_Corner   # used for quickly test
```
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09857.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09858.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09859.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09860.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09861.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09862.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09863.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09864.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09865.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09866.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09867.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09868.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09869.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09870.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09871.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09872.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09873.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09874.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09875.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09876.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09877.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robotics_Corner/DSC09878.jpg" width="210">  
Scene2: Robotics_Corner
```
Raw images 6000*4000: stored at /raw_img/Robot_Power    # raw from camera
Use images 1800*1200: stored at /use_img/Robot_Power   # used for final production
Test images 900*600: stored at /test_img/Robot_Power  # used for quickly test
```
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09923.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09924.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09925.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09926.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09927.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09928.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09929.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09930.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09931.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09932.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09933.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09934.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09935.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09936.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09937.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09938.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09939.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09940.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09941.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09942.jpg" width="210">
<img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09943.jpg" width="210"><img src="https://github.com/shannon112/VFXolo/blob/test/project1_hdrImage/test_img/Robot_Power/DSC09944.jpg" width="210">


#### 2. Resized images for testing
Stored at ```/test_img```  
2 test set, 2*22images, with 900x600 pixels  
Using online tranformation website: ```https://www.iloveimg.com/zh-tw/resize-image/resize-jpg```

#### 3. Alignment (MTB + Image Pyramid + Offset Search)
The method is based on a pyramid of median threshold bitmaps, which are aligned using bitwise shift and differencing operations.  
function name: ```Alignment```  
input: unaligned images  
output: aligned images  
```
Generate gassian images pyramid
Compute an median threshold bitmap for each exposure at each resolution level in our pyramid
Compute an exclusion bitmap for each exposure at each resolution level in our pyramid
Offset 1bit to generate 9 candidate 
Take the XOR difference for these candidates 
AND’ing it with both offset exclusion bitmaps to compute our final difference
Pick the min difference as the offset
At the next resolution level, we multiply this offset by 2 and repeat compute the minimum difference offset within a ±1 pixel
Continues to the highest (original) resolution MTB, where we get our final offset result
```

#### 4. Finding camera response function (CRF)

#### 5. Recover radiance map

#### x. Recover HDR image

#### x. Tone-mapped image
