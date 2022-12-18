from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

import nested_admin

from .models import TestCase, Test, Answer


class AnswersInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0


class TestInline(nested_admin.NestedStackedInline):
    model = Test
    inlines = AnswersInline,
    extra = 0


class TestCaseForm(forms.ModelForm):

    def clean(self):

        for test_number in range(int(self.data['test_set-TOTAL_FORMS'])):
            answers_count = int(self.data[f'test_set-{test_number}-answer_set-TOTAL_FORMS'])
            is_right_count = 0
            for answer_number in range(answers_count):
                if self.data.get(f'test_set-{test_number}-answer_set-{answer_number}-is_right'):
                    is_right_count += 1
            if is_right_count == 0:
                raise ValidationError('В вопросе "{}" должен быть хотя бы один правильный ответ'.format(
                    self.data[f'test_set-{test_number}-question']
                ))
            if is_right_count == answers_count:
                raise ValidationError('В вопросе "{}" все ответы не могут быть правильными'.format(
                    self.data[f'test_set-{test_number}-question']
                ))


@admin.register(TestCase)
class TestCaseAdmin(nested_admin.NestedModelAdmin):
    model = TestCase
    inlines = TestInline,
    form = TestCaseForm

