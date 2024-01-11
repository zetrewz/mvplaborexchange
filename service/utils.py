def is_employer(user):
    return hasattr(user, 'profile')


def is_worker(user):
    return not hasattr(user, 'profile')
