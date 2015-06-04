from django import template

register = template.Library()

def keyvalue(dict, key):    
    try:
        return dict[key]
    except KeyError:
        return ''
        
register.filter('keyvalue', keyvalue)