from PeerLearningAPP.models import User, Answer  # Make sure you import Answer or whatever the model's name is.
import json
from django.shortcuts import render
from django.db.models import Sum, Case, When, IntegerField, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from PeerLearningAPP.models import Teaching, Course,Selecting
from django.utils import timezone
import requests
from django.db.models import Avg
from PeerLearningAPP.utilities.request_util import post_response, get_response, SuccessResponse, session_required, role_required, role
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.db.models import Avg, Case, When, IntegerField,Sum
import json
from django.db.models import Q
from PeerLearningAPP.models import Homework, User
from PeerLearningAPP.utilities.request_util import SuccessResponse, FailResponse
from PeerLearningAPP.utilities.request_util import JsonRes
import json
from datetime import datetime, timedelta
from PeerLearningAPP.pretrained_model.simhash.tests.test_simhash import *
from PeerLearningAPP.pretrained_model.gptzzz.gptCheck import *
from PeerLearningAPP.models import User
import PeerLearningAPP.middleware.user.token_middleware as token_middleware
from PeerLearningAPP.models import *
import numpy as np
from PeerLearningAPP.models import Teaching, Selecting, Answer, User

@get_response(['teacherId', 'courseId', 'homeworkId'])
def get_course_summary(request, params):
    teacher_id = params['teacherId']
    course_id = params['courseId']
    homework_id = params.get('homeworkId')  # Optional parameter

    try:
        # 获取对应的 teachingId
        teaching = Teaching.objects.get(teacherId=teacher_id, courseId=course_id)

        # 计算选择这门课的学生数量
        student_count = Selecting.objects.filter(teachingId=teaching.teachingId).count()

        # 根据课程ID和可选的作业ID获取答案
        answer_query = Answer.objects.filter(homeworkId__courseId=course_id)
        if homework_id:
            answer_query = answer_query.filter(homeworkId=homework_id)
        answers = answer_query.all()
        total_submissions = answers.count()  # 计算提交的作业总数

        # 初始化答案信息列表
        answers_info = []

        for answer in answers:
            # 获取与此答案关联的所有 Assignment
            assignments = Assignment.objects.filter(answer=answer)

            # 计算每个批阅人的得分和总得分
            total_grader_score = 0
            grader_scores = []
            for assignment in assignments:
                grader_score = compute_student_score(
                    assignment.student.performanceWeight,
                    assignment.student.engagementWeight,
                    8,  # 这里需要一个逻辑来确定 expected_score
                    assignment.student.rightnessWeight
                )
                grader_scores.append(grader_score)
                total_grader_score += grader_score

            # 计算每个批阅人的得分百分比
            grader_percentage = [score / total_grader_score for score in grader_scores] if total_grader_score > 0 else [0] * len(grader_scores)

            # 计算加权总分
            scores = [float(score) for score in answer.finalScore.split('￥！') if score]
            weighted_scores = [sum(score * perc for score, perc in zip(scores, grader_percentage))]
            total_score = sum(weighted_scores)

            # 添加答案信息
            answer_info = {
                'answerId': answer.answerId,
                'studentName': answer.studentId.userName,
                'studentNumber': answer.studentId.userId,
                'totalScore': total_score
            }
            answers_info.append(answer_info)

        return SuccessResponse('Course summary retrieved successfully.', {
            'studentCount': student_count,
            'totalSubmissions': total_submissions,
            'answersInfo': answers_info
        })

    except Teaching.DoesNotExist:
        return FailResponse('Teaching record not found.')
    except User.DoesNotExist:
        return FailResponse('Student record not found.')
    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))
    
@require_http_methods(["POST"])
def update_assignments_complaint(request):
    try:
        data = json.loads(request.body)
        answer_id = data.get('answerId')
        complaint = data.get('complaint')

        if not answer_id or not complaint:
            return FailResponse('缺少必要参数')

        # 获取与 answerId 相关的所有 Assignment 实例
        assignments = Assignment.objects.filter(answer_id=answer_id)

        # 检查是否已经提交过申诉
        if any(assignment.isAppealed for assignment in assignments):
            return FailResponse('您已经提交过申诉，请耐心等待')

        # 更新每个 Assignment 实例
        for assignment in assignments:
            assignment.isAppealed = 1
            assignment.appealContent = complaint
            assignment.save()

        return SuccessResponse('您的申诉已经受理，请耐心等待', {})

    except Exception as e:
        return FailResponse('未知错误！申诉失败！请稍后重试')

def compute_student_score(performance, engagement, expected_score, given_score, w1=1.0, w2=1.0, w3=1.0, epsilon=1e-5):
    """
    Compute a student's score based on performance, engagement, and the difference between expected and given scores.
    A small constant epsilon is used to avoid logarithm of zero.
    
    Parameters:
    - performance: Average or median score of the student's past homework.
    - engagement: Measure of student's engagement (e.g., speed or frequency of completing homework).
    - expected_score: The expected or true score for the homework.
    - given_score: The score given by the student.
    - w1, w2, w3: Weighting factors for the three components.
    - epsilon: A small constant to avoid log(0).

    Returns:
    - score: Computed score for the student.
    """
    # Ensure performance is positive to avoid log(0)
    performance = max(performance, epsilon)
    
    score = (w1 * np.log(performance) + 
             w2 * np.tanh(engagement) - 
             w3 * np.exp(-abs(expected_score - given_score)))
    return score

def aggregate_student_grades(student):
    assignments = Assignment.objects.filter(student=student)
    total_grade_sum = 0
    total_questions_count = 0

    for assignment in assignments:
        if assignment.grade:
            grades = assignment.grade.split('￥！')
            grades = [float(grade) for grade in grades if grade]
            total_grade_sum += sum(grades)
            total_questions_count += len(grades)

    # Calculate the average if there are grades, otherwise return 0
    return (total_grade_sum / total_questions_count) if total_questions_count > 0 else 0

def aggregate_student_scores(student):
    answers = Answer.objects.filter(studentId=student)
    total_score_sum = 0
    total_questions_count = 0

    for answer in answers:
        if answer.finalScore:
            scores = answer.finalScore.split('￥！')
            scores = [float(score) for score in scores if score]
            total_score_sum += sum(scores)
            total_questions_count += len(scores)

    # Calculate the average if there are scores, otherwise return 0
    return (total_score_sum / total_questions_count) if total_questions_count > 0 else 0


def assign_homework_to_students():
    unassigned_answers = Answer.objects.filter(whetherAssigned=False)

    for answer in unassigned_answers:
        # 获取与此答案相关的课程ID
        course_id = answer.homeworkId.courseId.courseId

        # 只考虑选择了相同课程的学生，他们的 roleType 为 2，并按已分配作业数量排序
        students = list(User.objects.filter(
            roleType=2,
            selecting__teachingId__courseId=course_id
        ).exclude(userId=answer.studentId.userId).distinct().order_by('assignedHomeworkCount'))

        # 只分配给前三个满足条件的学生
        for student in students[:3]:
            Assignment.objects.create(
                student=student,
                answer=answer,
                teacher=answer.homeworkId.teacherId,
                comments="",
                grade=""
            )

            # 更新学生的已分配作业数量
            student.assignedHomeworkCount += 1
            student.save()

        # 更新答案的分配状态
        answer.whetherAssigned = True
        answer.save()

@require_http_methods(["POST"])  # 限制这个视图只能通过POST请求调用
def assign_homework(request):
    # 这里你可以添加验证逻辑，例如验证用户是否有权限分配作业
    # if not request.user.has_perm('can_assign_homework'):
    #     return JsonResponse({'error': 'Permission denied'}, status=403)
    # 调用分配作业的逻辑
    assign_homework_to_students()
    return SuccessResponse('Answers retrieved successfully.',{})


@post_response(['studentId'])
@session_required()
def get_assignments_for_student(request, params, user: User):
    try:
        student_id = params.get('studentId')
        
        assignments = Assignment.objects.filter(
            student__userId=student_id
        ).select_related(
            'answer',
            'answer__homeworkId',  # Ensure this is the correct related_name
            'answer__homeworkId__courseId'
        )

        data = []
        for assignment in assignments:
            answer = assignment.answer
            if answer is None:
                continue  # 如果没有关联的答案，跳过这个分配

            homework = answer.homeworkId
            if homework is None:
                continue  # 如果没有关联的作业，跳过这个分配

            datum = {
                'assignmentId': assignment.assignmentId,
                'answerId': answer.answerId,
                'courseId': homework.courseId.courseId,
                'courseName': homework.courseId.courseName,
                'endTime': homework.endTime.strftime("%Y-%m-%d %H:%M:%S") if homework.endTime else None,
                'isFinished': assignment.isFinished,
                'startTime': homework.startTime.strftime("%Y-%m-%d %H:%M:%S") if homework.startTime else None,
                'studentId': assignment.student.userId,
                'teacherId': homework.teacherId.userId,
            }
            data.append(datum)
        
        return SuccessResponse('Assignments retrieved successfully.', data)

    except Exception as e:
        return FailResponse(str(e))

    
@post_response(['assignmentId'])
@session_required()
def get_assignment_details(request, params, user: User):
    try:
        assignment_id = params['assignmentId']
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        answer = assignment.answer
        student = assignment.student
        teacher = assignment.teacher
        homework = answer.homeworkId  # 根据外键关系获取 Homework 实例

        # 构造响应数据
        assignment_data = {
            'assignmentId': assignment.assignmentId,
            'startTime': homework.startTime.strftime("%Y-%m-%d %H:%M:%S") if homework.startTime else None,
            'endTime': homework.endTime.strftime("%Y-%m-%d %H:%M:%S") if homework.endTime else None,
            'isFinished': assignment.isFinished,
            'comments': assignment.comments,  # 添加 comments 字段
            'grade': assignment.grade,
            'studentDetails': {
                'userId': student.userId,
                'roleType': student.roleType,
                'userName': student.userName,
                'class_field': student.class_field,
                'userFace': student.userFace,
                'email': student.email,
            },
            'teacherDetails': {
                'userId': teacher.userId,
                'roleType': teacher.roleType,
                'userName': teacher.userName,
                'class_field': teacher.class_field,
                'userFace': teacher.userFace,
                'email': teacher.email,
            },
            'answerDetails': {
                'answer': answer.answer,
            },
            'homeworkDetails': {
                'content': homework.content,
            },
        }

        return SuccessResponse('Assignment details retrieved successfully.', [assignment_data])

    except Assignment.DoesNotExist:
        return FailResponse('Assignment not found.')
    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))

@post_response(['assignmentId', 'comments', 'grade'])
@session_required()
def update_assignment(request, params, user: User):
    # 从 POST 请求中获取参数
    assignment_id = params.get('assignmentId')
    comments = params.get('comments')
    grade = params.get('grade')

    try:
        # 获取 Assignment 实例
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        # 如果 assignment 的 isFinished 字段为 0，则处理评阅逻辑
        if assignment.isFinished == 0:
            # 更新 Assignment 实例的字段
            assignment.comments = comments
            assignment.grade = grade
            assignment.isFinished = True
            assignment.save()

            # 减少学生的被分配任务数量
            student = assignment.student
            student.assignedHomeworkCount = max(0, student.assignedHomeworkCount - 1)
            student.save()

            return SuccessResponse('Assignment updated successfully, and student task count decremented.', {})
        else:
            return FailResponse('Assignment has already been completed.')

    except Assignment.DoesNotExist:
        return FailResponse('Assignment not found.')
    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))


from django.utils import timezone
from django.db.models import Avg, Case, When, IntegerField

@post_response(['studentId'])
@session_required()
def update_student_weights(request, params, user: User):
    try:
        student_id = params['studentId']
        student = get_object_or_404(User, userId=student_id)

        # 计算 performanceWeight
        performance_weight = Answer.objects.filter(
            studentId=student
        ).aggregate(Avg('finalScore'))['finalScore__avg'] or 0

        # 计算 engagementWeight，如果当前系统时间大于endTime，并且任务isFinished为False，则扣2分
        now = timezone.now()
        engagement_weight = Assignment.objects.filter(
            student=student
        ).aggregate(
            late_penalty=Sum(
                Case(
                    When(Q(endTime__lt=now) & Q(isFinished=False), then=-2),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['late_penalty'] or 0

        # 计算 rightnessWeight，取学生打分的均值
        rightness_weight = Assignment.objects.filter(
            teacher=student
        ).aggregate(Avg('grade'))['grade__avg'] or 0

        # 更新学生权重
        student.performanceWeight = performance_weight
        student.engagementWeight = max(0, student.engagementWeight + engagement_weight)  # 防止权重为负
        student.rightnessWeight = rightness_weight
        student.save()

        return SuccessResponse('Student weights updated successfully.', {
            'performanceWeight': performance_weight,
            'engagementWeight': engagement_weight,
            'rightnessWeight': rightness_weight
        })

    except User.DoesNotExist:
        return FailResponse('Student not found.')
    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))
    

@post_response([])
@session_required()
def update_all_students_weights(request, params, user: User):
    try:
        # 获取所有学生用户
        students = User.objects.filter(roleType=0)
        now = timezone.now()

        # 遍历所有学生，计算并更新权重
        for student in students:
            # 计算 performanceWeight
            performance_weight = aggregate_student_scores(student)
            # 计算 engagementWeight
            engagement_weight = Assignment.objects.filter(
                student=student
            ).annotate(
                penalty=Case(
                    When(Q(endTime__lt=now) & Q(isFinished=False), then=-2),
                    default=0,
                    output_field=IntegerField()
                )
            ).aggregate(total_penalty=Sum('penalty'))['total_penalty'] or 0

            # 计算 rightnessWeight
            rightness_weight = aggregate_student_grades(student)

            # 更新学生权重
            student.performanceWeight = performance_weight
            student.engagementWeight = max(0, engagement_weight)  # 确保不会有负数的权重
            student.rightnessWeight = rightness_weight
            student.save()

        return SuccessResponse('All student weights updated successfully.', {})

    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))

def get_final_score():
    answers = Answer.objects.all()
    
    for answer in answers:
        # 如果 whetherAssigned 为 0，跳过这个答案
        if not answer.whetherAssigned:
            continue

        assignments = Assignment.objects.filter(answer=answer)
        sub_question_grades = []
        total_weight = 0

        # Calculate weights for each assignment
        weights = []
        for assignment in assignments:
            # 确保 grade 是数字类型
            try:
                given_score = float(assignment.grade)
            except ValueError:
                # 如果 grade 无法转换为 float，跳过这个 assignment
                continue

            performance = assignment.student.performanceWeight
            engagement = assignment.student.engagementWeight
            expected_score = 8  # 根据实际情况调整
            weight = compute_student_score(performance, engagement, expected_score, given_score)
            weights.append(weight)
            total_weight += weight

        # Process each assignment
        for assignment, weight in zip(assignments, weights):
            if assignment.grade:
                grades = [float(g) for g in assignment.grade.split('￥！') if g]
                
                # Extend the list with grades from this assignment
                while len(sub_question_grades) < len(grades):
                    sub_question_grades.append([])

                # Add weighted grades to sub_question_grades
                for i, grade in enumerate(grades):
                    weighted_grade = (grade * weight) / total_weight if total_weight else 0
                    sub_question_grades[i].append(weighted_grade)

        # Calculate final grades for each sub-question
        final_grades = [str(sum(grades)) for grades in sub_question_grades]

        # Update finalScore
        answer.finalScore = '￥！'.join(final_grades)
        answer.save()

@require_http_methods(["POST"])
def update_final_scores(request):
    try:
        # 如果需要接收特定数据，可以从request.body中解析
        # data = json.loads(request.body)
        # answer_id = data.get('answerId')

        # 调用函数更新分数
        get_final_score()

        # 返回成功响应
        return JsonResponse({'status': 'success', 'message': 'Final scores updated successfully'}, status=200)

    except Exception as e:
        # 返回错误响应
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


        
@require_http_methods(["GET"])
def get_courses_by_teacher(request):
    teacher_id = request.GET.get('teacherId')
    if not teacher_id:
        return FailResponse('No teacherId provided.')

    try:
        # 获取与此 teacherId 关联的所有 Teaching 实例
        teachings = Teaching.objects.filter(teacherId=teacher_id).select_related('courseId')

        # 提取所有相关联的 courseId 和 courseName
        courses = [{'courseId': teaching.courseId.courseId, 'courseName': teaching.courseId.courseName} for teaching in teachings]

        return SuccessResponse('Courses retrieved successfully.', {
            'courses': courses
        })

    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))
    
@require_http_methods(["GET"])
def get_courses_by_student(request):
    student_id = request.GET.get('studentId')
    if not student_id:
        return FailResponse('No studentId provided.')

    try:
        # 获取与此 studentId 关联的所有 Selecting 实例
        selectings = Selecting.objects.filter(studentId=student_id).select_related('teachingId__courseId')

        # 提取所有相关联的 courseId 和 courseName
        courses = [{'courseId': selecting.teachingId.courseId.courseId, 'courseName': selecting.teachingId.courseId.courseName} for selecting in selectings]

        return SuccessResponse('Courses retrieved successfully for student.', {
            'courses': courses
        })

    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))


