from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class RegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
                not (
                        request.path.startswith('/api/') or
                        request.path.startswith('/__debug__/') or

                        # გამოვრიცხოთ ყველა გვერდი რომელიც იწყება admin:index-ით
                        request.path.startswith(reverse('admin:index')[:-1]) or

                        request.path in (  # გამოვრიცხოთ ეს ყველა გვერდი
                                reverse_lazy('frontend:authentication:register_fully'),
                                reverse_lazy('frontend:authentication:logout'),
                        )
                ) and
                request.user.is_authenticated and
                not request.user.is_fully_registered
        ):
            return redirect('frontend:authentication:register_fully')

        return self.get_response(request)
