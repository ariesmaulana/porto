import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import PROJECT_CATEGORIES, Project


def home(request: HttpRequest) -> HttpResponse:
    tech_stack = [
        "GOLANG",
        "PYTHON",
        "POSTGRESQL",
        "DOCKER",
        "REDIS",
        "SYSTEM DESIGN",
        "CI/CD",
        "PHP",
    ]
    featured_projects = Project.objects.filter(id__in=[1, 2])

    context = {
        "tech_stack": tech_stack,
        "featured_projects": featured_projects,
    }
    return render(request, "pages/home.html", context)


def project_list(request: HttpRequest) -> HttpResponse:
    category_filter = request.GET.get("category")
    if category_filter and category_filter != "all":
        projects = Project.objects.filter(category=category_filter)
    else:
        projects = Project.objects.all()

    # Get all unique categories from all projects, regardless of current filter

    projects_data = []
    for project in projects:
        projects_data.append(
            {
                "id": project.id,
                "title": project.title,
                "category": project.category,
                "year": project.year,
                "short_summary": project.short_summary,
                "tags": project.stack.split(),
            }
        )

    context = {
        "projects": projects,
        "projects_json": json.dumps(projects_data),
        "categories": PROJECT_CATEGORIES,
        "current_filter": category_filter or "all",
    }
    Project.objects.all()
    return render(request, "pages/projects.html", context)


def project_detail(request: HttpRequest, pk: int) -> HttpResponse:
    project = get_object_or_404(Project, pk=pk)

    context = {
        "project": project,
    }
    return render(request, "pages/project_detail.html", context)
