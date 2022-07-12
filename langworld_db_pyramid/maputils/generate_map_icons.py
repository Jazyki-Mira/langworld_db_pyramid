from clldutils import svg

COLORS = [
    'a6cee3',
    '1f78b4',
    'b2df8a',
    '33a02c',
    'fb9a99',
    'e31a1c',
    'fdbf6f',
    'ff7f00',
    'cab2d6',
    '6a3d9a',
    'ffff99',
    'b15928'
]

SHAPES = ('c', 's', 't', 'd', 'f')


def generate_map_icons():
    count = 0

    for shape in SHAPES:
        for color in COLORS:
            if count > 60:
                raise ValueError(f'Cannot generate more than 60 different markers')
            icon = svg.icon(f'{shape}{color}')
            yield {'icon': icon, 'data_url': svg.data_url(icon)}
            count += 1
            # TODO test if I decide to use this
