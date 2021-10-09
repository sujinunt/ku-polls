"""Admin panel class."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """Choice show."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Show fieldsets on question panel."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
