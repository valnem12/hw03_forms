from django import template
from django.utils.html import format_html
from yatube.settings import LOGIN_REDIRECT_URL
from django.urls import reverse


register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={'class': css, 'autofocus': 'username'})


@register.simple_tag
def addmethod(access):
    action_url = reverse(LOGIN_REDIRECT_URL)
    if action_url == '/':
        action_url = ''
    if access == 'login':
        return format_html(
            '<form method="post" '
            'action="{}">', action_url
        )
    return format_html(
        '<form method="post" '
        'action="{}">', action_url
    )


@register.simple_tag
def addmethod2(access):
    if access == 'login':
        return format_html("<div class='form-group row my-3' "
                           "{{% if field.field.required %}} "
                           "aria-required='true' {{% else %}} "
                           "aria-required='false' {{% endif %}}>")
    return format_html("<div class='form-group row my-3'>")
