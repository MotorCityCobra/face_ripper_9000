# face_ripper_9000
Creates 256 cropped, high quality facesets from a batch of mp4 videos end to end. 
Modified code from https://github.com/Tyrannosaurus1234/GetFaces by Tyrannosaurus1234 adjusted for batch converting and
extra quality scanning of the final faceset by removing photos below a minimum size and double checking there is only one
face in the photo

# Usage

    $python3 demo.py -i '/PATH/TO/PASSPORT/STYLE/PHOTO/OF/TARGET/FACE.jpg' -v '/PATH/TO/DIR/OF/MP4s'

-t = Tolerance of face detection, lower is stricter (0.1-1.0) Default= 0.6
-f = Amount of frames per second to extract. Default = 25
-n = Number of frames with target face to save from each video. Default=500
-s = Minimum KB size of images to keep in the faceset. Default = 32

# Dependancies
numpy

opencv-python >= 3.31

face_recognition

face_recognition requires a package called dlib. If you have a GPU you must install dlib in a specific way in order to get it to use your GPU ...Which doesn't seem to be listed in the documentation but doing so is as follows,

git clone https://github.com/davisking/dlib.git

cd dlib

mkdir build; cd build; cmake .. -DDLIB_USE_CUDA=0 -DUSE_AVX_INSTRUCTIONS=1; cmake --build .

cd ..

python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA
