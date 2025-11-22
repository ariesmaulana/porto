from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "role")
    list_filter = ("category", "year")
    search_fields = ("title", "short_summary", "description")

    fieldsets = (
        ("Basic Information", {"fields": ("title", "category", "year", "role")}),
        (
            "Summary",
            {
                "fields": ("short_summary",),
                "description": "Brief description shown on project listing page",
            },
        ),
        (
            "Technical Details",
            {
                "fields": ("stack", "repository"),
                "description": "Stack: Comma-separated technologies (e.g., PYTHON, AWS, TERRAFORM)",
            },
        ),
        (
            "Detailed Content",
            {
                "fields": ("description", "challenge", "key_features"),
                "description": "Full project details for the detail page",
            },
        ),
        (
            "Media",
            {"fields": ("image",), "description": "Project thumbnail/hero image"},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        # Make created/updated fields readonly if they exist
        return []
