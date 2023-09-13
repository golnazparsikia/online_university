from django.middleware.csrf import CsrfViewMiddleware
from django.core import signing
from kernel.settings import config


class RenameCSRFTokenMiddleware(CsrfViewMiddleware):
    """
    Middleware to rename the CSRF token field in both request and response.
    Inherits from Django's CsrfViewMiddleware.
    """
    BLANK = ''

    def process_response(self, request, response):
        """
        Process the response and replace the CSRF token field name in the response content.

        Args:
            request (HttpRequest): The request object.
            response (HttpResponse): The response object.

        Returns:
            HttpResponse: The modified response object with the CSRF token field name replaced.
        """
        csrf_cookie_name = 'csrftoken'
        csrf_token_name = config.get_value('security.csrf', 'CSRF_TOKEN_NAME')

        if self._should_replace_csrf_token(request, response, csrf_cookie_name):
            response.content = response.content.replace(
                f'name="csrfmiddlewaretoken"'.encode(),
                f'name="{csrf_token_name}"'.encode()
            )

        return response

    def __call__(self, request):
        """
        Process the request and create a new CSRF token if it's not present in the POST data.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object after processing the request.
        """
        csrf_token_name = config.get_value('security.csrf', 'CSRF_TOKEN_NAME')
        content_type = request.META.get('CONTENT_TYPE', '').lower()
        # Only process the request if it's a POST request and there are no files being uploaded
        if request.method == "POST" and not content_type.startswith('multipart/form-data'):
            request = self.make_request_post_mutable(request)
            csrf_token = request.POST.get(csrf_token_name, self.BLANK)

            if csrf_token == self.BLANK:
                request = self.create_token(request)
                request = self.make_request_post_immutable(request)

        response = self.get_response(request)
        return response

    def make_request_post_mutable(self, request):
        """
        Make the request.POST mutable if it's not already.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpRequest: The modified request object with mutable POST data.
        """
        if not request.POST._mutable:
            request.POST._mutable = True
        return request

    def make_request_post_immutable(self, request):
        """
        Make the request.POST immutable.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpRequest: The modified request object with immutable POST data.
        """
        request.POST._mutable = False
        return request

    def create_token(self, request):
        """
        Create a new CSRF token in the request.POST data.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpRequest: The modified request object with the new CSRF token.
        """
        csrf_token_name = config.get_value('security.csrf', 'CSRF_TOKEN_NAME')
        csrf_field = signing.dumps(csrf_token_name).partition(':')[0]
        request_csrf_token = request.POST.get(csrf_field, self.BLANK)
        request.POST[csrf_token_name] = request_csrf_token
        return request

    def _should_replace_csrf_token(self, request, response, csrf_cookie_name):
        """
        Determine if the CSRF token field name should be replaced in the response content.

        Args:
            request (HttpRequest): The request object.
            response (HttpResponse): The response object.
            csrf_cookie_name (str): The CSRF cookie name.

        Returns:
            bool: True if the CSRF token field name should be replaced, False otherwise.
        """
        return (
            hasattr(response, 'content') and
            'text/html' in response.get('Content-Type', '') and
            csrf_cookie_name in request.META.get('HTTP_COOKIE', '')
        )
