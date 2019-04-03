class StubSiteMiddleware:
    """ Even though wagtail site middleware is not useful for this service,
    wagtail expects `request.site` to be present - so we populate it with None
    """

    def process_request(self, request):
        request.site = None
