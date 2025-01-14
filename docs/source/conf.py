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

extensions = [
    'autoapi.extension',
]

# -- AutoAPI settings -------------------------------------------------------
autoapi_dirs = ['../../src/gerg_plotting','../../src/examples']
autoapi_template_dir = '../_templates'

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

autodoc_default_options = {'inherited-members': True}

autodoc_typehints = "signature"

autoapi_member_order = 'alphabetical'


# Parse docstrings using the NumPy format
napoleon_numpy_docstring = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'

