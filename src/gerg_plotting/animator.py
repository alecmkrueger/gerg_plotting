from attrs import define,field
from typing import Callable
import io
import os
import datetime
from pathlib import Path
import imageio.v3 as iio
from PIL import Image,ImageFile
import numpy as np
import matplotlib.pyplot as plt

@define
class Animator:
    plotting_function: Callable = field(init=False)
    iterable: np.ndarray|list = field(init=False)
    duration: int|float = field(init=False)
    iteration_param:str = field(init=False)
    frames:list = field(factory=list)
    image_dpi:int = field(default=300)

    gif_filename:Path = field(init=False)
    image_files:list = field(init=False)
    function_kwargs:dict = field(init=False)

    def fig2img(self, fig) -> ImageFile:
        '''Convert a Matplotlib figure to a PIL Image.'''
        buf = io.BytesIO()
        fig.savefig(buf, dpi=self.image_dpi)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def delete_images(self) -> None:
        '''Delete image files from disk.'''
        for file in self.image_files:
            os.remove(file)

    def generate_frames_in_memory(self) -> None:
        '''Generate frames and store them in memory.'''
        for _, iter_value in enumerate(self.iterable):
            fig = self.plotting_function(**{self.iteration_param: iter_value},**self.function_kwargs)
            if fig:
                img = self.fig2img(fig)
                self.frames.append(img)
                plt.close(fig)

    def generate_frames_on_disk(self) -> None:
        '''Generate frames and store them on disk.'''
        num_padding = len(str(len(self.iterable)))
        for idx, iter_value in enumerate(self.iterable):
            image_filename = self.images_path / f"{idx:0{num_padding}}.png"
            fig = self.plotting_function(**{self.iteration_param: iter_value},**self.function_kwargs)
            if fig:
                fig.savefig(image_filename, dpi=self.image_dpi, format='png')
                plt.close(fig)

    def save_gif_from_memory(self) -> None:
        '''Save GIF from frames stored in memory.'''
        self.frames[0].save(
            self.gif_filename,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=self.duration,
            loop=0
        )

    def save_gif_from_disk(self) -> None:
        '''Save GIF from frames stored on disk.'''
        self.image_files = sorted(self.images_path.glob('*.png'))
        with iio.imopen(self.gif_filename, 'w', format="GIF", duration=self.duration) as writer:
            for image_file in self.image_files:
                writer.write(iio.imread(image_file))

    def animate(self,plotting_function,interable,fps,iteration_param,gif_filename:str,**kwargs) -> None:
        '''
        Create and save a gif from the 3D self.plotting_function passed with a camera angle that moves 
        based on a set of elevation and azimuth values.

        Inputs:
        - plotting_function (function): Function to draw 3D figure function must contain kwargs of elev and azim
        - iterable (1D iterable): List of values to iterate over
        - fps (int|float): The number of frames per second
        - gif_filename (str): File location and name to save the gif as

        Outputs:
        A gif saved with the name passed by filename
        '''

        self.plotting_function = plotting_function
        self.iterable = interable
        self.iteration_param = iteration_param
        self.duration = 1000 / fps  # Frame duration in ms
        num_iterations = len(self.iterable)
        self.gif_filename = Path(gif_filename)
        self.function_kwargs = kwargs

        if num_iterations < 100:
            print(f'Saving figures to memory, n_iterations: {num_iterations}')
            self.generate_frames_in_memory()
            self.save_gif_from_memory()
        else:
            print(f'Saving figures to storage, n_iterations: {num_iterations}')
            self.images_path = Path(__file__).parent.joinpath('images')
            self.images_path.mkdir(parents=True, exist_ok=True)
            self.generate_frames_on_disk()
            self.save_gif_from_disk()
            self.delete_images()
