from django import template
from django.utils.dates import MONTHS
from django.utils.html import escape, mark_safe

import json

register = template.Library()

@register.filter(name='split_help_text')
def split(value, key):
    string_list = value.split(key)
    return_list = []
    for i in range(0, len(string_list)):
        if len(string_list[i]) > 0:
            return_list.append(string_list[i] + '.') # add again the dot removed

    return return_list


@register.filter(name='mask_cns')
def mask_cns(value):
    return value[:3] +' '+ value[3:7] +' '+ value[7:11] +' '+ value[11:15]


@register.filter(name='mask_cpf')
def mask_cpf(value):
    return value[:3] +'.'+ value[3:6] +'.'+ value[6:9] +'-'+ value[9:11]


@register.filter(name='mask_cnpj')
def mask_cnpj(value):
    return value[:2] +'.'+ value[2:5] +'.'+ value[5:8] +'/'+ value[8:12] +'-'+ value[12:14]

@register.filter(name='mask_cep')
def mask_cep(value):
    return value[:2] +'.'+ value[2:5] +'-'+ value[5:]


@register.filter(name='startswith')
def startswith(text, starts):
    if text.startswith(starts):
        return True
    else:
        return False

@register.filter(name='mask_str_date_to_date')
def mask_str_date_to_date(value):
    return value[-4:] +"-"+ value[3:5] +"-"+ value[:2]

@register.filter(name='file_startswith')
def file_startswith(text, starts):
    if text.name.startswith(starts):
        return True
    else:
        return False


def brake_int(value_int):
    str_final = ''
    count = 1

    for char in value_int[::-1]:
        if count == 3:
            str_final = '.'+ char + str_final
            count = 1
        else:
            str_final = char + str_final
            count += 1

    return str_final[1:] if str_final.startswith('.') else str_final
    
    
# ex de uso: {% <value>|mask_money:"R$" %}
@register.filter(name='mask_money')
def mask_money(value, sign=None):
    if sign is None:
        sign = 'R$'
    if value:
        str_value = str(value)
    
        int_part = brake_int(str_value.split(".")[0])
        dec_part = "{:0<2}".format(str_value.split(".")[1])
        str_value = ",".join([int_part, dec_part])
    else:
        str_value = "0,00"
    
    return " ".join([sign, str_value])

# ex de uso: {% mask_money_dec <value> "R$" 2 %} Retorno: R$ 1.429,00
@register.simple_tag
def mask_money_dec(value, sign, dec=None):
    
    if value:
        str_value = str(round(float(value), int(dec)))

        int_part = brake_int(str_value.split(".")[0])
        dec_part = "{:0<2}".format(str_value.split(".")[1])
        str_value = ",".join([int_part, dec_part])
    else:
        str_value = "0,00"
    return " ".join([sign, str_value])

# ex de uso: {% mask_money_dec <value> "R$" 2 %} Retorno: R$      1.429,00
@register.simple_tag
def mask_money_dec_contabil(value, sign, dec=None):
    
    if value:
        str_value = str(round(float(value), int(dec)))

        int_part = brake_int(str_value.split(".")[0])
        dec_part = "{:0<2}".format(str_value.split(".")[1])

        str_value = ",".join([int_part, dec_part])

        returned = sign + '{:_>15}'.format(str_value)
    else:
        returned = sign + '{:_>15}'.format('0,00')

    returned = returned.replace("_"," &nbsp;")
    return mark_safe(returned)

    #width = 15
    #padding = ' '
    #return sign +f'{str_value :{padding}>{width}}'

@register.simple_tag
def get_uf(cities_uf):
    return cities_uf[-2:]


def get_str_date_comp(date_object):
    #months_dict = {""}
    month_choices = dict(MONTHS.items())

    month = month_choices[date_object.month]

    return f"{month} de {date_object.year}"

def get_very_large_number(number, sep="."):
    num_aux = number
    str_num = ""

    while num_aux > 0:
        num_aux = num_aux/1000
        str_num_aux = str(num_aux).split(".")[1]
        
        while len(str_num_aux) < 3:
            str_num_aux += "0"

        if int(num_aux) > 0:
            str_num = "."+ str_num_aux + str_num
        else:
            str_num = str(int(str_num_aux)) + str_num

        num_aux = int(num_aux)
       
    return str_num

# retorna o valor pela chave informada
@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='dict_template_value')
def dict_template_value(d, value_choiced):
    # value_choiced deve ser:
    #   uma string com a chave
    
    # Exemplo de um dict_template
    #dict_template['templatePerson'] = {
    #    'cod': slug_searched, # código a ser carregado (primary key ou slug)
    #    'filter': area_choiced, # Filtro de identificação. No caso deste template é 'area_choiced'
    #    }

    value_back = None
    
    for key, value in d.items():
        if key == 'templatePerson':
            for keyB, valueB in value.items():
                if keyB == value_choiced:
                    value_back = valueB
                    break

    return value_back

# Verifica se usuário pertence ao grupo informado
@register.filter(name='isin_group')
def isin_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Verifica a instância de um número e retorna a string com ou sem ponto decimal
@register.filter(name='numeric_format')
def numeric_format(value):
    #num_int = str(value).split('.')[0]
    num_float = str(value).split('.')[1]

    if int(num_float) > 0:
        return "{}".format(value)
    else:
        return int(value)

@register.filter(name='get_key_by_dict_string')
def get_key_by_dict_string(str_dict, key):
    try:
        new_dict = json.loads(str_dict)
        return new_dict.get(key)
    except:
        return ""

@register.filter(name='has_key_in_dict_string')
def has_key_in_dict_string(str_dict, key):
    try:
        new_dict = eval(str_dict)
        return True if key in new_dict.keys() else False
    except:
        return ""

# verifica se User possui instância em Person
@register.filter(name='has_person')
def has_person(user):
    from person.models import Person
    try:
        person = Person.objects.get(user=user)
        return True
    except Person.DoesNotExist:
        return False

