from trakt.core.context_collection import ListCollection, ContextCollection


def test_list_collection():
    m = ListCollection(
        lambda: [1, 2, 3],
        [4, 5, 6]
    )

    assert len(m) == 6

    assert 1 in m
    assert 10 not in m

    assert m[0] == 1
    assert m[-1] == 6

    m[4] = 9
    assert m[4] == 9


def test_context_collection():
    o = ContextCollection(
        ['base']
    )

    o.append('child-1')

    assert o.current == ['base', 'child-1']
    assert o[0] == 'base'
    assert o[-1] == 'child-1'

    o.append('child-2')
    assert o.current == ['base', 'child-1', 'child-2']
    assert o[-1] == 'child-2'

    o.pop()
    assert o.current == ['base', 'child-1']
    assert o[-1] == 'child-1'
