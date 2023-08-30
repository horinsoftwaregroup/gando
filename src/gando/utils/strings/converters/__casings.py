from gando.utils.strings.casings import (
    SNAKE_CASE,
    CAMEL_CASE,
    PASCAL_CASE,
    KEBAB_CASE,
)


def casings(value: str, from_case: str, to_case: str):
    match from_case.lower():
        case 'snake':
            match to_case:
                case 'camel':
                    return s2c(value)
                case 'pascal':
                    return s2p(value)
                case 'kebab':
                    return s2k(value)
                case _:
                    return value
        case 'camel':
            match to_case:
                case 'snake':
                    return c2s(value)
                case 'pascal':
                    return c2p(value)
                case 'kebab':
                    return c2k(value)
                case _:
                    return value
        case 'pascal':
            match to_case:
                case 'snake':
                    return p2s(value)
                case 'camel':
                    return p2c(value)
                case 'kebab':
                    return p2k(value)
                case _:
                    return value
        case 'kebab':
            match to_case:
                case 'snake':
                    return k2s(value)
                case 'camel':
                    return k2c(value)
                case 'pascal':
                    return k2p(value)
                case _:
                    return value
        case _:
            return value


def s2c(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''
    uppercase = False

    for c in value:
        if c == '_':
            uppercase = True

        tmp += c.upper() if uppercase else c
        uppercase = False

    value = start_underscores + tmp + end_underscores
    return value


def s2p(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''
    uppercase = True

    for c in value:
        if c == '_':
            uppercase = True

        tmp += c.upper() if uppercase else c
        uppercase = False

    value = start_underscores + tmp + end_underscores
    return value


def s2k(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''

    for c in value:
        tmp += '-' if c == '_' else c

    value = start_underscores + tmp + end_underscores
    return value


def c2s(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''

    for c in value:
        tmp += f'_{c.lower()}' if c.isupper() else c

    value = start_underscores + tmp + end_underscores
    return value


def c2p(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    value = start_underscores + value[0].upper() if len(value) > 0 else '' + value[1:] if len(
        value) > 1 else '' + end_underscores
    return value


def c2k(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''

    for c in value:
        tmp += f'-{c.lower()}' if c.isupper() else c

    value = start_underscores + tmp + end_underscores
    return value


def p2s(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = value[0].lower()

    for c in value[1:]:
        tmp += f'_{c.lower()}' if c.isupper() else c

    value = start_underscores + tmp + end_underscores
    return value


def p2c(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    value = start_underscores + value[0].lower() if len(value) > 0 else '' + value[1:] if len(
        value) > 1 else '' + end_underscores
    return value


def p2k(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = value[0].lower()

    for c in value[1:]:
        tmp += f'-{c.lower()}' if c.isupper() else c

    value = start_underscores + tmp + end_underscores
    return value


def k2s(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''

    for c in value:
        tmp += '_' if c == '-' else c

    value = start_underscores + tmp + end_underscores
    return value


def k2c(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''
    uppercase = False

    for c in value:
        if c == '-':
            uppercase = True

        tmp += c.upper() if uppercase else c
        uppercase = False

    value = start_underscores + tmp + end_underscores
    return value


def k2p(value: str):
    value, start_underscores = get_all_start_underscores(value)
    value, end_underscores = get_all_end_underscores(value)

    tmp = ''
    uppercase = True

    for c in value:
        if c == '-':
            uppercase = True

        tmp += c.upper() if uppercase else c
        uppercase = False

    value = start_underscores + tmp + end_underscores
    return value


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
