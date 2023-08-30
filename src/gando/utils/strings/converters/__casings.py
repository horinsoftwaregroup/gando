from gando.utils.strings.casings import (
    SNAKE_CASE,
    CAMEL_CASE,
    PASCAL_CASE,
    KEBAB_CASE,
)


def casings(value: str, from_case: str, to_case: str):
    tmp, start_underscores = get_all_start_underscores(value)
    tmp, end_underscores = get_all_end_underscores(tmp)

    len_tmp = len(tmp)
    if len_tmp == 0:
        return value

    match from_case.lower():
        case 'snake':
            match to_case:
                case 'camel':
                    rslt = s2c(tmp)
                case 'pascal':
                    rslt = s2p(tmp)
                case 'kebab':
                    rslt = s2k(tmp)
                case _:
                    rslt = tmp
        case 'camel':
            match to_case:
                case 'snake':
                    rslt = c2s(tmp)
                case 'pascal':
                    rslt = c2p(tmp)
                case 'kebab':
                    rslt = c2k(tmp)
                case _:
                    rslt = tmp
        case 'pascal':
            match to_case:
                case 'snake':
                    rslt = p2s(tmp)
                case 'camel':
                    rslt = p2c(tmp)
                case 'kebab':
                    rslt = p2k(tmp)
                case _:
                    rslt = tmp
        case 'kebab':
            match to_case:
                case 'snake':
                    rslt = k2s(tmp)
                case 'camel':
                    rslt = k2c(tmp)
                case 'pascal':
                    rslt = k2p(tmp)
                case _:
                    rslt = tmp
        case _:
            rslt = tmp
    ret = start_underscores + rslt + end_underscores
    return ret


def s2c(value: str):
    tmp = ''
    uppercase = False
    for c in value:
        if c == '_':
            uppercase = True
            continue
        tmp += c.upper() if uppercase else c
        uppercase = False
    ret = tmp
    return ret


def s2p(value: str):
    tmp = ''
    uppercase = True
    for c in value:
        if c == '_':
            uppercase = True
            continue
        tmp += c.upper() if uppercase else c
        uppercase = False
    ret = tmp
    return ret


def s2k(value: str):
    ret = value.replace('_', '-')
    return ret


def c2s(value: str):
    tmp = ''
    for c in value:
        tmp += f'_{c.lower()}' if c.isupper() else c
    ret = tmp
    return ret


def c2p(value: str):
    ret = value[0].upper() + value[1:] if len(value) > 1 else ''
    return ret


def c2k(value: str):
    tmp = ''
    for c in value:
        tmp += f'-{c.lower()}' if c.isupper() else c
    ret = tmp
    return ret


def p2s(value: str):
    tmp = value[0].lower()
    for c in value[1:] if len(value) > 1 else '':
        tmp += f'_{c.lower()}' if c.isupper() else c
    ret = tmp
    return ret


def p2c(value: str):
    ret = value[0].lower() + value[1:] if len(value) > 1 else ''
    return ret


def p2k(value: str):
    tmp = value[0].lower()
    for c in value[1:] if len(value) > 1 else '':
        tmp += f'-{c.lower()}' if c.isupper() else c
    ret = tmp
    return ret


def k2s(value: str):
    ret = value.replace('-', '_')
    return ret


def k2c(value: str):
    tmp = ''
    uppercase = False
    for c in value:
        if c == '-':
            uppercase = True
            continue
        tmp += c.upper() if uppercase else c
        uppercase = False
    ret = tmp
    return ret


def k2p(value: str):
    tmp = ''
    uppercase = True
    for c in value:
        if c == '-':
            uppercase = True
            continue
        tmp += c.upper() if uppercase else c
        uppercase = False
    ret = tmp
    return ret


def get_all_start_underscores(value):
    i = 0
    start_underscores = ''
    while value[i] == '_':
        start_underscores += '_'
        i += 1
    return value[i:], start_underscores


def get_all_end_underscores(value):
    i = -1
    end_underscores = ''
    while value[i] == '_':
        end_underscores += '_'
        i -= 1
    return value[:len(value) + i + 1], end_underscores
