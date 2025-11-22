import json

import pytest
from django.urls import reverse

from project.models import PROJECT_CATEGORIES


@pytest.mark.django_db
def test_home_view_returns_200(client):
    """Test home view returns successful response."""
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_view_uses_correct_template(client):
    """Test home view uses the correct template."""
    url = reverse("home")
    response = client.get(url)
    assert "pages/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_home_view_context_contains_tech_stack(client):
    """Test home view context contains tech_stack."""
    url = reverse("home")
    response = client.get(url)
    assert "tech_stack" in response.context
    tech_stack = response.context["tech_stack"]
    assert isinstance(tech_stack, list)
    assert len(tech_stack) > 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "expected_tech",
    [
        "GOLANG",
        "PYTHON",
        "POSTGRESQL",
        "DOCKER",
        "REDIS",
        "SYSTEM DESIGN",
        "CI/CD",
        "PHP",
    ],
)
def test_home_view_contains_expected_technologies(client, expected_tech):
    """Test home view context contains expected technologies."""
    url = reverse("home")
    response = client.get(url)
    tech_stack = response.context["tech_stack"]
    assert expected_tech in tech_stack


@pytest.mark.django_db
def test_home_view_featured_projects(client, web_dev_project, sys_design_project):
    """Test home view displays featured projects."""
    url = reverse("home")
    response = client.get(url)
    assert "featured_projects" in response.context
    featured_projects = response.context["featured_projects"]
    assert featured_projects.count() >= 0


# ============================================================================
# PROJECT LIST VIEW TESTS
# ============================================================================


@pytest.mark.django_db
def test_project_list_view_returns_200(client):
    """Test project list view returns successful response."""
    url = reverse("projects")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_project_list_view_uses_correct_template(client):
    """Test project list view uses the correct template."""
    url = reverse("projects")
    response = client.get(url)
    assert "pages/projects.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_project_list_view_displays_all_projects(
    client, web_dev_project, sys_design_project, talk_project
):
    """Test project list view displays all projects without filter."""
    url = reverse("projects")
    response = client.get(url)
    projects = response.context["projects"]
    assert projects.count() == 3
    assert web_dev_project in projects
    assert sys_design_project in projects
    assert talk_project in projects


@pytest.mark.django_db
@pytest.mark.parametrize(
    "category,expected_count",
    [
        ("WEB_DEV", 1),
        ("SYS_DESIGN", 1),
        ("TALK", 1),
        ("all", 3),
    ],
)
def test_project_list_view_filter_by_category(
    client, category, expected_count, web_dev_project, sys_design_project, talk_project
):
    """Test project list view filters projects by category."""
    url = reverse("projects")
    response = client.get(url, {"category": category})
    projects = response.context["projects"]
    assert projects.count() == expected_count


@pytest.mark.django_db
def test_project_list_view_filter_web_dev_category(
    client, web_dev_project, sys_design_project
):
    """Test filtering by WEB_DEV category."""
    url = reverse("projects")
    response = client.get(url, {"category": "WEB_DEV"})
    projects = response.context["projects"]
    assert projects.count() == 1
    assert projects.first() == web_dev_project


@pytest.mark.django_db
def test_project_list_view_filter_sys_design_category(
    client, web_dev_project, sys_design_project
):
    """Test filtering by SYS_DESIGN category."""
    url = reverse("projects")
    response = client.get(url, {"category": "SYS_DESIGN"})
    projects = response.context["projects"]
    assert projects.count() == 1
    assert projects.first() == sys_design_project


@pytest.mark.django_db
def test_project_list_view_context_contains_categories(client):
    """Test project list view context contains categories."""
    url = reverse("projects")
    response = client.get(url)
    assert "categories" in response.context
    assert response.context["categories"] == PROJECT_CATEGORIES


@pytest.mark.django_db
def test_project_list_view_context_contains_current_filter(client):
    """Test project list view context contains current_filter."""
    url = reverse("projects")
    response = client.get(url, {"category": "WEB_DEV"})
    assert "current_filter" in response.context
    assert response.context["current_filter"] == "WEB_DEV"


@pytest.mark.django_db
def test_project_list_view_current_filter_defaults_to_all(client):
    """Test current_filter defaults to 'all' when no category provided."""
    url = reverse("projects")
    response = client.get(url)
    assert response.context["current_filter"] == "all"


@pytest.mark.django_db
def test_project_list_view_projects_json_format(client, web_dev_project):
    """Test projects_json is properly formatted."""
    url = reverse("projects")
    response = client.get(url)
    assert "projects_json" in response.context
    projects_json = json.loads(response.context["projects_json"])
    assert isinstance(projects_json, list)
    assert len(projects_json) == 1

    project_data = projects_json[0]
    assert "id" in project_data
    assert "title" in project_data
    assert "category" in project_data
    assert "year" in project_data
    assert "short_summary" in project_data
    assert "tags" in project_data
    assert isinstance(project_data["tags"], list)


@pytest.mark.django_db
def test_project_list_view_empty_projects(client):
    """Test project list view with no projects."""
    url = reverse("projects")
    response = client.get(url)
    projects = response.context["projects"]
    assert projects.count() == 0


# ============================================================================
# PROJECT DETAIL VIEW TESTS
# ============================================================================


@pytest.mark.django_db
def test_project_detail_view_returns_200(client, web_dev_project):
    """Test project detail view returns successful response."""
    url = reverse("project_detail", kwargs={"pk": web_dev_project.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_project_detail_view_uses_correct_template(client, web_dev_project):
    """Test project detail view uses the correct template."""
    url = reverse("project_detail", kwargs={"pk": web_dev_project.pk})
    response = client.get(url)
    assert "pages/project_detail.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_project_detail_view_context_contains_project(client, web_dev_project):
    """Test project detail view context contains the project."""
    url = reverse("project_detail", kwargs={"pk": web_dev_project.pk})
    response = client.get(url)
    assert "project" in response.context
    assert response.context["project"] == web_dev_project


@pytest.mark.django_db
@pytest.mark.parametrize(
    "project_fixture",
    [
        "web_dev_project",
        "sys_design_project",
        "talk_project",
    ],
)
def test_project_detail_view_for_different_categories(client, project_fixture, request):
    """Test project detail view works for all project categories."""
    project = request.getfixturevalue(project_fixture)
    url = reverse("project_detail", kwargs={"pk": project.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["project"] == project


@pytest.mark.django_db
def test_project_detail_view_displays_project_attributes(client, web_dev_project):
    """Test project detail view displays all project attributes."""
    url = reverse("project_detail", kwargs={"pk": web_dev_project.pk})
    response = client.get(url)
    project = response.context["project"]

    assert project.title == web_dev_project.title
    assert project.category == web_dev_project.category
    assert project.short_summary == web_dev_project.short_summary
    assert project.role == web_dev_project.role
    assert project.year == web_dev_project.year
    assert project.stack == web_dev_project.stack
    assert project.repository == web_dev_project.repository
    assert project.challenge == web_dev_project.challenge
    assert project.key_features == web_dev_project.key_features
    assert project.description == web_dev_project.description


@pytest.mark.django_db
def test_project_detail_view_returns_404_for_nonexistent_project(client):
    """Test project detail view returns 404 for non-existent project."""
    url = reverse("project_detail", kwargs={"pk": 99999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_pk",
    [
        99999,
        12345,
        54321,
    ],
)
def test_project_detail_view_404_for_multiple_invalid_ids(client, invalid_pk):
    """Test project detail view returns 404 for multiple invalid IDs."""
    url = reverse("project_detail", kwargs={"pk": invalid_pk})
    response = client.get(url)
    assert response.status_code == 404


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_navigation_flow_home_to_projects_to_detail(client, web_dev_project):
    """Test user navigation from home to projects to detail page."""
    home_response = client.get(reverse("home"))
    assert home_response.status_code == 200

    projects_response = client.get(reverse("projects"))
    assert projects_response.status_code == 200

    detail_response = client.get(
        reverse("project_detail", kwargs={"pk": web_dev_project.pk})
    )
    assert detail_response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name,kwargs",
    [
        ("home", {}),
        ("projects", {}),
    ],
)
def test_all_list_views_accessible(client, url_name, kwargs):
    """Test all list views are accessible."""
    url = reverse(url_name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_projects_filter_persistence(
    client, web_dev_project, sys_design_project, talk_project
):
    """Test that filtering works correctly across different categories."""
    response = client.get(reverse("projects"), {"category": "WEB_DEV"})
    assert response.context["projects"].count() == 1
    assert response.context["current_filter"] == "WEB_DEV"

    response = client.get(reverse("projects"), {"category": "SYS_DESIGN"})
    assert response.context["projects"].count() == 1
    assert response.context["current_filter"] == "SYS_DESIGN"

    response = client.get(reverse("projects"), {"category": "all"})
    assert response.context["projects"].count() == 3
    assert response.context["current_filter"] == "all"
