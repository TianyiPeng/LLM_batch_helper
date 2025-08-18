# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../llm_batch_helper'))

# -- Project information -----------------------------------------------------
project = 'LLM Batch Helper'
copyright = '2024, Tianyi Peng'
author = 'Tianyi Peng'
release = '0.1.5'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# MyST settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]