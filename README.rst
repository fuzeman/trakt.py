trakt.py
========

.. image:: https://img.shields.io/pypi/v/trakt.py.svg?style=flat-square
   :target: https://pypi.python.org/pypi/trakt.py

.. image:: https://github.com/fuzeman/trakt.py/actions/workflows/test.yml/badge.svg
   :target: https://github.com/fuzeman/trakt.py/actions/workflows/test.yml

.. image:: https://img.shields.io/codeclimate/github/fuzeman/trakt.py.svg?style=flat-square
   :target: https://codeclimate.com/github/fuzeman/trakt.py

.. image:: https://img.shields.io/coveralls/fuzeman/trakt.py.svg?style=flat-square
   :target: https://coveralls.io/r/fuzeman/trakt.py?branch=master

Python interface for the Trakt.tv API.

Install
-------

.. code-block:: shell

    pip install trakt.py

Examples
--------

**Configure the client**

.. code-block:: python

    from trakt import Trakt


    Trakt.configuration.defaults.client(
        id='<client-id>',
        secret='<client-secret>'
    )


**Scrobble an episode**

.. code-block:: python

    show = {
        'title': 'Community',
        'year': 2009
    }

    episode = {
        'season': 5,
        'number': 13
    }

    # Send "start" event
    Trakt['scrobble'].start(
        show=show,
        episode=episode,

        progress=1
    )

    # [...] (watching episode)

    # Send "stop" event (scrobble)
    Trakt['scrobble'].stop(
        show=show,
        episode=episode,

        progress=93
    )

**Add a movie to your collection**

.. code-block:: python

    Trakt['sync/collection'].add({
        'movies': [
            {
                'title': "Twelve Monkeys",
                'year': 1995,

                'ids': {
                    'imdb': "tt0114746"
                }
            }
        ]
    })

**Retrieve shows that a user has watched**

.. code-block:: python

    # `watched` = {<key>: <Show>} dictionary
    watched = Trakt['sync/watched'].movies()

    for key, show in watched.items():
        print '%s (%s)' % (show.title, show.year)

Trakt API support
-----------------

.. list-table::
   :widths: 45 10 45
   :header-rows: 1

   * - Trakt endpoint
     - method
     - trakt.py interface
   * - `calendars/my/shows <https://trakt.docs.apiary.io/#reference/calendars/my-shows/get-shows>`_
     - :code:`GET`
     - :code:`Trakt['calendars/my/shows'].get()`
   * - `calendars/my/shows/new <https://trakt.docs.apiary.io/#reference/calendars/my-new-show/get-new-shows>`_
     - :code:`GET`
     - :code:`Trakt['calendars/my/shows'].new()`
   * - `calendars/my/shows/premieres <https://trakt.docs.apiary.io/#reference/calendars/my-season-premieres/get-season-premieres>`_
     - :code:`GET`
     - :code:`Trakt['calendars/my/shows'].premieres()` 
   * - `calendars/my/movies <https://trakt.docs.apiary.io/#reference/calendars/my-movies/get-movies>`_
     - :code:`GET`
     - :code:`Trakt['calendars/my/movies'].get()`
   * - `calendars/my/dvd <https://trakt.docs.apiary.io/#reference/calendars/my-dvd/get-dvd-releases>`_
     - :code:`GET`
     - :code:`Trakt['calendars/my/dvd'].get()`
   * - `calendars/all/shows <https://trakt.docs.apiary.io/#reference/calendars/all-shows/get-shows>`_
     - :code:`GET`
     - :code:`Trakt['calendars/all/shows'].get()`
   * - `calendars/all/shows/new <https://trakt.docs.apiary.io/#reference/calendars/all-new-shows/get-new-shows>`_
     - :code:`GET`
     - :code:`Trakt['calendars/all/shows'].new()`
   * - `calendars/all/shows/premiers <https://trakt.docs.apiary.io/#reference/calendars/all-season-premieres/get-season-premieres>`_
     - :code:`GET`
     - :code:`Trakt['calendars/all/shows'].premiers()`
   * - `calendars/all/movies <https://trakt.docs.apiary.io/#reference/calendars/all-movies/get-movies>`_
     - :code:`GET`
     - :code:`Trakt['calendars/all/movies'].get()`
   * - `calendars/all/dvd <https://trakt.docs.apiary.io/#reference/calendars/all-dvd/get-dvd-releases>`_
     - :code:`GET`
     - :code:`Trakt['calendars/all/dvd'].get()`
   * - `checkin <https://trakt.docs.apiary.io/#reference/checkin/check-into-an-item>`_
     - :code:`POST`
     - 
   * - `certifications/<type> <https://trakt.docs.apiary.io/#reference/certifications/list/get-certifications>`_
     - :code:`GET`
     - 
   * - `comments <https://trakt.docs.apiary.io/#reference/comments/comments/post-a-comment>`_
     - :code:`POST`
     - 
   * - `comments/<id> <https://trakt.docs.apiary.io/#reference/comments/comment/get-a-comment-or-reply>`_
     - :code:`GET`
     - 
   * - `comments/<id> (update) <https://trakt.docs.apiary.io/#reference/comments/comment/update-a-comment-or-reply>`_
     - :code:`PUT`
     - 
   * - `comments/<id> (remove) <https://trakt.docs.apiary.io/#reference/comments/comment/delete-a-comment-or-reply>`_
     - :code:`DELETE`
     - 
   * - `comments/<id>/replies <https://trakt.docs.apiary.io/#reference/comments/replies/get-replies-for-a-comment>`_
     - :code:`GET`
     - 
   * - `comments/<id>/replies (add) <https://trakt.docs.apiary.io/#reference/comments/replies/post-a-reply-for-a-comment>`_
     - :code:`POST`
     - 
   * - `comments/<id>/item <https://trakt.docs.apiary.io/#reference/comments/item/get-the-attached-media-item>`_
     - :code:`GET`
     - 
   * - `comments/<id>/likes <https://trakt.docs.apiary.io/#reference/comments/likes/get-all-users-who-liked-a-comment>`_
     - :code:`GET`
     - 
   * - `comments/<id>/like <https://trakt.docs.apiary.io/#reference/comments/like/like-a-comment>`_
     - :code:`POST`
     - 
   * - `comments/<id>/like (remove) <https://trakt.docs.apiary.io/#reference/comments/like/remove-like-on-a-comment>`_
     - :code:`DELETE`
     - 
   * - `comments/trending/<comment_type>/<type> <https://trakt.docs.apiary.io/#reference/comments/trending/get-trending-comments>`_
     - :code:`GET`
     - 
   * - `comments/recent/<comment_type>/<type> <https://trakt.docs.apiary.io/#reference/comments/recent/get-recently-created-comments>`_
     - :code:`GET`
     - 
   * - `comments/updates/<comment_type>/<type> <https://trakt.docs.apiary.io/#reference/comments/updates/get-recently-updated-comments>`_
     - :code:`GET`
     - 
   * - `countries/<type> <https://trakt.docs.apiary.io/#reference/countries/list/get-countries>`_
     - :code:`GET`
     - 
   * - `genres/<type> <https://trakt.docs.apiary.io/#reference/genres/list/get-genres>`_
     - :code:`GET`
     - 
   * - `languages/<type> <https://trakt.docs.apiary.io/#reference/languages/list/get-languages>`_
     - :code:`GET`
     - 
   * - `lists/trending <https://trakt.docs.apiary.io/#reference/lists/trending/get-trending-lists>`_
     - :code:`GET`
     - :code:`Trakt['lists'].trending()`
   * - `lists/popular <https://trakt.docs.apiary.io/#reference/lists/popular/get-popular-lists>`_
     - :code:`GET`
     - :code:`Trakt['lists'].popular()`
   * - `lists/<id> <https://trakt.docs.apiary.io/#reference/lists/list/get-list>`_
     - :code:`GET`
     - 
   * - `lists/<id>/likes <https://trakt.docs.apiary.io/#reference/lists/list-likes/get-all-users-who-liked-a-list>`_
     - :code:`GET`
     - 
   * - `lists/<id>/items <https://trakt.docs.apiary.io/#reference/lists/list-items/get-items-on-a-list>`_
     - :code:`GET`
     - 
   * - `lists/<id>/comments <https://trakt.docs.apiary.io/#reference/lists/list-comments/get-all-list-comments>`_
     - :code:`GET`
     - 
   * - `movies/trending <https://trakt.docs.apiary.io/#reference/movies/trending/get-trending-movies>`_
     - :code:`GET`
     - :code:`Trakt['movies'].trending()`
   * - `movies/popular <https://trakt.docs.apiary.io/#reference/movies/popular/get-popular-movies>`_
     - :code:`GET`
     - :code:`Trakt['movies'].popular()`
   * - `movies/recommended <https://trakt.docs.apiary.io/#reference/movies/recommended/get-the-most-recommended-movies>`_
     - :code:`GET`
     - :code:`Trakt['movies'].recommended()`
   * - `movies/played <https://trakt.docs.apiary.io/#reference/movies/played/get-the-most-played-movies>`_
     - :code:`GET`
     - 
   * - `movies/watched <https://trakt.docs.apiary.io/#reference/movies/watched/get-the-most-watched-movies>`_
     - :code:`GET`
     - 
   * - `movies/collected <https://trakt.docs.apiary.io/#reference/movies/collected/get-the-most-collected-movies>`_
     - :code:`GET`
     - 
   * - `movies/anticipated <https://trakt.docs.apiary.io/#reference/movies/anticipated/get-the-most-anticipated-movies>`_
     - :code:`GET`
     - 
   * - `movies/boxoffice <https://trakt.docs.apiary.io/#reference/movies/box-office/get-the-weekend-box-office>`_
     - :code:`GET`
     - 
   * - `movies/updates <https://trakt.docs.apiary.io/#reference/movies/updates/get-recently-updated-movies>`_
     - :code:`GET`
     - 
   * - `movies/updates/id <https://trakt.docs.apiary.io/#reference/movies/updated-ids/get-recently-updated-movie-trakt-ids>`_
     - :code:`GET`
     - 
   * - `movies/id <https://trakt.docs.apiary.io/#reference/movies/summary/get-a-movie>`_
     - :code:`GET`
     - :code:`Trakt['movies'].get()`
   * - `movies/id/aliases <https://trakt.docs.apiary.io/#reference/movies/aliases/get-all-movie-aliases>`_
     - :code:`GET`
     - 
   * - `movies/id/releases <https://trakt.docs.apiary.io/#reference/movies/releases/get-all-movie-releases>`_
     - :code:`GET`
     - 
   * - `movies/id/translations <https://trakt.docs.apiary.io/#reference/movies/translations/get-all-movie-translations>`_
     - :code:`GET`
     - 
   * - `movies/id/comments <https://trakt.docs.apiary.io/#reference/movies/comments/get-all-movie-comments>`_
     - :code:`GET`
     - 
   * - `movies/id/lists <https://trakt.docs.apiary.io/#reference/movies/lists/get-lists-containing-this-movie>`_
     - :code:`GET`
     - 
   * - `movies/id/people <https://trakt.docs.apiary.io/#reference/movies/people/get-all-people-for-a-movie>`_
     - :code:`GET`
     - 
   * - `movies/id/ratings <https://trakt.docs.apiary.io/#reference/movies/ratings/get-movie-ratings>`_
     - :code:`GET`
     - 
   * - `movies/id/related <https://trakt.docs.apiary.io/#reference/movies/related/get-related-movies>`_
     - :code:`GET`
     - 
   * - `movies/id/stats <https://trakt.docs.apiary.io/#reference/movies/stats/get-movie-stats>`_
     - :code:`GET`
     - 
   * - `movies/id/studios <https://trakt.docs.apiary.io/#reference/movies/studios/get-movie-studios>`_
     - :code:`GET`
     - 
   * - `movies/id/watching <https://trakt.docs.apiary.io/#reference/movies/watching/get-users-watching-right-now>`_
     - :code:`GET`
     - 
   * - `networks <https://trakt.docs.apiary.io/#reference/networks/list/get-networks>`_
     - :code:`GET`
     - 
   * - `people/updates <https://trakt.docs.apiary.io/#reference/people/updates/get-recently-updated-people>`_
     - :code:`GET`
     - 
   * - `people/updates/id <https://trakt.docs.apiary.io/#reference/people/updated-ids/get-recently-updated-people-trakt-ids>`_
     - :code:`GET`
     - 
   * - `people/<id> <https://trakt.docs.apiary.io/#reference/people/summary/get-a-single-person>`_
     - :code:`GET`
     - 
   * - `people/<id>/movies <https://trakt.docs.apiary.io/#reference/people/movies/get-movie-credits>`_
     - :code:`GET`
     - 
   * - `people/<id>/shows <https://trakt.docs.apiary.io/#reference/people/shows/get-show-credits>`_
     - :code:`GET`
     - 
   * - `people/<id>/lists <https://trakt.docs.apiary.io/#reference/people/lists/get-lists-containing-this-person>`_
     - :code:`GET`
     - 
   * - `recommendations/movies <https://trakt.docs.apiary.io/#reference/recommendations/movies/get-movie-recommendations>`_
     - :code:`GET`
     - 
   * - `recommendations/movies/<id> <https://trakt.docs.apiary.io/#reference/recommendations/hide-movie/hide-a-movie-recommendation>`_
     - :code:`DELETE`
     - 
   * - `recommendations/shows <https://trakt.docs.apiary.io/#reference/recommendations/shows/get-show-recommendations>`_
     - :code:`GET`
     - 
   * - `recommendations/shows/<id> <https://trakt.docs.apiary.io/#reference/recommendations/hide-show/hide-a-show-recommendation>`_
     - :code:`DELETE`
     - 
   * - `scrobble/start <https://trakt.docs.apiary.io/#reference/scrobble/start/start-watching-in-a-media-center>`_
     - :code:`POST`
     - :code:`Trakt['scrobble'].start()`
   * - `scrobble/pause <https://trakt.docs.apiary.io/#reference/scrobble/pause/pause-watching-in-a-media-center>`_
     - :code:`POST`
     - :code:`Trakt['scrobble'].pause()`
   * - `scrobble/stop <https://trakt.docs.apiary.io/#reference/scrobble/stop/stop-or-finish-watching-in-a-media-center>`_
     - :code:`POST`
     - :code:`Trakt['scrobble'].stop()`
   * - `search/<type> <https://trakt.docs.apiary.io/#reference/search/text-query/get-text-query-results>`_
     - :code:`GET`
     - :code:`Trakt['search'].query()`
   * - `search/<id_type>/<id> <https://trakt.docs.apiary.io/#reference/search/id-lookup/get-id-lookup-results>`_
     - :code:`GET`
     - :code:`Trakt['search'].lookup()`
   * - `shows/trending <https://trakt.docs.apiary.io/#reference/shows/trending/get-trending-shows>`_
     - :code:`GET`
     - :code:`Trakt['shows'].trending()`
   * - `shows/popular <https://trakt.docs.apiary.io/#reference/shows/popular/get-popular-shows>`_
     - :code:`GET`
     - :code:`Trakt['shows'].popular()`
   * - `shows/recommended <https://trakt.docs.apiary.io/#reference/shows/recommended/get-the-most-recommended-shows>`_
     - :code:`GET`
     - :code:`Trakt['shows'].recommended()`
   * - `shows/played <https://trakt.docs.apiary.io/#reference/shows/played/get-the-most-played-shows>`_
     - :code:`GET`
     - 
   * - `shows/watched <https://trakt.docs.apiary.io/#reference/shows/watched/get-the-most-watched-shows>`_
     - :code:`GET`
     - 
   * - `shows/collected <https://trakt.docs.apiary.io/#reference/shows/collected/get-the-most-collected-shows>`_
     - :code:`GET`
     - 
   * - `shows/anticipated <https://trakt.docs.apiary.io/#reference/shows/anticipated/get-the-most-anticipated-shows>`_
     - :code:`GET`
     - 
   * - `shows/updates <https://trakt.docs.apiary.io/#reference/shows/updates/get-recently-updated-shows>`_
     - :code:`GET`
     - 
   * - `shows/updates/id <https://trakt.docs.apiary.io/#reference/shows/updated-ids/get-recently-updated-show-trakt-ids>`_
     - :code:`GET`
     - 
   * - `shows/<id> <https://trakt.docs.apiary.io/#reference/shows/summary/get-a-single-show>`_
     - :code:`GET`
     - :code:`Trakt['shows'].get()`
   * - `shows/<id>/aliases <https://trakt.docs.apiary.io/#reference/shows/aliases/get-all-show-aliases>`_
     - :code:`GET`
     - 
   * - `shows/<id>/certifications <https://trakt.docs.apiary.io/#reference/shows/certifications/get-all-show-certifications>`_
     - :code:`GET`
     - 
   * - `shows/<id>/translations <https://trakt.docs.apiary.io/#reference/shows/translations/get-all-show-translations>`_
     - :code:`GET`
     - 
   * - `shows/<id>/comments <https://trakt.docs.apiary.io/#reference/shows/comments/get-all-show-comments>`_
     - :code:`GET`
     - 
   * - `shows/<id>/lists <https://trakt.docs.apiary.io/#reference/shows/lists/get-lists-containing-this-show>`_
     - :code:`GET`
     - 
   * - `shows/<id>/progress/collection <https://trakt.docs.apiary.io/#reference/shows/collection-progress/get-show-collection-progress>`_
     - :code:`GET`
     - :code:`Trakt['shows'].progress_collection()`
   * - `shows/<id>/progress/watched <https://trakt.docs.apiary.io/#reference/shows/watched-progress/get-show-watched-progress>`_
     - :code:`GET`
     - :code:`Trakt['shows'].progress_watched()`
   * - `shows/<id>/progress/watched/reset <https://trakt.docs.apiary.io/#reference/shows/reset-watched-progress/reset-show-progress>`_
     - :code:`GET`
     - 
   * - `shows/<id>/progress/watched/reset (undo) <https://trakt.docs.apiary.io/#reference/shows/reset-watched-progress/undo-reset-show-progress>`_
     - :code:`DELETE`
     - 
   * - `shows/<id>/people <https://trakt.docs.apiary.io/#reference/shows/people/get-all-people-for-a-show>`_
     - :code:`GET`
     - 
   * - `shows/<id>/ratings <https://trakt.docs.apiary.io/#reference/shows/ratings/get-show-ratings>`_
     - :code:`GET`
     - 
   * - `shows/<id>/related <https://trakt.docs.apiary.io/#reference/shows/related/get-related-shows>`_
     - :code:`GET`
     - 
   * - `shows/<id>/stats <https://trakt.docs.apiary.io/#reference/shows/stats/get-show-stats>`_
     - :code:`GET`
     - 
   * - `shows/<id>/studios <https://trakt.docs.apiary.io/#reference/shows/studios/get-show-studios>`_
     - :code:`GET`
     - 
   * - `shows/<id>/watching <https://trakt.docs.apiary.io/#reference/shows/watching/get-users-watching-right-now>`_
     - :code:`GET`
     - 
   * - `shows/<id>/next_episode <https://trakt.docs.apiary.io/#reference/shows/next-episode/get-next-episode>`_
     - :code:`GET`
     - :code:`Trakt['shows'].next_episode()`
   * - `shows/<id>/last_episode <https://trakt.docs.apiary.io/#reference/shows/last-episode/get-last-episode>`_
     - :code:`GET`
     - :code:`Trakt['shows'].last_episode()`
   * - `shows/<id>/seasons <https://trakt.docs.apiary.io/#reference/seasons/summary/get-all-seasons-for-a-show>`_
     - :code:`GET`
     - :code:`Trakt['shows'].seasons()`
   * - `shows/<id>/seasons/<season> <https://trakt.docs.apiary.io/#reference/seasons/season/get-single-season-for-a-show>`_
     - :code:`GET`
     - :code:`Trakt['shows'].season()`
   * - `shows/<id>/seasons/<season>/translations <https://trakt.docs.apiary.io/#reference/seasons/translations/get-all-season-translations>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/comments <https://trakt.docs.apiary.io/#reference/seasons/comments/get-all-season-comments>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/lists <https://trakt.docs.apiary.io/#reference/seasons/lists/get-lists-containing-this-season>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/people <https://trakt.docs.apiary.io/#reference/seasons/people/get-all-people-for-a-season>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/ratings <https://trakt.docs.apiary.io/#reference/seasons/ratings/get-season-ratings>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/stats <https://trakt.docs.apiary.io/#reference/seasons/stats/get-season-stats>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/watching <https://trakt.docs.apiary.io/#reference/seasons/watching/get-users-watching-right-now>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/episode <https://trakt.docs.apiary.io/#reference/episodes/summary/get-a-single-episode-for-a-show>`_
     - :code:`GET`
     - :code:`Trakt['shows'].episode()`
   * - `shows/<id>/seasons/<season>/episodes/<episode>/translations <https://trakt.docs.apiary.io/#reference/episodes/translations/get-all-episode-translations>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/comments <https://trakt.docs.apiary.io/#reference/episodes/comments/get-all-episode-comments>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/lists <https://trakt.docs.apiary.io/#reference/episodes/lists/get-lists-containing-this-episode>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/people <https://trakt.docs.apiary.io/#reference/episodes/people/get-all-people-for-an-episode>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/ratings <https://trakt.docs.apiary.io/#reference/episodes/ratings/get-episode-ratings>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/stats <https://trakt.docs.apiary.io/#reference/episodes/stats/get-episode-stats>`_
     - :code:`GET`
     - 
   * - `shows/<id>/seasons/<season>/episodes/<episode>/watching <https://trakt.docs.apiary.io/#reference/episodes/watching/get-users-watching-right-now>`_
     - :code:`GET`
     - 
   * - `sync/last_activities <https://trakt.docs.apiary.io/#reference/sync/last-activities/get-last-activity>`_
     - :code:`GET`
     - :code:`Trakt['sync'].last_activities()`
   * - `sync/playback <https://trakt.docs.apiary.io/#reference/sync/playback/get-playback-progress>`_
     - :code:`GET`
     - :code:`Trakt['sync/playback'].get()`
   * - `sync/playback/<id> <https://trakt.docs.apiary.io/#reference/sync/remove-playback/remove-a-playback-item>`_
     - :code:`DELETE`
     - :code:`Trakt['sync/playback'].delete()`
   * - `sync/collection/<type> <https://trakt.docs.apiary.io/#reference/sync/get-collection/get-collection>`_
     - :code:`GET`
     - :code:`Trakt['sync/collection'].movies()`, :code:`Trakt['sync/collection'].shows()`
   * - `sync/collection <https://trakt.docs.apiary.io/#reference/sync/add-to-collection/add-items-to-collection>`_
     - :code:`POST`
     - :code:`Trakt['sync/collection'].add()`
   * - `sync/collection/remove <https://trakt.docs.apiary.io/#reference/sync/remove-from-collection/remove-items-from-collection>`_
     - :code:`POST`
     - :code:`Trakt['sync/collection'].remove()`
   * - `sync/watched/<type> <https://trakt.docs.apiary.io/#reference/sync/get-watched/get-watched>`_
     - :code:`GET`
     - :code:`Trakt['sync/watched'].movies()`, :code:`Trakt['sync/watched'].shows()`
   * - `sync/history <https://trakt.docs.apiary.io/#reference/sync/get-history/get-watched-history>`_
     - :code:`GET`
     - :code:`Trakt['sync/history'].episodes()`, :code:`Trakt['sync/history'].movies()`, :code:`Trakt['sync/history'].seasons()`, :code:`Trakt['sync/history'].shows()`
   * - `sync/history (add) <https://trakt.docs.apiary.io/#reference/sync/add-to-history/add-items-to-watched-history>`_
     - :code:`POST`
     - :code:`Trakt['sync/history'].add()`
   * - `sync/history/remove <https://trakt.docs.apiary.io/#reference/sync/remove-from-history/remove-items-from-history>`_
     - :code:`POST`
     - :code:`Trakt['sync/history'].remove()`
   * - `sync/ratings <https://trakt.docs.apiary.io/#reference/sync/get-ratings/get-ratings>`_
     - :code:`GET`
     - :code:`Trakt['sync/ratings'].add()`, :code:`Trakt['sync/ratings'].episodes()`, :code:`Trakt['sync/ratings'].movies()`, :code:`Trakt['sync/ratings'].seasons()`, :code:`Trakt['sync/ratings'].shows()`
   * - `sync/ratings (add) <https://trakt.docs.apiary.io/#reference/sync/add-ratings/add-new-ratings>`_
     - :code:`POST`
     - :code:`Trakt['sync/ratings'].add()`
   * - `sync/ratings/remove <https://trakt.docs.apiary.io/#reference/sync/remove-ratings>`_
     - :code:`POST`
     - :code:`Trakt['sync/ratings'].remove()`
   * - `sync/watchlist <https://trakt.docs.apiary.io/#reference/sync/get-watchlist/get-watchlist>`_
     - :code:`GET`
     - :code:`Trakt['sync/watchlist'].episodes()`, :code:`Trakt['sync/watchlist'].movies()`, :code:`Trakt['sync/watchlist'].seasons()`, :code:`Trakt['sync/watchlist'].shows()`
   * - `sync/watchlist (add) <https://trakt.docs.apiary.io/#reference/sync/add-to-watchlist/add-items-to-watchlist>`_
     - :code:`POST`
     - :code:`Trakt['sync/watchlist'].add()`
   * - `sync/watchlist/remove <https://trakt.docs.apiary.io/#reference/sync/remove-from-watchlist/remove-items-from-watchlist>`_
     - :code:`POST`
     - :code:`Trakt['sync/watchlist'].remove()`
   * - `sync/watchlist/reorder <https://trakt.docs.apiary.io/#reference/sync/reorder-watchlist/reorder-watchlist-items>`_
     - :code:`POST`
     - 
   * - `sync/recommendations <https://trakt.docs.apiary.io/#reference/sync/get-personal-recommendations-beta/get-personal-recommendations>`_
     - :code:`GET`
     - 
   * - `sync/recommendations (add) <https://trakt.docs.apiary.io/#reference/sync/add-to-personal-recommendations-beta/add-items-to-personal-recommendations>`_
     - :code:`POST`
     - 
   * - `sync/recommendations/remove <https://trakt.docs.apiary.io/#reference/sync/remove-from-personal-recommendations-beta/remove-items-from-personal-recommendations>`_
     - :code:`POST`
     - 
   * - `sync/recommendations/reorder <https://trakt.docs.apiary.io/#reference/sync/reorder-personal-recommendations-beta/reorder-personally-recommended-items>`_
     - :code:`POST`
     - 
   * - `users/settings <https://trakt.docs.apiary.io/#reference/users/settings/retrieve-settings>`_
     - :code:`GET`
     - :code:`Trakt['users/settings'].get()`
   * - `users/requests/following <https://trakt.docs.apiary.io/#reference/users/following-requests/get-pending-following-requests>`_
     - :code:`GET`
     - 
   * - `users/requests <https://trakt.docs.apiary.io/#reference/users/follower-requests/get-follow-requests>`_
     - :code:`GET`
     - 
   * - `users/requests/<id> (approve) <https://trakt.docs.apiary.io/#reference/users/approve-or-deny-follower-requests/approve-follow-request>`_
     - :code:`POST`
     - 
   * - `users/requests/<id> (deny) <https://trakt.docs.apiary.io/#reference/users/approve-or-deny-follower-requests/deny-follow-request>`_
     - :code:`DELETE`
     - 
   * - `users/saved_filters <https://trakt.docs.apiary.io/#reference/users/saved-filters/get-saved-filters>`_
     - :code:`GET`
     - 
   * - `users/hidden/<section> <https://trakt.docs.apiary.io/#reference/users/hidden-items/get-hidden-items>`_
     - :code:`GET`
     - :code:`Trakt['users/hidden/<section>'].get()`
   * - `users/hidden/<section> (add) <https://trakt.docs.apiary.io/#reference/users/add-hidden-items/add-hidden-items>`_
     - :code:`POST`
     - :code:`Trakt['users/hidden/<section>'].add()`
   * - `hidden/<section>/remove <https://trakt.docs.apiary.io/#reference/users/remove-hidden-items/remove-hidden-items>`_
     - :code:`POST`
     - :code:`Trakt['users/hidden/<section>'].remove()`
   * - `users/<id> <https://trakt.docs.apiary.io/#reference/users/profile/get-user-profile>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>'].profile()`
   * - `users/<id>/likes <https://trakt.docs.apiary.io/#reference/users/likes/get-likes>`_
     - :code:`GET`
     - :code:`Trakt['users'].likes()` (only for logged-in user)
   * - `users/<id>/collection <https://trakt.docs.apiary.io/#reference/users/collection/get-collection>`_
     - :code:`GET`
     - 
   * - `users/<id>/comments <https://trakt.docs.apiary.io/#reference/users/comments/get-comments>`_
     - :code:`GET`
     - 
   * - `users/<id>/lists <https://trakt.docs.apiary.io/#reference/users/lists/get-a-user's-personal-lists>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/lists'].get()`
   * - `users/<id>/lists (create) <https://trakt.docs.apiary.io/#reference/users/lists/create-personal-list>`_
     - :code:`POST`
     - :code:`Trakt['users/<id>/lists'].create()`
   * - `users/<id>/lists/reorder <https://trakt.docs.apiary.io/#reference/users/reorder-lists/reorder-a-user's-lists>`_
     - :code:`POST`
     - 
   * - `users/<id>/lists/collaborations <https://trakt.docs.apiary.io/#reference/users/collaborations/get-all-lists-a-user-can-collaborate-on>`_
     - :code:`GET`
     - 
   * - `users/<id>/lists/<list_id> <https://trakt.docs.apiary.io/#reference/users/list/get-personal-list>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/lists/<list_id>'].get()`
   * - `users/<id>/lists/<list_id> (update) <https://trakt.docs.apiary.io/#reference/users/list/update-personal-list>`_
     - :code:`PUT`
     - :code:`Trakt['users/<id>/lists/<list_id>'].update()`
   * - `users/<id>/lists/<list_id> (delete) <https://trakt.docs.apiary.io/#reference/users/list/delete-a-user's-personal-list>`_
     - :code:`DELETE`
     - :code:`Trakt['users/<id>/lists/<list_id>'].delete()`
   * - `users/<id>/lists/<list_id>/likes <https://trakt.docs.apiary.io/#reference/users/list-likes/get-all-users-who-liked-a-list>`_
     - :code:`GET`
     - 
   * - `users/<id>/lists/<list_id>/like <https://trakt.docs.apiary.io/#reference/users/list-like/like-a-list>`_
     - :code:`POST`
     - :code:`Trakt['users/<id>/lists/<list_id>'].like()`
   * - `users/<id>/lists/<list_id>/like (unlike) <https://trakt.docs.apiary.io/#reference/users/list-like/remove-like-on-a-list>`_
     - :code:`DELETE`
     - :code:`Trakt['users/<id>/lists/<list_id>'].unlike()`
   * - `users/<id>/lists/<list_id>/items <https://trakt.docs.apiary.io/#reference/users/list-items/get-items-on-a-personal-list>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/lists/<list_id>'].items()`
   * - `users/<id>/lists/<list_id>/items (add) <https://trakt.docs.apiary.io/#reference/users/add-list-items/add-items-to-personal-list>`_
     - :code:`POST`
     - :code:`Trakt['users/<id>/lists/<list_id>'].add()`
   * - `users/<id>/lists/<list_id>/items/remove <https://trakt.docs.apiary.io/#reference/users/remove-list-items/remove-items-from-personal-list>`_
     - :code:`POST`
     - :code:`Trakt['users/<id>/lists/<list_id>'].remove()`
   * - `users/<id>/lists/<list_id>/items/reorder <https://trakt.docs.apiary.io/#reference/users/reorder-list-items/reorder-items-on-a-list>`_
     - :code:`POST`
     - 
   * - `users/<id>/lists/<list_id>/comments <https://trakt.docs.apiary.io/#reference/users/list-comments/get-all-list-comments>`_
     - :code:`GET`
     - 
   * - `users/<id>/follow <https://trakt.docs.apiary.io/#reference/users/follow/follow-this-user>`_
     - :code:`POST`
     - :code:`Trakt['user/<id>'].follow()`
   * - `users/<id>/follow (unfollow) <https://trakt.docs.apiary.io/#reference/users/follow/unfollow-this-user>`_
     - :code:`DELETE`
     - :code:`Trakt['user/<id>'].unfollow()`
   * - `users/<id>/followers <https://trakt.docs.apiary.io/#reference/users/followers/get-followers>`_
     - :code:`GET`
     - 
   * - `users/<id>/following <https://trakt.docs.apiary.io/#reference/users/following/get-following>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/following'].get()`
   * - `users/<id>/friends <https://trakt.docs.apiary.io/#reference/users/friends/get-friends>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/friends'].get()`
   * - `users/<id>/history <https://trakt.docs.apiary.io/#reference/users/history/get-watched-history>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/history'].get()`, :code:`Trakt['users/<id>/history'].movies()`, :code:`Trakt['users/<id>/history'].seasons()`, :code:`Trakt['users/<id>/history'].shows()`, :code:`Trakt['users/<id>/history'].episodes()`
   * - `users/<id>/ratings <https://trakt.docs.apiary.io/#reference/users/ratings/get-ratings>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/ratings'].get()`, :code:`Trakt['users/<id>/ratings'].all()`, :code:`Trakt['users/<id>/ratings'].movies()`, :code:`Trakt['users/<id>/ratings'].shows()`, :code:`Trakt['users/<id>/ratings'].seasons()`, :code:`Trakt['users/<id>/ratings'].episodes()`
   * - `users/<id>/watchlist <https://trakt.docs.apiary.io/#reference/users/watchlist/get-watchlist>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/watchlist'].get()`, :code:`Trakt['users/<id>/watchlist'].movies()`, :code:`Trakt['users/<id>/watchlist'].shows()`, :code:`Trakt['users/<id>/watchlist'].seasons()`, :code:`Trakt['users/<id>/watchlist'].episodes()`
   * - `users/<id>/recommendations <https://trakt.docs.apiary.io/#reference/users/personal-recommendations-beta/get-personal-recommendations>`_
     - :code:`GET`
     - 
   * - `users/<id>/watching <https://trakt.docs.apiary.io/#reference/users/watching/get-watching>`_
     - :code:`GET`
     - 
   * - `users/<id>/watched/<type> <https://trakt.docs.apiary.io/#reference/users/watched/get-watched>`_
     - :code:`GET`
     - :code:`Trakt['users/<id>/watched'].get()`, :code:`Trakt['users/<id>/watched'].movies()`, :code:`Trakt['users/<id>/watched'].shows()`
   * - `users/<id>/stats <https://trakt.docs.apiary.io/#reference/users/stats/get-stats>`_
     - :code:`GET`
     - 


License
-------

  The MIT License (MIT)

  Copyright (c) 2014 Dean Gardiner

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
