from trakt import Trakt
import logging
import os


class Application(object):
    def login(self):
        # Request new device code
        code = Trakt['oauth/device'].code()

        print 'Enter the code "%s" at %s to authenticate your account' % (
            code.get('user_code'),
            code.get('verification_url')
        )

        # Construct device authentication poller
        poller = Trakt['oauth/device'].poll(**code)\
            .on('aborted', self.on_aborted)\
            .on('authenticated', self.on_authenticated)\
            .on('expired', self.on_expired)\
            .on('poll', self.on_poll)

        # Start polling for authentication token
        poller.start(daemon=False)

    def on_aborted(self):
        """Triggered when device authentication was aborted (either with `DeviceOAuthPoller.stop()`
           or via the "poll" event)"""

        print 'Authentication aborted'

    def on_authenticated(self, token):
        """Triggered when device authentication has been completed

        :param token: Authentication token details
        :type token: dict
        """

        print 'Authentication complete: %r' % token

    def on_expired(self):
        """Triggered when the device authentication code has expired"""

        print 'Authentication expired'

    def on_poll(self, callback):
        """Triggered before each poll

        :param callback: Call with `True` to continue polling, or `False` to abort polling
        :type callback: func
        """

        # Continue polling
        callback(True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Configure
    Trakt.base_url = 'http://api.staging.trakt.tv'

    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    app = Application()
    app.login()
