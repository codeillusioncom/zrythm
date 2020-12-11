# This is part of the Zrythm Manual.
# Copyright (C) 2019 Alexandros Theodotou <alex at zrythm dot org>
# See the file index.rst for copying conditions.
#
# ----------------------------------------------------------------------------
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# --- Project information ---

project = 'Zrythm'
copyright = '2019-2020 The Zrythm contributors'
author = 'The Zrythm contributors'

from subprocess import check_output

# The full version, including alpha/beta/rc tags
release = '1.0.0-alpha.6.0.0'
# The short X.Y version
version = release[:-4]

# --- General configuration ---

# If your documentation needs a minimal Sphinx
# version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as
# strings. They can be extensions coming with Sphinx
# (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.imgmath',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    # 'sphinxcontrib.programoutput',
    # 'sphinxcontrib.devhelp',
    # 'recommonmark',
]

# Add any paths that contain templates here,
# relative to this directory.
templates_path = ['_templates']

# Make sure the section target is unique
autosectionlabel_prefix_document = True

# If this is True, todo and todolist produce output,
# else they produce nothing. The default is False.
todo_include_todos = True

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = '@ LANG @'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['README.md', '_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme_path = ['./_themes']
html_theme_path = ['.']
html_theme = 'sphinx_zrythm_theme'
html_last_updated_fmt = ''

def setup(app):
   app.add_css_file ("css/custom.css")
   # app.add_source_suffix('.rst','restructuredtext')

# define some custom roles
rst_prolog = """
.. role:: zbutton
.. role:: red
.. role:: green
.. role:: blue
.. role:: bash(code)
   :language: bash
   :class: highlight
.. role:: scheme(code)
   :language: scheme
   :class: highlight
"""

# Theme options are theme-specific and customize the
# look and feel of a theme further.  For a list of
# options available for each theme, see the
# documentation.
html_theme_options = {
    'canonical_url': 'https://manual.zrythm.org/',
    'logo_only': True,
    'display_version': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = '_static/z.svg'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

dev_version = 'develop'  # This line auto-edited by newrelease script
stable_version = 'master'  # This line auto-edited by newrelease script
release_version = 'latest'  # This line auto-edited by newrelease script

html_context = {
        'current_version': '{0}'.format(release),
        'languages':
                [('af_ZA', 'Afrikaans'),
                 ('ar', 'اَلْعَرَبِيَّةُ‎'),
                 ('de', 'Deutsch'),
                 ('el', 'Ελληνικά'),
                 ('en', 'English'),
                 ('en_GB', 'English UK'),
                 ('es', 'Español'),
                 ('fr', 'Français'),
                 ('gl', 'Galego'),
                 ('it', 'Italiano'),
                 ('ja', '日本語'),
                 ('nb_NO', 'Bokmål'),
                 ('nl', 'Nederlands'),
                 ('pt', "Português"),
                 ('pt_BR', 'Português do Brasil'),
                 ('ru', 'русский'),
                 ('sv', 'Svenska'),
                 ('zh_CN', '简体中文'),
                 ('zh_TW', '繁體中文')],
        'vcs_pageview_mode': 'blob',
        'cgit_host': 'https://git.zrythm.org/cgit',
        'cgit_repo': 'zrythm',
        'downloads':
            [('pdf',
              'https://manual.zrythm.org/en/Zrythm.pdf'),
             ('htmlzip',
              'https://www.zrythm.org'),
             ('epub',
              'https://www.zrythm.org')]}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Zrythmdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': '',

    # Latex figure (float) alignment
    #
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Zrythm.tex', 'Zrythm User Manual',
     'Alexandros Theodotou', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'zrythm', 'Zrythm User Manual',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Zrythm', 'Zrythm User Manual',
     author, 'Zrythm', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Localization ----------------------------------------
locale_dirs = ['locale/']
# TODO after 3.3, set this to 'zrythm-manual' to
# compact all PO files into one
gettext_compact = True


# -- Extension configuration -------------------------------------------------
