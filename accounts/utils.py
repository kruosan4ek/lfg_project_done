"""
Утилиты для приложения accounts.
"""


def add_bootstrap_classes(form):
    """Добавляет Bootstrap-классы всем полям формы."""
    for field in form.fields.values():
        widget = field.widget
        if widget.__class__.__name__ in ('CheckboxInput',):
            widget.attrs.update({'class': 'form-check-input'})
        elif widget.__class__.__name__ in ('Select', 'SelectMultiple'):
            widget.attrs.update({'class': 'form-select'})
        elif widget.__class__.__name__ in ('ClearableFileInput', 'FileInput'):
            widget.attrs.update({'class': 'form-control'})
        else:
            widget.attrs.update({'class': 'form-control'})
    return form