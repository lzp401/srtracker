__author__ = 'victorlu'

'''
A support file for views
'''

from django.http.request import QueryDict


class ColumnHeader:
    def __init__(self, name, link):
            self.name = name
            self.link = link
            self.show_caret = False
            self.caret_style = ''
            self.order = None

    def __str__(self):
        return self.name


class UrlHelper:
    def __init__(self):
        pass


    @staticmethod
    def format_params(query_dict):
        return '&'.join(['{0}={1}'.format(key, val) for key, val in query_dict.iteritems()])


    @staticmethod
    def update_params(param_str, **kwargs):
        query_dict = QueryDict(param_str, True)

        for key, val in kwargs.iteritems():
            if val:
                query_dict[key] = val
            else:
                query_dict.pop(key) if query_dict.has_key(key) else None

        return UrlHelper.format_params(query_dict)


    @staticmethod
    def format_dict(param_str):
        return QueryDict(param_str).copy()


    @staticmethod
    def to_url(param_str):
        return '?{0}'.format(param_str) if len(param_str) > 0 else ''