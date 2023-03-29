

from trakt.mapper.core.base import Mapper


class HiddenItemMapper(Mapper):
    @classmethod
    def hidden_items(cls, client, items, **kwargs):
        if not items:
            return None

        return [item for item in [cls.hidden_item(client, item, **kwargs) for item in items] if item]

    @classmethod
    def hidden_item(cls, client, item, **kwargs):
        if not item:
            return None

        # Create object
        hidden_item = cls.construct(client, f'hidden_{item["type"]}', item, **kwargs)

        # Update with root info
        if 'hidden_item' in item:
            hidden_item._update(item)

        return hidden_item
