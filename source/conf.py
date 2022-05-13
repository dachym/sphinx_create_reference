# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or submodules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'sphinx_reference_example'
copyright = '2022, dachym'
author = 'dachym'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

special_extensions = ["nbsphinx", "sphinx_gallery.load_style"]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    # 'sphinx.ext.mathjax',
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx_rtd_theme",
    # Don't use autosectionlabel since many document may have the same section name
    # use explicit anchors when needed
    "sphinx.ext.autosectionlabel",
    # "numpydoc",
]
extensions += ["class_mapper"]
extensions += special_extensions

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}


# Still here to, maybe, integrate it after completing code
# def which_member_to_skip(app, what, name, obj, skip, option):
#     """
#     As 'private-members' does not seem to work with autosummary, this is a workaround
#     to remove private members.
#     """
#     print("Check this name: ", what, name, skip)
#     return skip


# -- Options for autosummary extension ---------------------------------------

autosummary_generate = True
autosummary_imported_members = True
# If __all__ is defined document what is in __all__ and nothing else.
# If imported modules are in __all__ they are documented, whatever
# autosummary_imported_members.
autosummary_ignore_module_all = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_css_file("basic.css")
