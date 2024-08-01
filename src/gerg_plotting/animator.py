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
    iterable: np.ndarray|list
    plotting_function: Callable
    fps: int
    iteration_param:str
    frames:list = field(factory=list)

    def fig2img(self, fig) -> ImageFile:
        '''Convert a Matplotlib figure to a PIL Image.'''
        buf = io.BytesIO()
        fig.savefig(buf, dpi=300)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def delete_images(self, images: list[Path]) -> None:
        '''Delete image files from disk.'''
        for file in images:
            os.remove(file)

    def generate_frames_in_memory(self) -> None:
        '''Generate frames and store them in memory.'''
        for idx, iter_value in enumerate(self.iterable):
            fig = self.plotting_function(**{self.iteration_param: iter_value})
            if fig:
                img = self.fig2img(fig)
                self.frames.append(img)
                plt.close(fig)

    def generate_frames_on_disk(self, images_path: Path) -> None:
        '''Generate frames and store them on disk.'''
        num_padding = len(str(len(self.iterable)))
        for idx, iter_value in enumerate(self.iterable):
            image_filename = images_path / f"{idx:0{num_padding}}.png"
            fig = self.plotting_function(**{self.iteration_param: iter_value})
            if fig:
                fig.savefig(image_filename, dpi=300, format='png')
                plt.close(fig)

    def save_gif_from_memory(self, filename: str, duration: int) -> None:
        '''Save GIF from frames stored in memory.'''
        self.frames[0].save(
            filename,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=duration,
            loop=0
        )

    def save_gif_from_disk(self, images_path: Path, filename: str, duration: int) -> None:
        '''Save GIF from frames stored on disk.'''
        image_files = sorted(images_path.glob('*.png'))
        with iio.imopen(filename, 'w', format="GIF", duration=duration) as writer:
            for image_file in image_files:
                writer.write(iio.imread(image_file))

    def animate(self, filename: str) -> None:
        '''
        Create and save a gif from the 3D self.plotting_function passed with a camera angle that moves 
        based on a set of elevation and azimuth values.

        Inputs:
        - self.plotting_function (function): Function to draw 3D figure function must contain kwargs of elev and azim
        - self.iterable (1D iterable): List of values to iterate over
        - filename (str): File location and name to save the gif as

        Outputs:
        A gif saved with the name passed by filename
        '''
        duration = 1000 / self.fps  # Frame duration in ms
        num_iterations = len(self.iterable)

        if num_iterations < 200:
            print(f'Saving figures to memory, n_iterations: {num_iterations}')
            self.generate_frames_in_memory()
            print(self.frames)
            self.save_gif_from_memory(filename, duration)
        else:
            print(f'Saving figures to storage, n_iterations: {num_iterations}')
            images_path = Path(__file__).parent / 'images'
            images_path.mkdir(parents=True, exist_ok=True)
            self.generate_frames_on_disk(images_path)
            self.save_gif_from_disk(images_path, filename, duration)
            self.delete_images(images_path.glob('*.png'))
