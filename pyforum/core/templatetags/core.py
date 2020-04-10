from django import template


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
