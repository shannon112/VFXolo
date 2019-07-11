# VFXolo
My NTU CSIE 7694 Digital Visual Effects (by Prof. CYY) homeworks,   
you can get more details in each ```README.md``` or ```report.pdf``` inside folders.   
> Mexican Hairless Dog, Xoloitzcuintli (/zoʊloʊiːtsˈkwiːntli/), or Xolo for short.  
<img src="https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12212255/Xoloitzcuintli-on-White-06.jpg" width="350">  

---

* project1_hdrImage
  * Alignment (MTB + Image Pyramid + Offset Search)
  * HDR (recover CRF + generate radiance map)
  * Tone mapping (opencv or Photomatix)
* project2_panorama
  * feature detection (SIFT detector, SIFT discriptor)
  * feature matching (Brute force(2-norm distance), flann(kd-tree, knn-search))
  * image matching (RANSAC finding shift)
  * stitching n blending (Linear filter on fixed width edge or entire overlapRegion, Naive overlap stitching)
  * end to end alignment (Scattering y displacement)
  * cropping

* project3_matchMove
  * structure from motion (sfm) concept
  * Blender, Voodoo, iMovie, Photoshop
