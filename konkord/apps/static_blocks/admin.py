from django.contrib import admin
from .models import StaticBlock
from modeltranslation.admin import TabbedTranslationAdmin
from .forms import StaticBlockForm


@admin.register(StaticBlock)
class StaticBlockAdmin(TabbedTranslationAdmin):
    form = StaticBlockForm
