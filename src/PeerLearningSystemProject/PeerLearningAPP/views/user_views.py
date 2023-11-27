from django.shortcuts import render
from django.http import JsonResponse
import django.http.request
from PeerLearningAPP.utilities.request_util import JsonRes
import json
from PeerLearningAPP.models import User, Assignment
import PeerLearningAPP.middleware.user.token_middleware as token_middleware
from PeerLearningAPP.utilities.request_util import post_response, get_response, SuccessResponse, FailResponse , session_required, role_required, role
from qiniu import Auth

def RegisterUser(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body.get("email")
        userName = body.get("userName")
        password = body.get("password")
        id = body.get("userId")
        
        success = False
        
        message = ""
        
        res = {}
        
        if (email is not None and userName is not None and password is not None):
            try :
                if len(User.objects.filter(userId = id)) != 0:
                    message = f"用户id {id} 已经被注册"
                    res = {
                    "status": success,
                    "description": message,
                    "code": 200,
                    "data": [
                            {}
                        ]
                    }
                else:
                    u = User.objects.create(userName = userName, email = email, password = password, userId = id,roleType = 2)
                    message = f"成功注册用户 {userName}，id是 {u.userId}"
                    success = True
                    res = {
                    "status": success,
                    "description": message,
                    "code": 200,
                    "data": [
                            {
                                "userId": u.userId,
                                "userName": u.userName,
                                "rollType": 2
                            }
                        ]
                    }
            except Exception as e:
                    message = f"遇到未知问题，注册失败"
                    res = {
                    "status": success,
                    "description": message,
                    "code": 200,
                    "data": [
                            {}
                        ]
                    }
        
        
        return JsonRes(res)
    else:
        return JsonRes({"error": "Invalid request method."})
    
def UserLogin(request):
    if request.method == "POST":
        body = json.loads(request.body)
        id = body.get("userId")
        pwd = body.get("password")
        success = False
        message = ""
        data = {}
        if (id is not None and pwd is not None):
            if len(User.objects.filter(userId = id)) != 1:
                success = False
                message = "用户名不存在"
            else:
                u = User.objects.filter(userId = id)[0]
                if(u.password == pwd) :
                    token = token_middleware.generate_token()
                    User.objects.filter(userId = id).update(token = token)
                    success = True
                    message = "登陆成功"
                    data = {"userId": f"{u.userId}",
                            "userName": u.userName,
                            "class": u.class_field,
                            "email": u.email,
                            "roleType": u.roleType,
                            "userFace": u.userFace,
                            'session': token
                            }
                else:
                    success = False
                    message = "密码错误"
        else:
            success = False
            message = "缺少必要参数"
            
        res = {
                "status": success,
                "description": message,
                "code": 200,
                "data": [
                        data
                    ]
                }
        return JsonRes(res)
            
    else:
        return JsonRes({"error": "Invalid request method."})
    

@post_response(['userName', 'userId'])
@session_required()
@role_required([0])
def UserDelete(request, params, u : User):
    users = User.objects.filter(userId = params['userId'])
    if(len(users) == 1):
        if users[0].userName == params['userName']:
            users.delete()
            return SuccessResponse("成功删除用户！", {"username": params['userName'], "userId": params['userId']})
        else:
            return FailResponse("用户名不匹配用户id！")
    else:
        return FailResponse("用户id不存在！")
    
@get_response(["userId"])
@session_required()
@role_required([0,1,2,3,4])
def ShowInfo(request, params, us : User):
    # 可以查看任何人信息的权限组
    allowed_role = [0,1,3]
    # 查询输入的用户id
    user_id = int(params["userId"])
    # 如果用户无权查看所有人信息，且用户查询的用户非自己，则查询失败
    if(us.roleType not in allowed_role and user_id != us.userId):
        # 查询失败返回
        return FailResponse("您没有权限查看id为{user_id}的用户的详细信息")
    # 否则，查询
    users = User.objects.filter(userId = user_id)
    # 如果用户不存在
    if(len(users) != 1):
        return FailResponse("您查看的用户id {user_id} 不存在！")
    u = users[0]
    # 用户的信息列表
    data = {"userId": u.userId,
            "roleType": u.roleType,
            "userName": u.userName,
            "password": u.password,
            "class": u.class_field,
            "userFace": u.userFace,
            "email": u.email,
            'session': u.token
            }
    # 查询成功返回
    return SuccessResponse(f"成功查询 id 为 {u.userId} 的用户【{u.userName}】的个人信息", data)

@get_response(["userId", "roleType", "userName", "password", "class", "userFace", "email"])
@session_required()
@role_required([0,1,3])
def ModifyInfo(request, params, u : User):
    return SuccessResponse("TODO: FINISH THIS API", {})

@post_response([])
@session_required()
def UserLogout(request, params, u : User):
    User.objects.filter(userId = u.userId).update(token = "NULL_NOT_LOGIN")
    return SuccessResponse(f"id为 {u.userId} 的用户【{u.userName}】已经成功登出！", {})

def RequestTemplate(request):
    if request.method == "POST":
        body = json.loads(request.body)
        # 获取参数
        id = body.get("userId")
        #初始化返回值
        success = False
        message = ""
        data = {}
        
        # 在这里插入业务逻辑
        ################################################################
        ################################################################
        ################################################################
        # 业务逻辑完毕
        
        res = {
                "status": success,
                "description": message,
                "code": 200,
                "data": [
                        data
                    ]
                }
        return JsonRes(res)        
    else:
        return JsonRes({"error": "Invalid request method."})
    
@get_response(['filename'])
@session_required()
@role_required([0,1,2,3])
def GetUploadToken(request, params, u : User):
    #需要填写你的 Access Key 和 Secret Key
    access_key = 'RvSSLZzyvWnQoHd6qWRNJpV4E3ti2Ifemsxj6Xvc'
    secret_key = 'GH2eDLZEJAItCNQqORoqjcfH3jzFqZo8Z_TqPKQm'
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token('peerlearning2023', params['filename'], 3600)
    return SuccessResponse("成功获取token", {"filename":params['filename'], "token":token})

@post_response(['userId', 'roleType', 'userName', 'password', 'class', 'userFace', 'email'])
@session_required()
@role_required([0,1,2,3,4])
def ModifyUserInfo(request, params, u : User):
    # 如果用户是管理员
    if(u.roleType == 0):
        userInstance = User.objects.filter(userId = params['userId'])
        if(len(userInstance)!=1):
            return FailResponse(f"您要更新的用户（id = {params['userId']}）不存在！")
        userInstance.update(roleType = params['roleType'])
        userInstance.update(userName = params['userName'])
        userInstance.update(password = params['password'])
        userInstance.update(class_field = params['class'])
        userInstance.update(userFace = params['userFace'])
        userInstance.update(email = params['email'])
        return SuccessResponse(f"您成功作为管理员更新了用户 {params['userId']} 的信息", {})
    else:
        if (u.userId != int(params['userId'])):
            return FailResponse(f"您不是管理员用户，无法更新其他用户的信息！")
        if(u.roleType != params['roleType']):
            return FailResponse(f"您不是管理员用户，无法更新您的权限信息！")
        userInstance = User.objects.filter(userId = u.userId)
        userInstance.update(userName = params['userName'])
        userInstance.update(password = params['password'])
        userInstance.update(class_field = params['class'])
        userInstance.update(userFace = params['userFace'])
        userInstance.update(email = params['email'])
        return SuccessResponse(f"您成功更新了您（{u.userName}）的信息", {})
    
@get_response([])
@session_required()
@role_required([0, 1])
def ListAll(request, params, u : User):
    result = []
    for u in User.objects.all():
        result.append({"userId":u.userId, "userName":u.userName, "roleType":u.roleType})
    return SuccessResponse("成功获取用户列表", result)

@get_response(['userId'])
@session_required()
@role_required([0,1,2,3,4])
def ListAssignment(request, params, u : User):
    # 不合格情况遍历
    if(u.roleType not in [0,1] and u.userId != int(params['userId'])):  # 非管理员用户查看非自身用户任务列表
        return FailResponse(f"您不是管理员，无法查看非自身用户（id={u.userId}）的任务列表")
    userSet = User.objects.filter(userId = params['userId'])
    if(len(userSet) != 1):
        return FailResponse(f"您查询的用户id（{params['userId']}）不存在！")
    targUser = userSet[0]
    assignSet = Assignment.objects.filter(student = targUser, isFinished = 0)
    result = []
    for a in assignSet:
        result.append({
            "assignementId": a.assignmentId,
            #"courseId": a.,
            "startTime": str(a.startTime),
            "endTime": str(a.endTime),
            "isFinished": str(a.isFinished),
            "studentId": a.student.userId,
            "answerId": a.answer.answerId,
            "teacherId": a.teacher.userId,
            "grade": a.grade
        })
    return SuccessResponse(f"成功查询用户 {targUser.userName} 的未完成任务列表！", result)
        
    

        



# @get_response(['studentId'])
# @session_required()
# # @role_required([0,1,2,3])
# def ShowSingleInfo(request, params, us : User):
#     # 可以查看任何人信息的权限组
#     # allowed_role = [0,1,2]
#     # 查询输入的用户id
#     user_id = params["userId"]
#     users = User.objects.filter(userId = user_id)
#     # 如果用户不存在
#     if(len(users) != 1):
#         return FailResponse("您查看的用户id {user_id} 不存在！")
#     u = users[0]
#     # 用户的信息列表
#     data = {"userId": u.userId,
#             "roleType": u.roleType,
#             "userName": u.userName,
#             "password": u.password,
#             "class": u.class_field,
#             "userFace": u.userFace,
#             "email": u.email,
#             'session': u.token
#             }
#     # 查询成功返回
#     return SuccessResponse(f"成功查询 id 为 {u.userId} 的用户【{u.userName}】的个人信息", data)


