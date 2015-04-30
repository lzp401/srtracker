__author__ = 'victorlu'

ASC = 'asc'
DESC = 'desc'


class FilterType:

    def __init__(self):
        pass

    CONTAINS = {
        'label': 'Contains',
        'suffix': '__contains'
    }

    IN = {
        'label': 'In',
        'suffix': '__in'
    }

    FROM_TO = (
        {
            'label': 'From',
            'suffix': '__gte'
        },
        {
            'label': 'To',
            'suffix': '__lte'
        }
    )

    IS = {
        'label': 'Is',
        'suffix': ''
    }