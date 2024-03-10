from django.http import HttpResponse

from .models import User


def activate_email(request):
    id = request.GET.get("id", "")
    email = request.GET.get("email", "")

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
        return HttpResponse(
            "The user is now activated. You can go ahead and log in.",
        )
    return HttpResponse("The parameters is not valid.")
