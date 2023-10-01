from django import template

register = template.Library()


@register.filter(name="get_completed_point")
def get_completed_point(value):
    done = value.filter(is_done=True).count()
    all_points = value.count()
    if all_points == 0:
        return 0
    return int(100 / all_points * done)
