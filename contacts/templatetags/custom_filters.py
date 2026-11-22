from django import template

register = template.Library()


@register.filter
def censor_phone(phone):
    if not phone:
        return "Номер скрыт императоршей"
    text = str(phone).strip()
    if len(text) > 4:
        return f"{text[:-4]}****"
    return text