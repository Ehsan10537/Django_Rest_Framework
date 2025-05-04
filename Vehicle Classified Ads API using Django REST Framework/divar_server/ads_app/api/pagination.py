from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CarAdListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'       # it's default to 'page' itself.
    page_size_query_param = 'size'  # user can override the page_size in the url using 'size' parameter if needed
    max_page_size = 5               # to restrict the user 
    last_page_strings = ('end',)      # it's default to ('last',). you can use ?page=end to visit the last page

# -------------------------------------------------------------

class MotorcycleAdPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 4
    limit_query_param = 'limit'    # it's default to 'limit' itself
    offset_query_param = 'start'   # it's default to 'offset' itself

    # limit is basically the page size
    # offset is
    # you can use the limit and offset(in this case start) parameters to specify them.
    # offset sets to 0 by default at the beginning
    # offset is the number of records you want to skip in the order before selecting records
    # you specify the limit and offset like this example in the url /?limit=3&start=0
    # offset=0 means skip no records and start from the first element in the order