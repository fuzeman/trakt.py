from trakt.interfaces.base import Interface, authenticated, application

__all__ = [
    'MoviesInterface'
]

class MoviesInterface(Interface):
    path = 'movies'

    @application
    @authenticated
    def get(self, id):
        response = self.http.get(
            path=id
        )

        return self.get_data(response)

