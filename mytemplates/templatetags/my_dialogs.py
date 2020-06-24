from django import template

register = template.Library()


@register.inclusion_tag('ats_statistics/block_btn_link.html')
def dialog_btn_link(dialog_id,link,pk):
    return {'dialog_id':dialog_id, 'link': link}