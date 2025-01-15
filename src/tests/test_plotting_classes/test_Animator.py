from gerg_plotting.plotting_classes.animator import Animator

import unittest
import pytest
from pathlib import Path
import matplotlib.pyplot as plt
import shutil
from PIL import Image


def simple_plot(x, y, **kwargs):
    """
    A simple plotting function for testing.
    """
    fig, ax = plt.subplots()
    ax.plot(x, y, **kwargs)
    return fig

def simple_plot_without_fig(x, y, **kwargs):
    """
    A simple plotting function for testing but the figure is not returned.
    """
    fig, ax = plt.subplots()
    ax.plot(x, y, **kwargs)

class TestAnimator(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = Path("test_images")
        self.test_dir.mkdir(exist_ok=True)
        self.gif_path = self.test_dir / "test_animation.gif"
        self.animator = Animator()

    def tearDown(self):
        """Clean up after tests."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_restructure_params(self):
        """Test _restructure_params correctly reshapes parameter dictionary."""
        param_dict = {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
        expected = [{"x": 1, "y": 4}, {"x": 2, "y": 5}, {"x": 3, "y": 6}]
        result = self.animator._restructure_params(param_dict)
        self.assertEqual(result, expected)
        self.assertEqual(self.animator.num_iterations, 3)

    def test_restructure_params_with_mismatch(self):
        """Test _restructure_params correctly reshapes parameter dictionary."""
        param_dict = {
            "x": [1, 2, 3],
            "y": [4, 5],
        }
        expected = [{"x": 1, "y": 4}, {"x": 2, "y": 5}, {"x": 3, "y": 6}]
        with self.assertRaises(ValueError):
            result = self.animator._restructure_params(param_dict)

    def test_fig2img(self):
        """Test _fig2img converts Matplotlib figures to PIL images."""
        fig = simple_plot([0, 1], [1, 0])
        img = self.animator._fig2img(fig)
        self.assertIsInstance(img, Image.Image)
        plt.close(fig)

    def test_generate_frames_in_memory(self):
        """Test _generate_frames_in_memory stores frames as PIL images."""
        param_dict = {"x": [[0, 1]], "y": [[1, 0]]}
        self.animator.animate(
            plotting_function=simple_plot,
            param_dict=param_dict,
            gif_filename=str(self.gif_path),
        )
        self.assertGreater(len(self.animator.frames), 0)
        self.assertIsInstance(self.animator.frames[0], Image.Image)

        # Test if the user failed to pass the figure
        with self.assertRaises(ValueError):
            self.animator.animate(
                plotting_function=simple_plot_without_fig,
                param_dict=param_dict,
                gif_filename=str(self.gif_path),
            )
        

    @pytest.mark.slow
    def test_generate_frames_on_disk(self):
        """Test _generate_frames_on_disk saves images to disk."""
        param_dict = {"x": [[0, 1]] * 101, "y": [[1, 0]] * 101}
        # Assign the provided arguments to the corresponding attributes
        self.animator.plotting_function = simple_plot
        self.animator.param_list = self.animator._restructure_params(param_dict=param_dict)
        self.animator.duration = 1000 / 24  # Calculate frame duration in milliseconds
        self.animator.gif_filename = Path(str(self.gif_path))
        self.animator.function_kwargs = {'color':'r'}
        self.animator.images_path = Path(self.test_dir)
        self.animator._generate_frames_on_disk()
        self.animator._save_gif_from_disk()
        self.assertTrue(self.gif_path.exists())
        self.assertTrue(any(self.test_dir.glob("*.png")))

        # Test if the user failed to pass the figure
        self.animator.plotting_function = simple_plot_without_fig
        with self.assertRaises(ValueError):
            self.animator._generate_frames_on_disk()

    def test_save_gif_from_memory(self):
        """Test _save_gif_from_memory creates a GIF from in-memory frames."""
        param_dict = {"x": [[0, 1]], "y": [[1, 0]]}
        self.animator.animate(
            plotting_function=simple_plot,
            param_dict=param_dict,
            gif_filename=str(self.gif_path),
        )
        self.assertTrue(self.gif_path.exists())

    @pytest.mark.slow
    def test_save_gif_from_disk(self):
        """Test _save_gif_from_disk creates a GIF from disk-stored frames."""
        param_dict = {"x": [[0, 1]] * 101, "y": [[1, 0]] * 101}
        self.animator.animate(
            plotting_function=simple_plot,
            param_dict=param_dict,
            gif_filename=str(self.gif_path),
        )
        self.assertTrue(self.gif_path.exists())

    def test_delete_images(self):
        """Test _delete_images removes temporary image files."""
        # Create some test files to remove
        files = [f'{self.test_dir}/{idx}.png' for idx in range(5)]
        create_files = [Path(file).touch() for file in files]
        self.animator.image_files = files
        self.animator._delete_images()
        self.assertFalse(any(self.test_dir.glob("*.png")))

