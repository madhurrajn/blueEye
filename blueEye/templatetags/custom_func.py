from django import template

register = template.Library()

@register.filter
def compare_hour(hour, val):
    if hour < val:
        return True
    else:
        return False

@register.filter
def get_cell_elem(cell, listelem):
    for elem in listelem.cell_list:
        if elem.cell_name==cell.cell_name:
            return elem
