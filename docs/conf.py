# flake8: noqa: I100

# -*- coding: utf-8 -*-
#
# trakt.py documentation build configuration file, created by
# sphinx-quickstart on Sun Sep 20 14:07:31 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import inspect
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

INTERFACES_DIR = os.path.join(ROOT_DIR, 'trakt', 'interfaces')
OBJECTS_DIR = os.path.join(ROOT_DIR, 'trakt', 'objects')

MODULE_TYPE_ORDER = [
    'interfaces',
    'objects',
    'modules'
]

IGNORED_INTERFACE_MEMBERS = [
    'http',
    'path',

    'get_data'
]

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, BASE_DIR)

from trakt.interfaces.base import Interface


def refresh_autodoc_index():
    def find_autodoc_modules(module_name, sourcedir):
        """Return a list of modules in the SOURCE directory."""
        result = []

        os.chdir(os.path.join(sourcedir, module_name))

        print('SEARCHING %s' % sourcedir)

        for root, dirs, files in os.walk('.'):
            for filename in files:
                if not filename.endswith('.py'):
                    continue

                # remove the pieces of the root
                elements = root.split(os.path.sep)

                # replace the leading '.' with the module name
                elements[0] = module_name

                # and get the base module name
                base, extension = os.path.splitext(filename)

                if not (base == '__init__'):
                    elements.append(base)

                result.append('.'.join(elements))

        result.sort()

        return result

    RSTDIR = os.path.abspath(os.path.join(BASE_DIR, 'sourcecode'))
    SRCS = {'trakt': ROOT_DIR}

    EXCLUDED_MODULES = ('trakt.tests',)
    CURRENT_SOURCES = {}

    if not(os.path.exists(RSTDIR)):
        os.mkdir(RSTDIR)

    CURRENT_SOURCES[RSTDIR] = [
        'interfaces.rst',
        'modules.rst',
        'objects.rst'
    ]

    # Open index files
    def open_index(filename, name):
        path = os.path.join(RSTDIR, filename)

        fp = open(path, 'w')
        fp.write('=================\n')
        fp.write('%s\n' % name)
        fp.write('=================\n')
        return fp

    fp_indices = {
        'interfaces': open_index('interfaces.rst', 'Interfaces'),
        'objects': open_index('objects.rst', 'Objects'),

        'modules': open_index('modules.rst', 'Modules')
    }

    # Generate documentation for modules
    for base, path in SRCS.items():
        sys.stdout.write('Generating source documentation for %s\n' % base)

        MOD_DIR = os.path.join(RSTDIR, base)
        CURRENT_SOURCES[MOD_DIR] = []

        if not(os.path.exists(MOD_DIR)):
            os.mkdir(MOD_DIR)

        modules = {}

        for module_name in find_autodoc_modules(base, path):
            if any([module_name.startswith(exclude)
                    for exclude
                    in EXCLUDED_MODULES]):
                print('EXCLUDED: %s' % module_name)
                continue

            mod_path = os.path.join(path, *module_name.split('.'))
            generated_path = os.path.join(MOD_DIR, '%s.rst' % module_name)

            # Find the __init__.py module if this is a directory
            if os.path.isdir(mod_path):
                source_path = '.'.join((os.path.join(mod_path, '__init__'), 'py',))
            else:
                source_path = '.'.join((os.path.join(mod_path), 'py'))

            CURRENT_SOURCES[MOD_DIR].append('%s.rst' % module_name)

            # Refresh autodoc file
            module_type = refresh_autodoc(source_path, generated_path, module_name)

            if not module_type:
                print('IGNORED: %s' % module_name)
                continue

            # Append module to the `modules` dictionary
            if module_type not in modules:
                modules[module_type] = []

            modules[module_type].append('%s/%s' % (base, module_name))

        # Write modules to index
        for module_type in MODULE_TYPE_ORDER:
            if module_type not in modules:
                continue

            fp_index = fp_indices[module_type]
            fp_index.write('.. toctree::\n')
            fp_index.write('   :maxdepth: 1\n')
            fp_index.write('\n')

            for name in modules[module_type]:
                fp_index.write('   %s\n' % name)

    for fp in fp_indices.values():
        fp.close()

    # Delete auto-generated .rst files for sources which no longer exist
    for directory, subdirs, files in list(os.walk(RSTDIR)):
        for old_file in files:
            if old_file not in CURRENT_SOURCES.get(directory, []):
                print('Removing outdated file for %s' % old_file)
                os.remove(os.path.join(directory, old_file))


def refresh_autodoc(source_path, generated_path, module_name):
    # Only update documentation if file exists
    if not os.access(generated_path, os.F_OK):
        return None

    fp = open(generated_path, 'w')

    module_type = 'modules'

    if source_path.startswith(INTERFACES_DIR) and write_autodoc_interface(fp, module_name):
        module_type = 'interfaces'
    elif source_path.startswith(OBJECTS_DIR) and write_autodoc_object(fp, module_name):
        module_type = 'objects'
    else:
        write_autodoc_module(fp, module_name)

    fp.close()

    return module_type


def write_autodoc_module(fp, module_name):
    # Write header
    header = ":mod:`%s`" % module_name

    fp.write('%s\n' % ('=' * len(header),))
    fp.write('%s\n' % header)
    fp.write('%s\n' % ('=' * len(header),))

    # Write modules
    fp.write('.. automodule:: %s\n' % module_name)
    fp.write('  :members:\n')
    fp.write('  :undoc-members:\n')
    fp.write('  :show-inheritance:\n')


def write_autodoc_interface(fp, module_name):
    # Import interface
    interface = import_subclass(module_name, Interface)

    if not interface:
        print('Unable to find interface in module %r' % module_name)
        return False

    # Retrieve interface path
    path = interface.path

    if not path:
        print('Invalid "path" property found on %r' % interface)
        return False

    # Retrieve interface members
    members = [
        name for name in dir(interface)
        if not name.startswith('_') and name not in IGNORED_INTERFACE_MEMBERS
    ]

    # Write header
    header = ":code:`Trakt['%s']`" % path

    fp.write('%s\n' % ('=' * len(header),))
    fp.write('%s\n' % header)
    fp.write('%s\n\n' % ('=' * len(header),))

    # Write modules
    fp.write('.. automodule:: %s\n\n' % module_name)
    fp.write('  .. autoclass:: %s\n' % interface.__name__)
    fp.write('    :members: %s\n' % ', '.join(members))
    fp.write('    :undoc-members:\n')
    return True


def write_autodoc_object(fp, module_name):
    # Import interface
    obj = import_subclass(module_name, object)

    if not obj:
        print('Unable to find object in module %r' % module_name)
        return False

    # Write header
    header = ":code:`%s`" % obj.__name__

    fp.write('%s\n' % ('=' * len(header),))
    fp.write('%s\n' % header)
    fp.write('%s\n' % ('=' * len(header),))

    # Write modules
    fp.write('.. automodule:: %s\n' % module_name)
    fp.write('  :inherited-members:\n')
    fp.write('  :members:\n')
    fp.write('  :undoc-members:\n')
    fp.write('  :show-inheritance:\n')
    return True


def import_subclass(module_name, base):
    # TODO display a warning if multiple classes have been found?

    module = __import__(module_name, fromlist='*')
    result = None

    for name in dir(module):
        value = getattr(module, name)

        if not value or not inspect.isclass(value):
            continue

        if value.__module__ != module_name:
            continue

        if issubclass(value, base):
            result = value
            break

    return result


refresh_autodoc_index()

# -- General configuration ------------------------------------------------


# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'trakt.sphinxext',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'trakt.py'
copyright = u'2015 - 2016, Dean Gardiner'
author = u'Dean Gardiner'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

# Read current package version
_version = {}

with open(os.path.join(ROOT_DIR, "trakt", "version.py")) as fp:
    exec(fp.read(), _version)

# The short X.Y version.
version = _version['__version__']

# The full version, including alpha/beta/rc tags.
release = _version['__version__']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Intersphinx mappings
intersphinx_mapping = {
    'python': ('https://docs.python.org/2', None)
}


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    'index': [
        'sidebar_header.html',
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ],
    '**': [
        'sidebar_header.html',
        'sidebar_index.html',
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'traktpydoc'


from docutils.utils import get_source_line
import sphinx.environment


def _warn_node(self, msg, node, **kwargs):
    if not msg.startswith('nonlocal image URI found:'):
        self._warnfunc(msg, '%s:%s' % get_source_line(node))

sphinx.environment.BuildEnvironment.warn_node = _warn_node
