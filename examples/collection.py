from trakt import Trakt

import logging
import os

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    Trakt.api_key = os.environ.get('API_KEY')
    Trakt.credentials = ('test', 'test')

    #print Trakt['account'].test()
    #print Trakt['account'].test(credentials=('blah', 'blah'))

    print Trakt['user']
    print Trakt['user/library/movies'].watched()
    print Trakt['user/library/shows'].all()
