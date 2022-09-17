class BasePageHandler(object):
    """
    Parent class of all concrete web page handlers (based on Chain of Responsibility DP)
    Note:
        Used when there are web pages of the same underlying subject (such as article) where the elements and values of
        the pages are the same (title, author, time, content etc.) but different locators are needed since the
        formatting of the pages themselves vary (structure of html is different)
    """

    def __init__(self, nxt, locators):
        """change or increase the local variable using nxt"""
        self._nxt = nxt
        self.locators = locators

    def handle(self, request):
        """Methode calls the processRequest through given request"""
        handled = self.process_request(request)
        """case when it is not handled"""
        if not handled:
            if self._nxt is None:
                return None
            return self._nxt.handle(request)
        """case when it is handled"""
        return self.locators

    def process_request(self, request):
        """throws a NotImplementedError"""
        raise NotImplementedError('Implement how handler deals with a request.')
