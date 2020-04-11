from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML

from .models import Question, Answer


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'category', 'content',)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "py-4"
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('category'),
            ),
            Field('content', rows=6),
            Submit('submit', 'Đăng', css_class="btn btn-success btn-lg btn-block"),
        )


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('content',)
    
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""


class ReplyForm(forms.Form):
    content = forms.CharField(max_length=300)

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""