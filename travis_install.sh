# Install trakt.py
pip install .

# Install dependencies
if [[ $TRAVIS_PYTHON_VERSION == '3.2' ]]; then
    pip install -r requirements_py32.txt
else
    pip install -r requirements.txt
fi

# Install test requirements
if [[ $TRAVIS_PYTHON_VERSION == '3.2' ]]; then
    pip install -r requirements_test_py32.txt
else
    pip install -r requirements_test.txt
fi

# Install travis requirements
if [[ $TRAVIS_PYTHON_VERSION == '3.2' ]]; then
    pip install -r requirements_travis_py32.txt
else
    pip install -r requirements_travis.txt
fi
