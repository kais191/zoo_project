from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    """Add a CSS class to a form field."""
    return value.as_widget(attrs={"class": arg})
