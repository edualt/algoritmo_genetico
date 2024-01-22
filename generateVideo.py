import glob
file_list = sorted(glob.glob('./images/*.png'))
import moviepy.editor as mpy
fps = 10
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_videofile('movie.avi', codec = 'libx264')
import cv2
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.avi', fourcc, 1, (640, 480))

for j in range(1, 100):
    img = cv2.imread("./images/generation " + str(j) + '.png')
    video.write(img)

cv2.destroyAllWindows()
video.release()