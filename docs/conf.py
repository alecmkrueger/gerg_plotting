# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(0, os.path.abspath(".."))

project = 'gerg_plotting'
copyright = '2025, Alec Krueger'
author = 'Alec Krueger'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "matplotlib.sphinxext.plot_directive",
    'sphinx_gallery.gen_gallery',
    'autoapi.extension',
]

# Execute the setup function during build
def setup(app):
    """Download all required data before building docs."""
    from gerg_plotting.data_classes.bathy import Bathy
    from gerg_plotting.download_example_data import download_example_data
    
    # Download seafloor data
    bathy = Bathy(bounds=None)
    # Download example data
    download_example_data()
    return app

# Configure nbsphinx to execute notebooks during build
nbsphinx_execute = 'always'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','sg_execution_times.rst']


# -- Examples gallery settings ---------------------------------------------------------

sphinx_gallery_conf = {
    'examples_dirs': 'examples',
    'gallery_dirs': 'auto_examples',
    'image_scrapers': ('matplotlib',),
    'remove_config_comments': True,
    'example_extensions': {'.py'}
}

# -- AutoAPI settings -------------------------------------------------------
autoapi_dirs = ['../src/gerg_plotting']
autoapi_template_dir = '_templates'
autoapi_output_dir = '_build/autoapi'

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "imported-members"
]

autodoc_default_options = {'inherited-members': True}

autodoc_typehints = "signature"

autoapi_member_order = 'alphabetical'

autoapi_keep_files = True

# Parse docstrings using the NumPy format
napoleon_numpy_docstring = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
# html_static_path = ['_static']
