from trakt import __version__

from setuptools import setup, find_packages

setup(
    name='trakt.py',
    version=__version__,
    license='MIT',
    url='https://github.com/fuzeman/trakt.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Python interface for the trakt.tv API',
    packages=find_packages(exclude=[
        'examples',
        'tests'
    ]),
    platforms='any',

    install_requires=[
        'arrow',
        'requests>=2.4.0',
        'six'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
