from django.http import JsonResponse
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from PeerLearningAPP.models import User


def JsonRes(d, safe=False):
    # res = JsonResponse(d, safe=safe, headers={"Access-Control-Allow-Origin":"http://localhost:9999"})
    # # 允许相应的域名来访问，多个域名中间以逗号隔开，如果全部可使用'*'
    # res['Access-Control-Allow-Origin'] = "*"
    # # 允许携带的请求头，多个中间以逗号隔开
    # res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, access-control-allow-origin"
    # # 允许发送的请求方式
    # res['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
    # res['Access-Control-Allow-Credentials'] = "true"
    
    res = JsonResponse(d, safe=safe)
    return res

def FailResponse(msg : str):
    res = {
                "status": False,
                "description": msg,
                "code": 200,
                "data": [
                        {}
                    ]
                }
    return JsonRes(res)

def SuccessResponse(msg: str, data : dict):
    res = {
                "status": True,
                "description": msg,
                "code": 200,
                "data": [
                        data
                    ]
                }
    return JsonRes(res)

def MultiSuccessResponse(msg: str, data : dict):
    res = {
                "status": True,
                "description": msg,
                "code": 200,
                "data": data
                }
    return JsonRes(res)
    



class message:
    notEnoughParameter = "缺少必要参数"
    unknownError = "遇到未知问题，请求失败"
    wrongRequestMethod = "错误的请求方法，请求失败"
    
    class user:
        class session:
            invalidSession = "用户的session不正确或不存在"
        class register:
            idAlreadyExist = "用户id已经被注册"
            success = "成功注册用户"
        class login:
            idNotExist = "用户名不存在"
            wrongPassword = "密码错误"
            success = "成功登录"
    class role:
        class check:
            noPermission = "当前用户的角色没有权限执行此请求，请求失败"
            
class role:
    admin = 0
    teacher = 1
    assitant = 2
    student = 3
    visiter = 4
            
def post_response(required_params : list):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if request.method != 'POST':
                return FailResponse(f"错误的请求方法（{request.method}），应当是 POST。请求失败！" )
            
            params = {}
            
            if len(required_params) == 0:
                return func(request, params)
            try:
                body = json.loads(request.body)
                for param_name in required_params:
                    
                    param_value = body.get(param_name)
                    if param_value is None:
                        return FailResponse(message.notEnoughParameter + ": " + param_name)
                    params[param_name] = param_value

                return func(request, params)
            except Exception as e:
                return FailResponse(message.notEnoughParameter + f": {e.__class__}错误（{str(e)}）：" + ", ".join(required_params))
        return wrapper
    return decorator

def get_response(required_params : list):
    
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            print("nihao, getresponse")
            if request.method != 'GET':
                return FailResponse(f"错误的请求方法（{request.method}），应当是 GET。请求失败！" )
            
            params = {}
            try:
                if(len(required_params) == 0):
                    return func(request, params)
                for param_name in required_params:
                    param_value = request.GET[param_name]
                    if param_value is None:
                        return FailResponse(message.notEnoughParameter + ": 参数【" + param_name + "】未提供")
                    params[param_name] = param_value
                return func(request, params)
            except Exception as e:
                return FailResponse(message.notEnoughParameter + f": {e.__class__}错误（{str(e)}）：" + ", ".join(required_params) + repr(e.__traceback__))
        return wrapper
    return decorator

def role_required(required_rows : list):
    def decorator(func):
        @wraps(func)
        def wrapper(request, params, user : User):
            if user.roleType not in required_rows:
                return FailResponse(message.role.check.noPermission)
            else:
                return func(request, params, user)
        return wrapper
    return decorator
            

def session_required():
    def decorator(func):
        @wraps(func)
        def wrapper(request, params):
            #print("nihao,sessionrequired")
            session_key = ""
            if request.method == 'POST':
                try:
                    session_key = request.COOKIES.get('session')
                    print(str(request.COOKIES))
                except:
                    return FailResponse(message.notEnoughParameter + ": " + "session")
            elif request.method == 'GET':
                try:
                    session_key = request.COOKIES.get('session')
                    print(str(request.COOKIES))
                except:
                    return FailResponse(message.notEnoughParameter + ": " + "session")
            else:
                return FailResponse(message.wrongRequestMethod + ": " + request.method)
            if not session_key:
                return FailResponse(message.user.session.invalidSession)
            

            try:
                users = User.objects.filter(token = session_key)
                user = None
                if(len(users) != 1):
                    return FailResponse(message.user.session.invalidSession)
                else:
                    user = users[0]
            except User.DoesNotExist:
                return FailResponse(message.user.session.invalidSession)

            return func(request, params, user)

        return wrapper
    return decorator




    
    
    



