def merge_dicts_recursive(list_of_dicts):
    result = {}
    for d in list_of_dicts:
        for key, value in d.items():
            if key not in result:
                result[key] = value
            else:
                if isinstance(result[key], list) and isinstance(value, list):
                    result[key].extend(value)
                elif isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts_recursive([result[key], value])
    return result
