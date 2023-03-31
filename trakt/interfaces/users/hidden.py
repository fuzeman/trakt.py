
import requests

from trakt.core.helpers import dictfilter
from trakt.core.pagination import PaginationIterator
from trakt.interfaces.base import Interface, authenticated
from trakt.mapper.hidden import HiddenItemMapper


class UsersHiddenInterface(Interface):
    path = 'users/hidden/*'
    _valid_sections = ['calendar', 'progress_watched', 'progress_collected', 
                      'recommendations', 'comments']
    _valid_types = ['movie', 'show', 'season', 'user']

    @authenticated
    def get(self, section, type=None, page=None, per_page=None, **kwargs):
        if section not in self._valid_sections:
            raise ValueError(f'Unknown section specified: {section}')
        
        if type and type not in self._valid_types:
            raise ValueError(f'Unknown type specified: {type}')
        
        response = self.http.get(f'/users/hidden/{section}', query={
            'type': type,
            'page': page,
            'limit': per_page
            },
            **dictfilter(kwargs, pop=[
                'authenticated',
                'pagination',
                'validate_token'
            ])
        )

        items = self.get_data(response, **kwargs)

        if isinstance(items, PaginationIterator):
            return items.with_mapper(lambda items: HiddenItemMapper.hidden_items(self.client, items))

        if isinstance(items, requests.Response):
            return items

        return HiddenItemMapper.hidden_items(self.client, items)

    @authenticated
    def add(self, section, items, **kwargs):
        if section not in self._valid_sections:
            raise ValueError(f'Unknown section specified: {section}')
        
        response = self.http.post(f'/users/hidden/{section}',
            data=items,
            **dictfilter(kwargs, pop=[
                'authenticated',
                'validate_token'
            ])
        )

        return self.get_data(response, **kwargs)
        

    @authenticated
    def remove(self, section, items, **kwargs):
        if section not in self._valid_sections:
            raise ValueError(f'Unknown section specified: {section}')

        response = self.http.post(f'/users/hidden/{section}/remove',
            data=items,
            **dictfilter(kwargs, pop=[
                'authenticated',
                'validate_token'
            ])
        )
        
        return self.get_data(response, **kwargs)