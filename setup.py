from setuptools import setup, find_packages
import os

base_dir = os.path.dirname(__file__)

version = {}
with open(os.path.join(base_dir, "trakt", "version.py")) as f:
    exec(f.read(), version)

setup(
    name='trakt.py',
    version=version['__version__'],
    license='MIT',
    url='https://github.com/fuzeman/trakt.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Python interface for the trakt.tv API',
    packages=find_packages(exclude=[
        'examples'
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
