def remove_dict_key(obj, *keys):
    if keys:
        for key in keys:
            obj.pop(key, None)


def update_dict(current, new):
    return {**current, **new}