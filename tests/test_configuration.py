from trakt.core.configuration import ConfigurationManager
from tests.core.semaphore import Semaphore

from threading import Thread
import threading
import time
import uuid


def test_threaded():
    id = uuid.uuid4()
    lock = Semaphore(value=0)

    configuration = ConfigurationManager()
    results = {}

    def test(key):
        with configuration.app(name='%s-test' % key):
            # Wait for signal
            lock.acquire()

            with configuration.app(version='%s-1.0' % key):
                results[threading.current_thread().name] = {
                    'app.name': configuration.get('app.name'),
                    'app.version': configuration.get('app.version')
                }

    one = Thread(target=test, name='%s.one' % id, args=(1, ))
    two = Thread(target=test, name='%s.two' % id, args=(2, ))

    one.start()
    two.start()

    # Wait for threads to properly startup
    time.sleep(1)

    # Wake up threads
    lock.release_multi(2)

    # Wait for threads to finish
    one.join()
    two.join()

    # Test results
    assert results['%s.one' % id] == {
        'app.name': '1-test',
        'app.version': '1-1.0',
    }

    assert results['%s.two' % id] == {
        'app.name': '2-test',
        'app.version': '2-1.0',
    }

    assert len(configuration.stack._threads) == 0
