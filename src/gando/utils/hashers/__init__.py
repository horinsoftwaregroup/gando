from django.contrib.auth.hashers import get_hasher, identify_hasher


def make_hash_string(value, salt=None, hasher='default'):
    if value is None:
        return None

    value = str(value)
    hasher = get_hasher(hasher)
    salt = salt or hasher.salt()

    ret = hasher.encode(value, salt)
    return ret


def check_hash_string(value, encoded, setter=None, preferred='default'):
    if not value:
        return False

    preferred = get_hasher(preferred)
    try:
        hasher = identify_hasher(encoded)
    except ValueError:
        return False

    hasher_changed = hasher.algorithm != preferred.algorithm
    must_update = hasher_changed or preferred.must_update(encoded)
    is_correct = hasher.verify(value, encoded)

    if not is_correct and not hasher_changed and must_update:
        hasher.harden_runtime(value, encoded)

    if setter and is_correct and must_update:
        setter(value)

    ret = is_correct
    return ret
