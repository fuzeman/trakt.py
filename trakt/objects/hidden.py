
from trakt.core.helpers import from_iso8601_datetime, to_iso8601_datetime

class HiddenItem(object):
    """
    Base object for hidden items
    """
   
    hidden_type = None
    """
    :type: :class:`~python:str`

    The type of hidden item (:code:`movie`, :code:`show`, :code:`season`, :code:`user`)
    """
    
    def __init__(self, client, hidden_at=None, hidden_type=None, hidden_item=None):
        self._client = client

        self.hidden_at = hidden_at
        """
        :type: :class:`~python:datetime.datetime`

        When the item was hidden
        """

        self.hidden_item = hidden_item
        self.hidden_type = hidden_type
        
    
    def to_dict(self):
        result = {
            'hidden_at': to_iso8601_datetime(self.hidden_at),
            'type': self.hidden_type
        }

        if self.hidden_item:
            result[self.hidden_type] = self.hidden_item.to_dict()
        
        return result

    def _update(self, info=None, **kwargs):
        if not info:
            return

        if 'hidden_at' in info:
            self.hidden_at = from_iso8601_datetime(info.get('hidden_at'))
        if 'type' in info:
            self.hidden_type = info.get('type')
        if self.hidden_type in info:
            self.hidden_item = self._client.construct(self.hidden_type, info[self.hidden_type])

    @classmethod
    def _construct(cls, client, info=None, **kwargs):
        if not info:
            return
        hidden = cls(client)
        hidden._update(info, **kwargs)

        return hidden

class HiddenShow(HiddenItem):
    """
    A hidden show

    Shows can be hidden in the :code:`calendar`, :code:`progress_watched`, :code:`progress_collected`, 
    and :code:`recommendations` sections
    """
    hidden_type = 'show'


class HiddenMovie(HiddenItem):
    """
    A hidden movie

    Movies can be hidden in the :code:`calendar` and :code:`recommendations` sections
    """
    hidden_type = 'movie'


class HiddenSeason(HiddenItem):
    """
    A hidden season

    Seasons can be hidden in the :code:`progress_watched`, and :code:`progress_collected` sections
    """
    hidden_type = 'season'

    def to_dict(self):
        result = super(HiddenSeason, self).to_dict()
        if self.show:
            result['show'] = self.show.to_dict()
        return result
    
    def _update(self, info=None, **kwargs):
        super(HiddenSeason, self)._update(info, **kwargs)

        if 'show' in info:
            self.show = self._client.construct('show', info['show'])

class HiddenUser(HiddenItem):
    """
    A hidden user

    Users can be hidden in te :code:`comments` section
    """
    hidden_type = 'user'