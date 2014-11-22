def main():
    # this program is coded in Python v. 2.7
    from __future__ import print_function
    from PIL import Image
    import argparse
    from time import sleep

    print('ImageSampler')
    # command-line argument parser
    parser = argparse.ArgumentParser(
            prog = 'ImageSampler',
            prefix_chars = '-/',
            description = """This program assigns settings to a list of bulbs (list is currently coded into the .py file).""")
    parser.add_argument('-f', '--filename', help='Filename for temporary image storage', type=str, default='image.png')
    parser.add_argument('-d', '--delay', help='Delay before sampling (seconds)', type=float, default=0)
    args = parser.parse_args()

    sleep(args.delay)


    from cv2 import *
    # initialize the camera
    cam = VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
        imshow("cam-test",img)
        waitKey(0)
        destroyWindow("cam-test")
        imwrite("filename.jpg",img) #save image

    from SimpleCV import Image, Camera
    
    cam = Camera()
    img = cam.getImage()
    img.save("filename.jpg")
    
    # debug
#    import pdb
#    pdb.set_trace()
    # debug

from PIL import Image
 
def average_image_color(filename):
	i = Image.open(filename)
	h = i.histogram()
 
	# split into red, green, blue
	r = h[0:256]
	g = h[256:256*2]
	b = h[256*2: 256*3]
 
	# perform the weighted average of each channel:
	# the *index* is the channel value, and the *value* is its weight
	return (
		sum( i*w for i, w in enumerate(r) ) / sum(r),
		sum( i*w for i, w in enumerate(g) ) / sum(g),
		sum( i*w for i, w in enumerate(b) ) / sum(b)
	)
 
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print average_image_color(sys.argv[1])
    else:
        print 'usage: average_image_color.py FILENAME'
        print 'prints the average color of the image as (R,G,B) where R,G,B are between 0 and 255.'



if __name__ == '__main__':
    main()
