from django.shortcuts import render
from django.contrib import messages
from .models import About
from .forms import CollaborateForm


def about_me(request):
    """
    Render the About page and handle collaboration form submissions.

    This view retrieves the most recently updated About object and
    displays it on the "about/about.html" template. If a POST request
    is received, it processes the CollaborateForm. When the form is
    valid, it saves the submission and shows a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered About page with About content and
        collaboration form.
    """
    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Collaboration request received! I endeavour to respond within 2 working days."
            )

    about = About.objects.all().order_by('-updated_on').first()
    collaborate_form = CollaborateForm()

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form
        },
    )
