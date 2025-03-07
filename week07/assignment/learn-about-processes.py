import multiprocessing as mp
import timeit

import numpy as np
from matplotlib.pylab import plt  # load plot library
from PIL import Image

# number of CPUs on your computer
CPU_COUNT = mp.cpu_count()

# TODO Your final video needs to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 20

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions you need here


        
def proccess_frames(frame: int):
    image_file = rf'elephant/image{frame:03d}.png'
    green_file = rf'green/image{frame:03d}.png'
    process_file = rf'processed/image{frame:03d}.png'
    create_new_frame(image_file, green_file, process_file)
   


if __name__ == '__main__':
    beginTime = timeit.default_timer()

    # TODO - the code currently is set to only process the 10th frame.()
    # Modify the code to process all 300 frames using a process pool and map.


    images = []
    # for image_number in range(1, FRAME_COUNT + 1 ):
    #     image_file = rf'elephant/image{image_number:03d}.png'
    #     green_file = rf'green/image{image_number:03d}.png'
    #     process_file = rf'processed/image{image_number:03d}.png'
        # images.append(image_file)
        # images.append(green_file)
        # images.append(process_file)
        # create_new_frame(image_file, green_file, process_file)

    with mp.Pool(mp.cpu_count()) as p:
        p.map(proccess_frames, list(range(1, 301)))
        # p = mp.Pool(300)



  
    image_number = 10








    # what i started with, so i can ask ai to help explain and give me sample problems to know how i got from where i started to where i ended up


    # with mp.Pool(mp.cpu_count()) as p:
    #     outputs = p.map(create_new_frame, input)
    #     p = mp.Pool(300)



    # for image_number in range(1, 301):
    #     image_file = rf'elephant/image{image_number:03d}.png'
    #     green_file = rf'green/image{image_number:03d}.png'
    #     process_file = rf'processed/image{image_number:03d}.png'
    #     create_new_frame(image_file, green_file, process_file)

    # image_number = 10

   

   
    
    print(f'\nTime To process all images = {timeit.default_timer() - beginTime} sec')
