# Composite HDR images from multiple exposures
A python implementation of **images alignment**, **HDR**, **tone mapping**   
Based on papers: 
```
1. Greg Ward, Fast Robust Image Registration for Compositing High Dynamic Range Photographs from Hand-Held Exposures, jgt 2003.  
2. Paul E. Debevec, Jitendra Malik, Recovering High Dynamic Range Radiance Maps from Photographs, SIGGRAPH 1997.  
3. Raanan Fattal, Dani Lischinski, Michael Werman, Gradient Domain High Dynamic Range Compression, SIGGRAPH 2002.  
```
Instruction to run:
```
python2 hdr_img.py
```

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
Stored at ```/raw_img```  
4scene, 4*22images, each with 6000x4000 pixels  

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
