from django import template

register = template.Library()


@register.inclusion_tag('ats_statistics/block_btn_link.html')
def dialog_btn_link(dialog_id, link, pk):
    return {'dialog_id': dialog_id, 'link': link}


@register.filter
def get_item(dictionary, key):
    if dictionary and key:
        if hasattr(dictionary, 'get'):
            return dictionary.get(key)
        else:
            return getattr(dictionary, key)
    else:
        return None


@register.simple_tag
def show_dict_sub(dictionary, key, subkey=None, default=None):
    if dictionary and key:
        if hasattr(dictionary, 'get'):
            result = dictionary.get(key)
        else:
            result = getattr(dictionary, key)

        if subkey:
            return show_dict_sub(result, subkey, None, default)
        else:
            return result
    else:
        return default
