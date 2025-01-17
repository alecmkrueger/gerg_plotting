# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'gerg_plotting'
copyright = '2025, Alec Krueger'
author = 'Alec Krueger'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = [
#     'matplotlib.sphinxext.plot_directive',
#     'sphinx_gallery.gen_gallery',
#     'autoapi.extension',
# ]

extensions = [
    'sphinx_gallery.gen_gallery',
    'autoapi.extension',
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','sg_execution_times.rst']

# -- Plot settings -----------------------------------------------------------
from sphinx.builders.html import StandaloneHTMLBuilder
StandaloneHTMLBuilder.supported_image_types = [
    'image/svg+xml',
    'image/gif',
    'image/png',
    'image/jpeg'
]
plot_include_source = True
plot_html_show_source_link = True
plot_formats = ['png','gif']

# -- Examples gallery settings ---------------------------------------------------------

# sphinx_gallery_conf = {
#     'examples_dirs': '../examples',
#     'gallery_dirs': 'auto_examples',
#     'image_scrapers': ('matplotlib',),
#     'remove_config_comments': True,
#     'example_extensions': {'.py'}
# }

sphinx_gallery_conf = {
    'examples_dirs': 'examples',         # Directory with example scripts
    'gallery_dirs': 'auto_examples',    # Where the gallery output will go
    'image_scrapers': (),               # Disable plot generation during the build
    'reset_modules_order': 'after',     # Reset modules after script execution
    'plot_gallery': 'False'
}

# -- AutoAPI settings -------------------------------------------------------
autoapi_dirs = ['../src/gerg_plotting']
autoapi_template_dir = '_templates'

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
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
