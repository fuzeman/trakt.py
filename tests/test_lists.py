# flake8: noqa: F403, F405
from __future__ import absolute_import, division, print_function

from tests.core import mock
from trakt import Trakt
from trakt.objects import PublicList, User

from hamcrest import *
from httmock import HTTMock


def test_popular():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['lists'].popular()

    assert_that(items, all_of(
        has_length(2),
        contains(
            all_of(
                instance_of(PublicList),
                has_properties({
                    'pk': ('trakt', '1338'),
                    'name': 'Top Chihuahua Movies',
                    'description': 'So cute.',
                    'privacy': 'public',

                    'allow_comments': True,
                    'display_numbers': True,
                    'sort_by': 'rank',
                    'sort_how': 'asc',

                    'comment_count': 20,
                    'comment_total': 20,
                    'like_count': 109,
                    'like_total': 109,

                    'item_count': 50,

                    # Keys
                    'keys': [
                        ('trakt', '1338'),
                        ('slug', 'top-chihuahua-movies')
                    ],

                    # User
                    'user': all_of(
                        instance_of(User),
                        has_properties({
                            'pk': ('slug', 'justin'),
                            'username': 'justin',
                            'private': False,
                            'name': 'Justin Nemeth',

                            'vip': True,
                            'vip_ep': False
                        })
                    )
                })
            ),
            all_of(
                instance_of(PublicList),
                has_properties({
                    'pk': ('trakt', '1337'),
                    'name': 'Incredible Thoughts',
                    'description': 'How could my brain conceive them?',
                    'privacy': 'public',

                    'allow_comments': True,
                    'display_numbers': True,
                    'sort_by': 'rank',
                    'sort_how': 'asc',

                    'comment_count': 10,
                    'comment_total': 10,
                    'like_count': 99,
                    'like_total': 99,

                    'item_count': 50,

                    # Keys
                    'keys': [
                        ('trakt', '1337'),
                        ('slug', 'incredible-thoughts')
                    ],

                    # User
                    'user': all_of(
                        instance_of(User),
                        has_properties({
                            'pk': ('slug', 'justin'),
                            'username': 'justin',
                            'private': False,
                            'name': 'Justin Nemeth',

                            'vip': True,
                            'vip_ep': False
                        })
                    )
                })
            )
        )
    ))


def test_trending():
    with HTTMock(mock.fixtures, mock.unknown):
        items = Trakt['lists'].trending()

    assert_that(items, all_of(
        has_length(2),
        contains(
            all_of(
                instance_of(PublicList),
                has_properties({
                    'pk': ('trakt', '1337'),
                    'name': 'Incredible Thoughts',
                    'description': 'How could my brain conceive them?',
                    'privacy': 'public',

                    'allow_comments': True,
                    'display_numbers': True,
                    'sort_by': 'rank',
                    'sort_how': 'asc',

                    'comment_count': 5,
                    'comment_total': 10,
                    'like_count': 5,
                    'like_total': 99,

                    'item_count': 50,

                    # Keys
                    'keys': [
                        ('trakt', '1337'),
                        ('slug', 'incredible-thoughts')
                    ],

                    # User
                    'user': all_of(
                        instance_of(User),
                        has_properties({
                            'pk': ('slug', 'justin'),
                            'username': 'justin',
                            'private': False,
                            'name': 'Justin Nemeth',

                            'vip': True,
                            'vip_ep': False
                        })
                    )
                })
            ),
            all_of(
                instance_of(PublicList),
                has_properties({
                    'pk': ('trakt', '1338'),
                    'name': 'Top Chihuahua Movies',
                    'description': 'So cute.',
                    'privacy': 'public',

                    'allow_comments': True,
                    'display_numbers': True,
                    'sort_by': 'rank',
                    'sort_how': 'asc',

                    'comment_count': 4,
                    'comment_total': 20,
                    'like_count': 4,
                    'like_total': 109,

                    'item_count': 50,

                    # Keys
                    'keys': [
                        ('trakt', '1338'),
                        ('slug', 'top-chihuahua-movies')
                    ],

                    # User
                    'user': all_of(
                        instance_of(User),
                        has_properties({
                            'pk': ('slug', 'justin'),
                            'username': 'justin',
                            'private': False,
                            'name': 'Justin Nemeth',

                            'vip': True,
                            'vip_ep': False
                        })
                    )
                })
            )
        )
    ))
