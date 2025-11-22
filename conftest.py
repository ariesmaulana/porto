import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from project.models import Project


@pytest.fixture
def sample_image():
    """Create a simple test image."""
    return SimpleUploadedFile(
        name="test_image.jpg",
        content=b"fake image content",
        content_type="image/jpeg",
    )


@pytest.fixture
def create_project(db, sample_image):
    """Factory fixture to create projects."""

    def _create_project(**kwargs):
        defaults = {
            "title": "Test Project",
            "category": "WEB_DEV",
            "short_summary": "A test project summary",
            "role": "Developer",
            "year": 2024,
            "stack": "Python Django PostgreSQL",
            "repository": "https://github.com/test/repo",
            "challenge": "Test challenge description",
            "key_features": "Feature 1, Feature 2",
            "description": "Detailed project description",
            "image": sample_image,
        }
        defaults.update(kwargs)
        return Project.objects.create(**defaults)

    return _create_project


@pytest.fixture
def web_dev_project(create_project):
    """Create a web development project."""
    return create_project(
        title="Web Dev Project",
        category="WEB_DEV",
        year=2024,
    )


@pytest.fixture
def sys_design_project(create_project):
    """Create a system design project."""
    return create_project(
        title="System Design Project",
        category="SYS_DESIGN",
        year=2023,
    )


@pytest.fixture
def talk_project(create_project):
    """Create a talk project."""
    return create_project(
        title="Tech Talk",
        category="TALK",
        year=2022,
    )
