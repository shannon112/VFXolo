Related Software:
```
Blender (Win64_2.6.2 -> Win64_2.79b)
Voodoo (Win32_1.2.0)
iMovie (Mac_10.1.11)
```

# Blender
## 1.Selecting
```
select all = double press 'a'
select object = click that object on the right panel so that you could select all parts of that object
ref: https://www.youtube.com/watch?v=guLSfezNjZw
```

## 2.View control
- setting
```
File -> User preference -> Interface -> select "Zoom to Mouse Position"
File -> User preference -> Interface -> select "Rotate Around Selection"
File -> User preference -> Input -> select "Emulate 3 Button Mouse"
Save as default
```
- three button control view
```
zoom in/out: scroll mouse middle wheel to zoom in/out at mouse position
rotate: select object and click middle wheel to rotate around object
padding: hold shift and click middle wheel to pad
```
- two button control view
```
zoom in/out: ctrl + alt + left mouse to zoom in/out at mouse position
rotate: select object and alt+left mouse to rotate around object
padding: hold shift+alt and left mouse to pad
```
ref: https://www.youtube.com/watch?v=RNBYuYRFQe0

# 3.resume to default setting
```
file -> load factory setting
file -> sava as user default
```

# 4. 3D model
- import 3D model
```
model要先load進來看看顏色對不對能不能用 (press F12 or select "render camera"
remember to turn on the light (use add -> lamp)
```
- create a plane with texture
```
create a plane 
https://blender.stackexchange.com/questions/7465/create-a-flat-plane-with-beveled-edges
editing texture
https://www.youtube.com/watch?v=il7ajiCepus
```
- using texture with transparency property(.png)
```
-> On Material Tab, go to Transparency Section, activate leaves' Material transparency
-> set it's transparency mode to "Z Transparency"
-> then set the Alpha value to 0.
-> On Texture Tab, go to Influence Section, tick Alpha and set it's value to 1. 
-> Don't forget to tick Use Alpha on Image Section.
ref: https://blender.stackexchange.com/questions/78917/how-to-render-transparent-textures-in-blender-render
```
