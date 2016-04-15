import logging

from trakt.core.helpers import try_convert

log = logging.getLogger(__name__)


class PaginationIterator(object):
    def __init__(self, client, response):
        self.client = client
        self.response = response

        # Retrieve pagination headers
        self.per_page = try_convert(response.headers.get('x-pagination-limit'), int)
        self.total_items = try_convert(response.headers.get('x-pagination-item-count'), int)
        self.total_pages = try_convert(response.headers.get('x-pagination-page-count'), int)

    def fetch(self, page, per_page=None):
        if page == 1:
            return self.response

        if per_page is None:
            per_page = self.per_page or 10

        # Construct parameters
        params = {}

        if page != 1:
            params['page'] = page

        if per_page != 10:
            params['limit'] = per_page

        # Construct request
        request = self.response.request.copy()
        request.prepare_url(request.url, params)

        # Send request
        return self.client.http.send(request)

    def get(self, page):
        response = self.fetch(page)

        # Parse response, return data
        content_type = response.headers.get('content-type')

        if content_type and content_type.startswith('application/json'):
            # Try parse json response
            try:
                data = response.json()
            except Exception as e:
                log.warning('unable to parse JSON response: %s', e)
                return None
        else:
            log.debug('response returned content-type: %r, falling back to raw data', content_type)

            # Fallback to raw content
            data = response.content

        return data

    def __iter__(self):
        current = 1

        while current <= self.total_pages:
            for item in self.get(current):
                yield item

            current += 1
