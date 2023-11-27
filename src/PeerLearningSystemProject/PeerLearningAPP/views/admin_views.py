from django.shortcuts import render
from django.http import JsonResponse
import django.http.request
from PeerLearningAPP.utilities.request_util import JsonRes
import json
from PeerLearningAPP.models import User, Assignment
import PeerLearningAPP.middleware.user.token_middleware as token_middleware
from PeerLearningAPP.utilities.request_util import post_response, get_response, SuccessResponse, FailResponse , session_required, role_required, role, MultiSuccessResponse

@get_response([])
@session_required()
@role_required([0])
def GetAllStudents(request, params, u : User):
    searchedUsers = User.objects.filter(roleType = 2)
    result = []
    for student in searchedUsers:
        result.append({
            "userId": student.userId,
            "roleType": student.roleType,
            "userName": student.userName,
            "password": student.password,
            "class": student.class_field,
            "userFace": student.userFace,
            "email": student.email
        })
    return MultiSuccessResponse("成功查询所有学生的信息", result)

@get_response([])
@session_required()
@role_required([0])
def GetAllTeachers(request, params, u : User):
    searchedUsers = User.objects.filter(roleType = 1)
    result = []
    for teacher in searchedUsers:
        result.append({
            "userId": teacher.userId,
            "roleType": teacher.roleType,
            "userName": teacher.userName,
            "password": teacher.password,
            "class": teacher.class_field,
            "userFace": teacher.userFace,
            "email": teacher.email
        })
    return MultiSuccessResponse("成功查询所有教师的信息", result)

@get_response([])
@session_required()
@role_required([0])
def GetAllAssistants(request, params, u : User):
    searchedUsers = User.objects.filter(roleType = 3)
    result = []
    for assistant in searchedUsers:
        result.append({
            "userId": assistant.userId,
            "roleType": assistant.roleType,
            "userName": assistant.userName,
            "password": assistant.password,
            "class": assistant.class_field,
            "userFace": assistant.userFace,
            "email": assistant.email
        })
    return MultiSuccessResponse("成功查询所有助教的信息", result)