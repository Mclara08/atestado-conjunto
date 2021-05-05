from django import template

register = template.Library()

@register.simple_tag
def minha_url(valor, nome_campo, urlencode=None):
    url = '?{}={}'.format(nome_campo, valor)
    if urlencode:
        query = urlencode.split('&')
        filtro_query = filter(lambda p: p.split('=')[0]!=nome_campo, query)
        encode_query = '&'.join(filtro_query)
        url = '{}&{}'.format(url, encode_query)

    return url