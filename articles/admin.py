from django.contrib import admin
from .models import Article, Tag, TagScope
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


class MainInlineFormset(BaseInlineFormSet):
    def check_errors(self):
        if self.is_main_counter > 1:
            raise ValidationError('Основным может быть только один раздел.')
        if self.is_main_counter == 0:
            raise ValidationError('Укажите основной раздел')

    def clean(self):
        self.is_main_counter = 0
        for form in self.forms:
            form_data = form.cleaned_data
            if form_data and form_data['is_main']:
                self.is_main_counter += 1
        self.check_errors()
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = TagScope
    formset = MainInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]