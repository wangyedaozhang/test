import jsonpickle

def getLoginUserInfo(request):
    '''获取登录用户信息'''
    user = request.session.get('user','')
    print(user)
    if user:
        user = jsonpickle.loads((user))

    return {'loginUser':user}