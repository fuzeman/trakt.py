from trakt.interfaces.base import Interface, authenticated, application

__all__ = [
    'ShowsInterface'
]

class ShowsInterface(Interface):
    path = 'shows'


    @application
    @authenticated
    def get(self, id):
        response = self.http.get(
            path=str(id)
        )

        return self.get_data(response)

    @application
    @authenticated
    def seasons(self, id):
        response = self.http.get(
            path=str(id)+'/seasons'
        )

        return self.get_data(response)

    @application
    @authenticated
    def season(self, id, season):
        response = self.http.get(
            path=str(id)+'/seasons/'+str(season)
        )

        return self.get_data(response)

    @application
    @authenticated
    def episode(self, id, season, episode):
        response = self.http.get(
            path=str(id)+'/seasons/'+str(season)+'/episodes/'+str(episode)
        )

        return self.get_data(response)
