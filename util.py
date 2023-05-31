def get_support_count(support_object: dict) ->int:
    count = 0
    for key in list(support_object.keys()):
        count += len(support_object[key])
    return count