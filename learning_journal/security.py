USERS = {
    'viewer': 'viewer',
    'user': 'user',
    'admin': 'admin',
}


GROUPS = {'admin': ['g:admin']}


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

# def groupfinder(userid, request):
#     groups = []
#     if userid.lower() in request.approved:
#         groups.append('g:users')
#     if userid.lower() in request.admins:
#         groups.append('g:admins')
#     return groups or None
