# Dinosaur Face
###### An image recognition to play Chrome Dinosaur game with the face

___

#### Installation

```shell
$ git clone https://github.com/Lucisu/DinosaurFace.git
$ cd DinosaurFace
$ pip3 install -r requirements.txt
```

###### Don't forget: You need install CMake before install Dlib

#### Execute

Open Chrome, with the game, and:
```shell
$ python3 main.py
```

##### Note

###### When the script starts, it will try to find the dinosaur. If finded, the frame with your webcam video will be displayed, and you need click on Chrome window to focus.

#### How does it work

First, script try to find the dinosaur, to prevent launching keys in the wrong place.

After that, using [`shape_predictor_68_face_landmarks.dat`](https://github.com/AKSHAYUBHAT/TensorFace/tree/master/openface/models/dlib) and [OpenCV](https://opencv.org/), we can track some face points.

The main points are in the sides and in the nose. Based on difference between nose height and sides of the face, generate the key press.

Lift your nose to jump, lower it to lower the dinosaur.

It's very simple, but cool :)
