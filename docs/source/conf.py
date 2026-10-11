# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Import Python modules ---------------------------------------------------
import datetime
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = tomllib.loads(
    (ROOT / "pyproject.toml").read_text(encoding="utf-8")
)["project"]

# autodoc needs the package importable without an install step.
sys.path.insert(0, str(ROOT / "src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = PROJECT["name"]
author = PROJECT["authors"][0]["name"]
copyright = f"{datetime.datetime.now().year}, {author}"
release = PROJECT["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_prompt",
    "sphinxcontrib.jquery",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinx_design",
    "sphinxcontrib.asciinema",
]
source_suffix = [".rst"]

exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

language = "en_US"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["../static"]
html_css_files = [
    # Save the table width
    # override wide tables in RTD theme
    # https://rackerlabs.github.io/docs-rackspace/tools/rtd-tables.html
    "css/theme_overrides.css",
    # Tweak styles of the sphinx_inline_tabs extension
    "css/codeblock_tab.css",
]

# Show a deeper toctree in the sidebar
# https://stackoverflow.com/questions/27669376/show-entire-toctree-in-read-the-docs-sidebar
html_theme_options = {
    "navigation_depth": 6,
}

# -- Options for sphinx-intl -------------------------------------------------
# po files will be created in this directory
# path is example but recommended.
locale_dirs = ["locales"]
gettext_compact = False  # optional

# -- Options for sphinx.ext.autodoc -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = "bysource"
autodoc_inherit_docstrings = False  # so overridden methods won't pop up
add_module_names = False

# -- Options for sphinx.ext.autosectionlabel -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_prefix_document = True

# -- Options for sphinx.ext.intersphinx -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
# disable all auto external document references
# implicit ref for general std domain is bad
intersphinx_disabled_reftypes = ["std:*"]
intersphinx_timeout = 30
