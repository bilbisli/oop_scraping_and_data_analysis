

class BasePageHandler():
    """Parent class of all concrete handlers"""
 
    def __init__(self, nxt, locators):
        """change or increase the local variable using nxt"""
 
        self._nxt = nxt
        self.locators = locators
 
    def handle(self, request):
        """It calls the processRequest through given request"""
 
        handled = self.processRequest(request)
        """case when it is not handled"""
 
        if not handled:
            if self._nxt is None:
                return None
            return self._nxt.handle(request)
        return self.locators
 
    def processRequest(self, request):
        """throws a NotImplementedError"""

        raise NotImplementedError('Implement how handler deals with a request.')
