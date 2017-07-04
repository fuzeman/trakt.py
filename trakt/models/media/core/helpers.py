IDENTIFIERS = {
    'movie': [
        'imdb',
        'tmdb',

        'slug',
        'trakt'
    ],
    'show': [
        'tvdb',
        'tmdb',
        'imdb',
        'tvrage',

        'slug',
        'trakt'
    ],
    'season': [
        'tvdb',
        'tmdb',

        'trakt'
    ],
    'episode': [
        'tvdb',
        'tmdb',
        'imdb',
        'tvrage',

        'trakt'
    ],
    'custom_list': [
        'trakt',
        'slug'
    ],
    'person': [
        'tmdb',
        'imdb',
        'tvrage',

        'slug',
        'trakt'
    ]
}


def build_keys(media_type, ids):
    if media_type not in IDENTIFIERS:
        raise NotImplementedError('Unsupported media type: %s' % (media_type,))

    if not ids:
        return []

    keys = []

    for key in IDENTIFIERS[media_type]:
        value = ids.get(key)

        if not value:
            continue

        keys.append((key, str(value)))

    if not len(keys):
        return []

    return keys
