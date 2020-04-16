from django import template
from django.utils.html import mark_safe

from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

register = template.Library()


@register.filter(name='class_color')
def get_class_color(instance):
    colors = [
        'primary', 'secondary', 'info',
        'success', 'warning', 'dark',
    ]

    try:
        index = instance.id % len(colors)
        return colors[index]
    except:
        return 'primary'
        

@register.filter(name='markdown')
def markdown_filter(value):
    return mark_safe(markdown(value, safe_mode='escape', extensions=[GithubFlavoredMarkdownExtension()]))
