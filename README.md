# Accident_detection_using_object_detection_model_MobilenetSSD

Hardware Setup:
1. Install Raspbian OS Desktop version
2. Install vncserver
3. Install xtightvncviewer
4. Connect all the raspberry pis to same Wi-Fi network
5. Connect the pi camera to csi port
6. Connect the display screens like monitor through HDMI
cable

Installation and execution of the code :-
1. Clone the source code repository to the raspberry pi.
2. Install python 3.5
3. Install tensorflow1.5
4. Install the following python packages with the following
commands -
   ```    
      a. pip install cython
      b. pip install scipy
      c. pip install dataclasses
      d. pip install gin-config
      e. pip install lvis
      f. pip install pycocotools
      g. pip install imutils
      h. pip install opencv-python
      i. pip install pickle

5. Go to the models /research /object_detection /
object_detection_webcame.py
6. Run the Object_detection_webcam python file to start the
accident detection code.

```Note:
      ● This file accesses the webcam or the pi cam (incase of
      our project) and begins the surveillance of the
      surroundings.
      ● When an accident is detected the file automatically
      triggers video transmission code.
      ● Other vehicles in the same network receive the video
      through socket programming.
      
```
For live video broadcast
1. Sender captures the video and sends it to the cacheServer
2. The cacheServer stores the video and sends it to the other clients(Vehicles in this application)
