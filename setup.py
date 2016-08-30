from setuptools import setup, find_packages
import os
import re
import sys

BASE_DIR = os.path.dirname(__file__)

RE_DEPENDENCY_LINK = re.compile(r"^(?P<url>(?P<protocol>[\w\+]+):\/\/.*?)(?:#egg=(?P<egg>.*?))?$", re.IGNORECASE)
RE_EGG_VERSION = re.compile(r"^(?P<name>.*?)(?:-(?P<version>\d+\.\d+(?:\.\d+)?))?$", re.IGNORECASE)


def read_requirements_file(path):
    path = os.path.join(BASE_DIR, path)

    if not os.path.exists(path):
        sys.stderr.write('ERROR: Unable to read requirements file at %r\n', path)
        return [], []

    # Parse requirements from file
    dependency_links = []
    requirements = []

    for line in open(path):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        # Check for dependency links
        m_link = RE_DEPENDENCY_LINK.match(line)

        if m_link:
            egg = m_link.group('egg')

            if not egg:
                sys.stderr.write('ERROR: Missing "egg" parameter for: %r\n', line)
                continue

            # Add requirement
            m_egg = RE_EGG_VERSION.match(egg)

            if m_egg.group('name') and m_egg.group('version'):
                requirements.append('%s==%s' % (m_egg.group('name'), m_egg.group('version')))
            elif m_egg.group('name'):
                requirements.append(m_egg.group('name'))
            else:
                sys.stderr.write('ERROR: Invalid "egg" definition: %r\n', egg)
                continue

            # Add dependency link
            dependency_links.append(line)
            continue

        # Simple requirement
        requirements.append(line)

    return dependency_links, requirements


def read_requirements():
    dependency_links = []

    install_requires = []
    test_requires = []

    def parse(requires, path):
        d, r = read_requirements_file(path)

        dependency_links.extend(d)
        requires.extend(r)

    # Parse requirement files
    parse(install_requires, 'requirements.txt')
    parse(test_requires, 'requirements_test.txt')

    return {
        'dependency_links': dependency_links,

        'install_requires': install_requires,
        'tests_require': test_requires
    }

# Read current package version
version = {}

with open(os.path.join(BASE_DIR, "trakt", "version.py")) as fp:
    exec(fp.read(), version)

# Read contents of the "README.rst" file
with open(os.path.join(BASE_DIR, 'README.rst')) as fp:
    readme = fp.read()

# Setup configuration
setup(
    name='trakt.py',
    version=version['__version__'],
    description='Python interface for the trakt.tv API',
    long_description=readme,
    url='https://github.com/fuzeman/trakt.py',
    license='MIT',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    # Packages
    platforms='any',
    packages=find_packages(include=[
        'trakt*'
    ]),

    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    # Requirements
    setup_requires=[
        'pytest-runner'
    ],

    **read_requirements()
)
