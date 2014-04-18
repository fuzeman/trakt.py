from trakt import __version__

from setuptools import setup, find_packages

setup(
    name='trakt.py',
    version=__version__,
    url='https://github.com/fuzeman/trakt.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='',
    packages=find_packages(),
    platforms='any',

    install_requires=[
        'requests'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
