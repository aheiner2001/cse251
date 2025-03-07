'''
Requirements
1. Finish the team06 assignment (if necessary).
2. Change your program to process all 300 images using 1 CPU, then 2 CPUs, all the way up to the
   number of CPUs on your computer plus 4.
3. Keep track of the time it takes to process all 300 images per CPU.
4. Plot the time to process vs the number of CPUs.
5. COMMENT every line that you write yourself.
   
Questions:
1. What is the relationship between the time to process versus the number of CPUs?
   Does there appear to be an asymptote? If so, what do you think the asymptote is?
   >
   >
2. Is this a CPU bound or IO bound problem? Why?
   >
   >
3. Would threads work on this assignment? Why or why not? (guess if you need to) 
   >
   >
4. When you run "create_final_video.py", does it produce a video with the elephants
   inside of the screen?
   >
'''

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp
from cse251functions import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
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
def process_frames(frame: int):
    image_file = rf'elephant/image{frame:03d}.png'
    green_file = rf'green/image{frame:03d}.png'
    process_file = rf'processed/image{frame:03d}.png'
    create_new_frame(image_file, green_file, process_file)

if __name__ == '__main__':
    all_process_time = timeit.default_timer()

    xaxis_cpus = []
    yaxis_times = []

    for cpu_count in range(1, CPU_COUNT + 1):
        start_time = timeit.default_timer()
        
        with mp.Pool(cpu_count) as p:
            p.map(process_frames, list(range(1, FRAME_COUNT + 1)))
        
        elapsed_time = timeit.default_timer() - start_time
        xaxis_cpus.append(cpu_count)
        yaxis_times.append(elapsed_time)
        
        print(f'Time to process with {cpu_count} CPUs: {elapsed_time}')

    print(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    plt.title('CPU Core Times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()

    create_signature_file("CSE251W25")
