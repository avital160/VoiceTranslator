import uuid


def generate_random_filename(extension=''):
    if extension:
        return uuid.uuid4().hex + '.' + extension
    else:
        return uuid.uuid4().hex
