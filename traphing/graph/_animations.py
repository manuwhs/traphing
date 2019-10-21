import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio
import cv2
import os
import numpy as np

def fig_to_frame(fig, figsize):
        # Used to return the plot as an image rray
        fig.set_size_inches( figsize )
        fig.canvas.draw()       # draw the canvas, cache the renderer
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        
        image_shape = fig.canvas.get_width_height()[::-1] + (3,)
        image_shape = list(image_shape)
        
        image_shape[0] = image_shape[0]*2; image_shape[1] = image_shape[1]*2
        
        image  = image.reshape(image_shape)
        return image

def compute_frames_list(plot_func, n_frames, figsize):
    frames_list = []
    for i in range(n_frames):
        print ("\r Creating image %i/%i"%(i+1,n_frames), end = "")
        fig = plot_func(i) 
        image = fig_to_frame(fig, figsize)
        frames_list.append(image)
    
    return frames_list


##############################################################################################
def make_gif(self, plot_func, filepath = './powers.gif', n_frames = 200, 
                   fps = 1.0, quantizer = "nq", figsize = [12,8]):
    # Data for plotting
    frames_list = compute_frames_list(plot_func, n_frames, figsize)
    imageio.mimsave(filepath, frames_list, fps=fps)

def make_video(self, plot_func, filepath = './powers.avi', n_frames = 200, 
               fps = 1.0, quantizer = "nq", figsize = [12,8]):
    
    fourcc = fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    
    frames_list = compute_frames_list(plot_func, n_frames, figsize)
    width,height,d = frames_list[0].shape
    out = cv2.VideoWriter(filepath,fourcc , fps, (width,height))
    
    for i in range(n_frames):
        out.write(frames_list[i]) # Write out frame to video
        
    out.release()