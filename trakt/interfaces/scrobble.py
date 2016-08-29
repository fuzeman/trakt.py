from trakt.interfaces.base import Interface, authenticated, application


class ScrobbleInterface(Interface):
    path = 'scrobble'

    @application
    @authenticated
    def action(self, action, movie=None, show=None, episode=None, progress=0.0, **kwargs):
        """Perform specified scrobble action

        :param action: Action to perform (either :code:`start`, :code:`pause` or :code:`stop`)
        :type action: str

        :param movie: Movie definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Guardians of the Galaxy',
                    'year': 2014,

                    'ids': {
                        'tmdb': 118340
                    }
                }

        :type movie: dict or None

        :param show: Show definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Breaking Bad',
                    'year': 2008,

                    'ids': {
                        'tvdb': 81189
                    }
                }


        :type show: dict or None

        :param episode: Episode definition

            **Example:**

            .. code-block:: python

                {
                    "season": 3,
                    "number": 11
                }

        :type episode: dict or None

        :param progress: Current movie/episode progress percentage
        :type progress: float

        :param kwargs: Extra request options

        :return: Response

            **Example:**

            .. code-block:: python

                {
                    'action': 'start',
                    'progress': 1.25,

                    'sharing': {
                        'facebook': true,
                        'twitter': true,
                        'tumblr': false
                    },

                    'movie': {
                        'title': 'Guardians of the Galaxy',
                        'year': 2014,

                        'ids': {
                            'trakt': 28,
                            'slug': 'guardians-of-the-galaxy-2014',
                            'imdb': 'tt2015381',
                            'tmdb': 118340
                        }
                    }
                }

        :rtype: dict or None
        """
        if movie and (show or episode):
            raise ValueError('Only one media type should be provided')

        if not movie and not episode:
            raise ValueError('Missing media item')

        data = {
            'progress': progress,
            'app_version': kwargs.get('app_version', '1.0'),
            'app_date': kwargs.get('app_date', '2014-08-29')
        }

        if movie:
            # TODO validate
            data['movie'] = movie
        elif episode:
            if show:
                data['show'] = show

            # TODO validate
            data['episode'] = episode

        response = self.http.post(
            action,
            data=data,

            authenticated=kwargs.get('authenticated', None)
        )

        return self.get_data(response)

    @application
    @authenticated
    def start(self, movie=None, show=None, episode=None, progress=0.0, **kwargs):
        """Use this method when the video initially starts playing or is un-paused. This will
        remove any playback progress if it exists.

        **Note:** A watching status will auto expire after the remaining runtime has elapsed.
        There is no need to re-send every 15 minutes.

        :param movie: Movie definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Guardians of the Galaxy',
                    'year': 2014,

                    'ids': {
                        'tmdb': 118340
                    }
                }

        :type movie: dict or None

        :param show: Show definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Breaking Bad',
                    'year': 2008,

                    'ids': {
                        'tvdb': 81189
                    }
                }


        :type show: dict or None

        :param episode: Episode definition

            **Example:**

            .. code-block:: python

                {
                    "season": 3,
                    "number": 11
                }

        :type episode: dict or None

        :param progress: Current movie/episode progress percentage
        :type progress: float

        :param kwargs: Extra request options

        :return: Response

            **Example:**

            .. code-block:: python

                {
                    'action': 'start',
                    'progress': 1.25,

                    'sharing': {
                        'facebook': true,
                        'twitter': true,
                        'tumblr': false
                    },

                    'movie': {
                        'title': 'Guardians of the Galaxy',
                        'year': 2014,

                        'ids': {
                            'trakt': 28,
                            'slug': 'guardians-of-the-galaxy-2014',
                            'imdb': 'tt2015381',
                            'tmdb': 118340
                        }
                    }
                }

        :rtype: dict or None
        """
        return self.action(
            'start',
            movie, show, episode,
            progress,

            **kwargs
        )

    @application
    @authenticated
    def pause(self, movie=None, show=None, episode=None, progress=0.0, **kwargs):
        """Use this method when the video is paused. The playback progress will be saved and
        :code:`Trakt['sync/playback'].get()` can be used to resume the video from this exact
        position. Un-pause a video by calling the :code:`Trakt['scrobble'].start()` method again.

        :param movie: Movie definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Guardians of the Galaxy',
                    'year': 2014,

                    'ids': {
                        'tmdb': 118340
                    }
                }

        :type movie: dict or None

        :param show: Show definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Breaking Bad',
                    'year': 2008,

                    'ids': {
                        'tvdb': 81189
                    }
                }


        :type show: dict or None

        :param episode: Episode definition

            **Example:**

            .. code-block:: python

                {
                    "season": 3,
                    "number": 11
                }

        :type episode: dict or None

        :param progress: Current movie/episode progress percentage
        :type progress: float

        :param kwargs: Extra request options

        :return: Response

            **Example:**

            .. code-block:: python

                {
                    'action': 'pause',
                    'progress': 75,

                    'sharing': {
                        'facebook': true,
                        'twitter': true,
                        'tumblr': false
                    },

                    'movie': {
                        'title': 'Guardians of the Galaxy',
                        'year': 2014,

                        'ids': {
                            'trakt': 28,
                            'slug': 'guardians-of-the-galaxy-2014',
                            'imdb': 'tt2015381',
                            'tmdb': 118340
                        }
                    }
                }

        :rtype: dict or None
        """
        return self.action(
            'pause',
            movie, show, episode,
            progress,

            **kwargs
        )

    @application
    @authenticated
    def stop(self, movie=None, show=None, episode=None, progress=0.0, **kwargs):
        """Use this method when the video is stopped or finishes playing on its own. If the
        progress is above 80%, the video will be scrobbled and the :code:`action` will be set
        to **scrobble**.

        If the progress is less than 80%, it will be treated as a *pause* and the :code:`action`
        will be set to **pause**. The playback progress will be saved and :code:`Trakt['sync/playback'].get()`
        can be used to resume the video from this exact position.

        **Note:** If you prefer to use a threshold higher than 80%, you should use :code:`Trakt['scrobble'].pause()`
        yourself so it doesn't create duplicate scrobbles.

        :param movie: Movie definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Guardians of the Galaxy',
                    'year': 2014,

                    'ids': {
                        'tmdb': 118340
                    }
                }

        :type movie: dict or None

        :param show: Show definition

            **Example:**

            .. code-block:: python

                {
                    'title': 'Breaking Bad',
                    'year': 2008,

                    'ids': {
                        'tvdb': 81189
                    }
                }


        :type show: dict or None

        :param episode: Episode definition

            **Example:**

            .. code-block:: python

                {
                    "season": 3,
                    "number": 11
                }

        :type episode: dict or None

        :param progress: Current movie/episode progress percentage
        :type progress: float

        :param kwargs: Extra request options

        :return: Response

            **Example:**

            .. code-block:: python

                {
                    'action': 'scrobble',
                    'progress': 99.9,

                    'sharing': {
                        'facebook': true,
                        'twitter': true,
                        'tumblr': false
                    },

                    'movie': {
                        'title': 'Guardians of the Galaxy',
                        'year': 2014,

                        'ids': {
                            'trakt': 28,
                            'slug': 'guardians-of-the-galaxy-2014',
                            'imdb': 'tt2015381',
                            'tmdb': 118340
                        }
                    }
                }

        :rtype: dict or None
        """
        return self.action(
            'stop',
            movie, show, episode,
            progress,

            **kwargs
        )
