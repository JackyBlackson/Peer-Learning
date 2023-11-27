"""PeerLearningSystemProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PeerLearningAPP.views import  user_views,check_views,homework_views,answer_views,assignment_views,admin_views,data_generate_view

# 路由注册
urlpatterns = [
    path('domain/user/add', user_views.RegisterUser, name='register_user'),
    path('domain/user/login', user_views.UserLogin, name='user_login'),
    path('domain/user/delete', user_views.UserDelete, name='user_delete'),
    path('domain/user/info', user_views.ShowInfo, name='show_info'),
    path('domain/user/logout', user_views.UserLogout, name='user_logout'),
    path('domain/user/modify', user_views.ModifyUserInfo, name='modify_user_info'),
    path('domain/user/listall', user_views.ListAll, name='list_all_users'),
    path('domain/user/assignment', user_views.ListAssignment, name='list_assignments'),

    path('domain/check/checkSim', check_views.SimhashDetect, name='check_simhash'),
    # path('domain/check/checkGpt', check_views.gptDetect, name='check_gpt'),
    path('domain/ai/queryAi', check_views.queryAi, name='query_ai'),
    path('domain/homework/add', homework_views.create_homework, name='add_homework'),
    path('domain/homework/delete', homework_views.delete_homework, name='delete_homework'),
    path('domain/homework/all', homework_views.list_homeworks, name='list_all_homeworks'),
    path('domain/homework/update', homework_views.update_homework_partial, name='update_homework'),
    path('domain/homework/showHomework', homework_views.showHomeWork, name='show_homework'),
    path('domain/homework/getHomeworkByCourse', homework_views.get_homeworks_by_course, name='get_homework_by_course'),
    path('domain/homework/getHomeworkByCourseForStu', homework_views.get_homeworks_by_course_forStu, name='get_homework_for_student_by_course'),
    path('domain/homework/grade', homework_views.get_score_distribution, name='get_homework_grade_distribution'),

    path('domain/answer/add', answer_views.create_answer, name='create_answer'),
    path('domain/answer/delete', answer_views.delete_answer, name='delete_answer'),
    path('domain/answer/update', answer_views.update_answer, name='update_answer'),
    path('domain/answer/getAnsDetail', answer_views.get_answer_details, name='get_answer_details'),
    path('domain/answer/updateScore', assignment_views.update_final_scores, name='update_final_scores'),

    path('domain/assignment/start', assignment_views.assign_homework, name='assign_homework'),
    path('domain/assignment/getWork', assignment_views.get_assignments_for_student, name='get_assignments_for_student'),
    path('domain/assignment/info', assignment_views.get_assignment_details, name='get_assignment_details'),
    path('domain/assignment/setAssignment', assignment_views.update_assignment, name='set_assignment'),
    path('domain/assignment/upgradeStuWeights', assignment_views.update_student_weights, name='upgrade_student_weights'),
    path('domain/answer/getCourseAns', assignment_views.get_course_summary, name='get_course_summary'),
    path('domain/homework/complaint', assignment_views.update_assignments_complaint, name='update_assignment_complaint'),
    path('domain/homework/assignHomework', assignment_views.assign_homework, name='reassign_homework'),

    path('domain/manager/getAllStudents', admin_views.GetAllStudents, name='get_all_students'),
    path('domain/manager/getAllTeachers', admin_views.GetAllTeachers, name='get_all_teachers'),
    path('domain/manager/getAllAssistants', admin_views.GetAllAssistants, name='get_all_assistants'),

    path('domain/teaching/info', assignment_views.get_courses_by_teacher, name='get_courses_by_teacher'),
    path('domain/selecting/info', assignment_views.get_courses_by_student, name='get_courses_by_student'),

    path('domain/user/get-upload-token', user_views.GetUploadToken, name='get_upload_token'),
    path('domain/data/generate', data_generate_view.generate_data_view, name='generate_data')
]
