from django import template
from django.db import models
from django.forms import fields_for_model
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('mytemplates/blocks/block_btn_link.html')
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
def get_items(dictionary, *keys, default=None, object_if_no_key=False, **args):
    if dictionary and keys:
        current = dictionary
        for key in keys:
            if hasattr(current, 'get'):
                current = current.get(key)
            elif hasattr(current, key):
                current = getattr(current, key)
            else:
                if not object_if_no_key:
                    current = default
                break
        if current is None:
            current = default
        return current
    else:
        return default


@register.simple_tag
def show_dict_sub(dictionary, key, subkey=None, default=None):
    if dictionary and key:
        if hasattr(dictionary, 'get'):
            result = dictionary.get(key)
        else:
            result = getattr(dictionary, key)

        if subkey and isinstance(result, dict):
            return show_dict_sub(result, subkey, None, default)
        else:
            return result
    else:
        return default


@register.inclusion_tag('mytemplates/blocks/block_object.html')
def show_object_ex(record, deep_inspection=False, empty_value=None, simplify_object=True):
    if not record:
        return None
    if isinstance(record, models.Model):
        meta_data = fields_for_model(record)
        data = {}

        for key in meta_data:
            obj = meta_data[key]
            name = obj.label
            field = getattr(record, key)
            if hasattr(field, 'target_field'):
                if deep_inspection:
                    val = [show_object_ex(rec, deep_inspection, empty_value) for rec in field.all()]
                else:
                    if simplify_object:
                        val = [str(rec) for rec in field.all()]
                    else:
                        val = [rec for rec in field.all()]
            else:
                if hasattr(field, 'get'):
                    val = field.get()
                else:
                    val = field
                if val is None:
                    val = empty_value
            data[name] = val
    else:
        data = record
    return {'record': data}


@register.simple_tag(takes_context=True)
def abs_url(context, view_name, *args, **kwargs):
    # Could add except for KeyError, if rendering the template
    # without a request available.
    return context['request'].build_absolute_uri(
        reverse(view_name, args=args, kwargs=kwargs)
    )

# <a href='{% abs_url view_name obj.uuid %}'>
#
# {% url view_name obj.uuid as view_url %}
# <a href='{{ view_url|as_abs_url:request }}'>
@register.filter
def as_abs_url(path, request):
    return request.build_absolute_uri(path)
