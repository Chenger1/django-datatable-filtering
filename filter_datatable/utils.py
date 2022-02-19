def get_none_attr(obj, attr_name, default_value):
    obj_attr = getattr(obj, attr_name, None)
    return obj_attr if obj_attr else default_value
