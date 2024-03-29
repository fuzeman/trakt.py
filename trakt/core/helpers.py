

import functools
import logging
import warnings

try:
    import arrow
except ImportError:
    arrow = None

log = logging.getLogger(__name__)


def clean_username(username):
    if not username:
        return username

    return username.replace('.', '-')


def deprecated(message):
    def wrap(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)

            return func(self, *args, **kwargs)

        return wrapped

    return wrap


def dictfilter(d, **kwargs):
    result = {}

    if 'get' in kwargs:
        for key in kwargs['get']:
            value = d.get(key, None)

            if value is not None:
                result[key] = value

    if 'pop' in kwargs:
        for key in kwargs['pop']:
            value = d.pop(key, None)

            if value is not None:
                result[key] = value

    return result


def synchronized(f_lock, mode='full'):
    if mode == 'full':
        mode = ['acquire', 'release']
    elif isinstance(mode, str):
        mode = [mode]

    def wrap(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            lock = f_lock(self)

            def acquire():
                if 'acquire' not in mode:
                    return

                lock.acquire()

            def release():
                if 'release' not in mode:
                    return

                lock.release()

            # Acquire the lock
            acquire()

            try:
                # Execute wrapped function
                result = func(self, *args, **kwargs)
            finally:
                # Release the lock
                release()

            # Return the result
            return result

        return wrapped

    return wrap


def try_convert(value, value_type, default=None):
    try:
        return value_type(value)
    except (ValueError, TypeError):
        return default


def reraise(tp, value, tb=None):
    try:
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None
        tb = None
#
# Date/Time Conversion
#


@deprecated('`from_iso8601(value)` has been renamed to `from_iso8601_datetime(value)`')
def from_iso8601(value):
    return from_iso8601_datetime(value)


def from_iso8601_date(value):
    if value is None:
        return None

    if arrow is None:
        raise Exception('"arrow" module is not available')

    # Parse ISO8601 datetime
    dt = arrow.get(value, 'YYYY-MM-DD')

    # Return date object
    return dt.date()


def from_iso8601_datetime(value):
    if value is None:
        return None

    if arrow is None:
        raise Exception('"arrow" module is not available')

    # Parse ISO8601 datetime
    dt = arrow.get(value, 'YYYY-MM-DDTHH:mm:ss.SZZ')

    # Convert to UTC
    dt = dt.to('UTC')

    # Return datetime object
    return dt.datetime


@deprecated('`to_iso8601(value)` has been renamed to `to_iso8601_datetime(value)`')
def to_iso8601(value):
    return to_iso8601_datetime(value)


def to_iso8601_date(value):
    if value is None:
        return None

    return value.strftime('%Y-%m-%d')


def to_iso8601_datetime(value):
    if value is None:
        return None

    return value.strftime('%Y-%m-%dT%H:%M:%S') + '.000-00:00'
