import json


def get_log(fp):
    return json.loads(open(fp, 'r').read())


def get_logged_item(fp, item):
    log = json.loads(open(fp, 'r').read())
    return log[item]


def write_log(fp, log):
    with open(fp, 'w') as file_obj:
        json.dump(log, file_obj, indent=4)
        file_obj.close()


def reset_history(fp, item):
    log = get_log(fp)
    log[item] = []
    write_log(fp, log)


def append_log(fp, item, append_list):
    log = get_log(fp)
    log[item].extend(append_list)
    write_log(fp, log)


