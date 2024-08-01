from attrs import define,field
import numpy as np
import io
import imageio
from PIL import Image
import datetime
from gerg_plotting.utils import print_time
from pathlib import Path
import os
import matplotlib.pyplot as plt

@define
class Animator:
    iterable:np.ndarray|list
    plotting_function:function

    def fig2img(self,fig):
        # Convert a Matplotlib figure to a PIL Image and return it
        buf = io.BytesIO()
        fig.savefig(buf,dpi=300)
        buf.seek(0)
        img = Image.open(buf)
        return img
    
    def delete_images(images):
        for file in images:
            os.remove(file)

    def animate(self,filename,duration=200):
        '''
        Create and save a gif from the 3-d self.plotting_function passed with a camera angle that moves based on a set of elevation and azimuth values

        Inputs:
        self.plotting_function (function): function to draw 3d figure function must contain kwargs of elev and azim
        self.iterable (1-d iterable): list of values to iterate over
        filename (str): file location and name to save the gif as and to
        duration (int): duration of each frame in milliseconds (default 200ms)
        
        Outputs:
        A gif saved with the name passed by filename

        Example:
        make_gif(self.plotting_function,self.iterable=[1,2,3,4,5,6,7],
                filename='test.gif',duration=1000)
        '''
        start = str(datetime.datetime.today())[11:22]

        # Check the length of self.iterable
        num_iterations = len(self.iterable)

        if num_iterations<200:
            print(f'Saving figures to memory, n_iterations:{num_iterations}')
            list_gif = []
            #check interators length
            for idx,iter in enumerate(self.iterable):
                print_time(idx)
                #create figure from plotting function
                fig = self.plotting_function(iter=iter)
                if fig is None:
                    continue
                #create image from figure to image function
                img = self.fig2img(fig)
                #append the images to store them
                list_gif.append(img)
                # clean up
                plt.close(fig)
            #save the images as a gif
            list_gif[0].save(filename,save_all=True, 
                            append_images=list_gif[1:],optimize=True,
                            duration=duration,loop=0)
        else:
            print(f'Saving figures to storage, n_iterations:{num_iterations}')
            num_padding = len(str(num_iterations))
            for idx,iter in enumerate(self.iterable):
                # Track
                print_time(idx)
                image_filename = f"{idx:0{num_padding}}.png"
                # Generate figure
                fig = self.plotting_function(iter=iter)
                if fig is None:
                    continue
                fig.savefig(f'Plots/images/{image_filename}',dpi=300,format='png')
                plt.close(fig)
            # Create gif
            images_path = Path(__file__).parent.joinpath('images')
            image_files = images_path.rglob('*.png')
            # Create GIF writer object
            with imageio.get_writer(filename, mode='I', duration=duration) as writer:
                for image_file in image_files:
                    # Append each image to the GIF
                    writer.append_data(imageio.imread(image_file))
                
            # Clean up
            self.delete_images(images=image_files)
        end = str(datetime.datetime.today())[11:22]
        return('Done: {0}-{1}'.format(start,end))