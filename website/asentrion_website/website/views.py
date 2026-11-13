from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .email import (
    send_collaboration_confirmation,
    send_project_confirmation,
)


def home(request):

    return render(
        request,
        "website/index.html",
    )


def portfolio(request):

    return render(
        request,
        "website/portfolio.html",
    )


def get_started(request):

    if request.method != "POST":

        return redirect(
            f"{reverse('home')}#contact"
        )


    data = {
        "full_name": request.POST.get("full_name"),
        "organization": request.POST.get("organization"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "service": request.POST.get("service"),
        "preferred_contact": request.POST.get(
            "preferred_contact"
        ),
        "timeline": request.POST.get("timeline"),
        "budget": request.POST.get("budget"),
        "details": request.POST.get("details"),
    }


    sent = send_project_confirmation(data)

    print(
        f"[ASENTRION] Project confirmation result: {sent}"
    )


    return redirect(
        f"{reverse('home')}?submitted=project#contact"
    )


def collaborate(request):

    if request.method != "POST":

        return redirect(
            f"{reverse('home')}#collaborate"
        )


    data = {
        "full_name": request.POST.get("full_name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "location": request.POST.get("location"),
        "current_role": request.POST.get("current_role"),
        "experience_level": request.POST.get(
            "experience_level"
        ),
        "primary_focus": request.POST.get(
            "primary_focus"
        ),

        "areas_of_interest": request.POST.getlist(
            "areas_of_interest"
        ),

        "github": request.POST.get("github"),
        "portfolio_url": request.POST.get(
            "portfolio_url"
        ),
        "resume_url": request.POST.get(
            "resume_url"
        ),
        "availability": request.POST.get(
            "availability"
        ),
        "introduction": request.POST.get(
            "introduction"
        ),
        "collaboration_fit": request.POST.get(
            "collaboration_fit"
        ),
    }


    sent = send_collaboration_confirmation(data)

    print(
        f"[ASENTRION] Collaboration confirmation result: {sent}"
    )


    return redirect(
        f"{reverse('home')}?submitted=collaboration#collaborate"
    )


def public_logo(request):

    logo_path = finders.find(
        "website/images/asentrion-3.png"
    )

    if not logo_path:
        raise Http404("Logo not found")


    response = FileResponse(
        open(logo_path, "rb"),
        content_type="image/png",
    )

    response["Cache-Control"] = (
        "public, max-age=86400"
    )

    return response