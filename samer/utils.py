from ast import literal_eval


def get_tuple_list_env(list: str | None):
    if list is None:
        return ""
    res = list.split(";")
    res = [literal_eval(t) for t in res]
    return res
