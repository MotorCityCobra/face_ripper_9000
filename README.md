# face_ripper_9000
Creates 256 cropped, high quality facesets from a batch of mp4 videos end to end. 
Modified code from https://github.com/Tyrannosaurus1234/GetFaces by Tyrannosaurus1234 adjusted for batch converting and
extra quality scanning of the final faceset by removing photos below a minimum size and double checking there is only one
face in the photo

# Usage

    $python3 demo.py -i '/PATH/TO/PASSPORT/STYLE/PHOTO/OF/TARGET/FACE.jpg' -v '/PATH/TO/DIR/OF/MP4s'

    -t = Tolerance of face detection, lower is stricter (0.1-1.0) Default= 0.6
    -f = Amount of frames per second to scan. Default = 25
    -n = Number photos of the face from each video. Default=500 (Set higher if you have less vids)
    -s = Minimum KB size of images to keep in the faceset. Default = 32

Running the script creates three files in your directory. One for the faceset. One for the scanned mp4s. One for the small faces.

The batch processing of the faceset can be stopped or started anytime without a problem, aside from maybe it creating
duplicates if it stops in the middle of a video. Just go in your faceset folder and remove photos from the half processed
video when you start it again.

The script can read videos other than mp4s. Just do a find and replace in the script to your extension, like mp4 to mkv.  
Best to use mp4s ripped from YouTube. Use YouTube video downloader sites or apps to grab dozen(s) of 1080p videos starring
the target face.

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



# Donations Accepted and Appreciated
BTC: 18vFPf3mKBEk8m2xvR21Vw3B8GNUrmYsoe  
ETH: 0x5E9c5fC0Ba54e7fe7da675AF73fF65A047aB3309  
LTC: LS2QoBuAQm6PXrKJgjYeVijK4c8pj1CXjS  
Monero: 44GW7eCnwcMbgaEaqwtzt5WgWiVH3U6p5FtK1Rg8b65fj6A5AHqeyF6ad9a2owQGPCZFStskLsmbcULiYUBcCAAUKX177FF
