# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../notebooks'))


# -- Project information -----------------------------------------------------

project = '深層学習チュートリアル'
author = '人工知能画像診断学共同研究講座'
copyright = '2020, ' + author
version = '0.0.6'
release = version
editors = ['Yuki Suzuki']


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxcontrib.katex',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ja'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',  '**.ipynb_checkpoints']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_title = project
html_logo = 'images/logo.svg'
html_favicon = 'images/logo.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/alerts.css',
]

latex_show_urls = 'footnote'
latex_show_pagerefs = True
latex_logo = 'images/logo.pdf'

latex_preamble = r'''
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{2}

\authoraddress{
  大阪大学医学系研究科
}
'''

latex_bg = r'''
\usepackage{transparent}
\usepackage{eso-pic}
\newcommand\BackgroundPic{
  \put(0,0){
    \parbox[b][\paperheight]{\paperwidth}{
      \vfill
      \hspace{.1\paperwidth}
      \scalebox{-1}[1]{
           \includegraphics[width=.5\paperwidth,height=.5\paperheight,
             keepaspectratio]{logo.pdf}
           }
          \vspace{.2\paperheight}
    }
  }
}
'''

latex_title = r'''
\begin{titlepage}
  \noindent\rule{\textwidth}{1pt}\par
      \begingroup % for PDF information dictionary
       \def\endgraf{ }\def\and{\& }%
       \pdfstringdefDisableCommands{\def\\{, }}% overwrite hyperref setup
       \hypersetup{pdfauthor={$author}, pdftitle={$title}}%
      \endgroup
  \begin{flushright}
    {\Huge $title \par}
    {\itshape\LARGE Ver. $release \par}
    {\LARGE
      \begin{tabular}[t]{c}
        $author
      \end{tabular}\kern-\tabcolsep
      \par}
    {\large
      $editors
    }
    \vfill
        {\large
          $date \par
        }%

  \end{flushright}
  \AddToShipoutPicture*{\BackgroundPic}
\end{titlepage}
\setcounter{footnote}{0}%
\clearpage
'''

from datetime import datetime
date = datetime.today().strftime("%Y/%m/%d")
import string
latex_title = string.Template(latex_title).substitute(title=project,release=release,author=author,editors=', '.join(editors),date=date)

latex_elements = {
  'papersize': 'a4paper',
  'extraclassoptions': 'openany,oneside', # remove empty pages
  'releasename': 'Ver.',
  'preamble': latex_preamble + latex_bg,
  'maketitle': latex_title,
}


