# NTU Mcdonalds Mystery 台大麥當勞神秘魔法陣
### (NTU VFX 2019 spring project#3 matchMove)
Related Software:
```
Blender (Win64_2.6.2 -> Win64_2.79b)
Voodoo (Win32_1.2.0)
iMovie (Mac_10.1.11)
Photoshop (Mac_CC 2018)
```
Final Artifact on Youtube: 
[![youtube_video](https://i.imgur.com/in9swJX.png)](https://www.youtube.com/watch?v=Ez4CHCjBK3o)
![](https://i.imgur.com/in9swJX.png | width=840)

Final Artifact filename: ```Final_artifact.mp4```  
First animation clip filename: ```suc_v2 (Converted).mov```  
Second animation clip filename: ```suc_walk (Converted).mov```  
  
Handout: https://www.csie.ntu.edu.tw/~cyy/courses/vfx/19spring/assignments/proj3/index.html  
General instruction: https://www.csie.ntu.edu.tw/~cyy/courses/vfx/19spring/assignments/proj3/MatchMove_vfx2017.pdf

# Blender techniques
### 1.Selecting
ref: https://www.youtube.com/watch?v=guLSfezNjZw  
```
select all = double press 'a'
select object = click that object on the right panel so that you could select all parts of that object
```
ref: https://blender.stackexchange.com/questions/84632/how-do-i-select-and-deselect-only-one-object
```
Lasso select = allows you to draw a selection polygon. holding ⎈ Ctrl while dragging the action mouse LMB around. 
deselection = By using ⇧ Shift⎈ CtrlLMB you can draw a deselection polygon, any items within this polygon will be deselected.
```

### 2.View control
ref: https://www.youtube.com/watch?v=RNBYuYRFQe0  
setting
```
File -> User preference -> Interface -> select "Zoom to Mouse Position"
File -> User preference -> Interface -> select "Rotate Around Selection"
File -> User preference -> Input -> select "Emulate 3 Button Mouse"
Save as default
```
three button control view
```
zoom in/out: scroll mouse middle wheel to zoom in/out at mouse position
rotate: select object and click middle wheel to rotate around object
padding: hold shift and click middle wheel to pad
```
two button control view
```
zoom in/out: ctrl + alt + left mouse to zoom in/out at mouse position
rotate: select object and alt+left mouse to rotate around object
padding: hold shift+alt and left mouse to pad
```

### 3.Resume to default setting
```
file -> load factory setting
file -> sava as user default
```

### 4. 3D model
create a plane with texture  
ref: https://www.youtube.com/watch?v=il7ajiCepus  
```
create a plane 
https://blender.stackexchange.com/questions/7465/create-a-flat-plane-with-beveled-edges
editing texture
```
using texture with transparency property(.png)  
ref: https://blender.stackexchange.com/questions/78917/how-to-render-transparent-textures-in-blender-render  
```
-> On Material Tab, go to Transparency Section, activate leaves' Material transparency
-> set it's transparency mode to "Z Transparency"
-> then set the Alpha value to 0.
-> On Texture Tab, go to Influence Section, tick Alpha and set it's value to 1. 
-> Don't forget to tick Use Alpha on Image Section.
```
import 3D model
```
model要先load進來看看顏色對不對能不能用 (press F12 or select "render camera"
remember to turn on the light (use add -> lamp)
```
mirror object  
ref: https://docs.blender.org/manual/en/latest/editors/3dview/object/editing/transform/mirror.html  
```
To mirror a selection along a particular global axis press: Ctrl-M, followed by X, Y or Z
```
walking  
ref: https://www.youtube.com/watch?v=gFf5eGCjUUg  
```
walking type 
```

### 5. Output as video
Video Sequence Editor -> scene track -> property -> Scene -> Alpha M -> Set Sky to Transparent  
ref: https://blender.stackexchange.com/questions/28772/background-image-is-not-displaying-in-rendered-mode  

### 6. Mask (or filter)
Using layer to mask out object  
ref: https://www.youtube.com/watch?v=xbdfpo4dOyk  

# Material Reference
- Audio - fire sound effect: https://www.youtube.com/watch?v=mz9ftphTWTM   
- Audio - footstep sound effect: https://www.youtube.com/watch?v=btiw_49DeUU  
- Audio - evil laught sound effect: https://www.youtube.com/watch?v=btiw_49DeUU  
- Musice - BGM(Y files): https://www.youtube.com/audiolibrary_download?vid=f46f035db51fce50  
- 3Dmodel - Ronald McDonald: https://3dwarehouse.sketchup.com/model/ee6e706488291a8cb60886b233d6cbd8/Ronald-McDonald  
- 3Dmodel - Fire: https://3dwarehouse.sketchup.com/model/3f272748fccff4dbccbc9e602dbf6a4a/FIRE  
- Picture - McDonalds stand1: https://www.mynewshub.tv/wp-content/uploads/2017/01/mcd-sg.jpg  
- Picture - McDonalds stand2: https://www.irenenorth.com/writings/wp-content/uploads/2018/06/mcdonalds-kowloon-park-IMG_0772.jpg  
