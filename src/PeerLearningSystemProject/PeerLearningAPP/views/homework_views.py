from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.db.models import Max
import json
from django.utils import timezone
from django.db.models import Q
from PeerLearningAPP.models import User, Course, Teaching, Answer, Selecting,Homework
from PeerLearningAPP.utilities.request_util import SuccessResponse, FailResponse,get_response

# List all homeworks
def list_homeworks(request):
    homeworks = Homework.objects.select_related('teacherId').all()
    homework_list = []

    for hw in homeworks:
        teacher_name = hw.teacherId.userName if hw.teacherId else "Unknown"

        homework_list.append({
            "homeworkId": hw.homeworkId,
            "teacherId": hw.teacherId_id,
            "teacherName": teacher_name,
            "startTime": hw.startTime.strftime("%Y-%m-%d") if hw.startTime else None,
            "endTime": hw.endTime.strftime("%Y-%m-%d") if hw.endTime else None,
        })

    return SuccessResponse("List of all homeworks", homework_list)

@require_http_methods(["POST"])
def create_homework(request):
    
    data = json.loads(request.body)

    # 查询当前最大的 homeworkId
    max_homework_id = Homework.objects.all().aggregate(Max('homeworkId'))['homeworkId__max']
    new_homework_id = (max_homework_id or 0) + 1  # 如果没有现有记录，则从 1 开始

    # 获取 Course 实例
    course_instance = Course.objects.get(courseId=data['courseId'])

    # 创建 Homework 实例，手动设置 homeworkId
    homework = Homework.objects.create(
        homeworkId=new_homework_id,  # 设置 homeworkId
        teacherId_id=data['teacherId'],
        content=data.get('content', ''),
        courseId=course_instance,
        startTime=data.get('startTime'),
        standAns=data.get('standAns'),
        endTime=data.get('endTime'),
        homeworkDes=data.get('homeworkDes', '')
    )
    return SuccessResponse('Homework created successfully.', {})

# Delete a homework
@require_http_methods(["POST"])
def delete_homework(request):
    try:
        data = json.loads(request.body)
        Homework.objects.get(homeworkId=data['homeworkId']).delete()
        return SuccessResponse('Homework deleted successfully.', {})
    except Homework.DoesNotExist:
        return FailResponse('Homework not found.')



@require_http_methods(["POST"])
def update_homework_partial(request):
    try:
        data = json.loads(request.body)
        homework = Homework.objects.get(homeworkId=data['homeworkId'])

        update_fields = []
        for field in ['content', 'courseId', 'whetherAssigned', 'startTime', 'endTime', 'homeworkDes']:  # 添加 homeworkDes
            if field in data:
                setattr(homework, field, data[field])
                update_fields.append(field)

        homework.save(update_fields=update_fields)
        return SuccessResponse('Homework updated successfully.', model_to_dict(homework))
    except Homework.DoesNotExist:
        return FailResponse('Homework not found.')


from django.http import JsonResponse

@require_http_methods(["GET"])
def showHomeWork(request):
    # Getting the homeworkId from the GET request
    homework_id = request.GET.get('homeworkId')
    if not homework_id:
        return FailResponse('No homeworkId provided.')

    try:
        # Retrieve the homework based on homeworkId
        homework = Homework.objects.get(homeworkId=homework_id)
        
        # Prepare the response data
        homework_data = {
            'homeworkId': homework.homeworkId,
            'teacherId': homework.teacherId_id,
            'content': homework.content,
            'homeworkDes':homework.homeworkDes
        }
        
        # If the teacher is associated, fetch the teacher's name
        if homework.teacherId:
            homework_data['teacherName'] = homework.teacherId.userName

        return SuccessResponse('Homework details retrieved successfully.', homework_data)
    except Homework.DoesNotExist:
        return FailResponse('Homework not found.')


@require_http_methods(["GET"])
def get_homeworks_by_course(request):
    course_id = request.GET.get('courseId')
    if not course_id:
        return FailResponse('No courseId provided.')

    try:
        # 获取当前时间
        current_time = timezone.now()

        # 获取与此 courseId 关联的所有 Homework 实例
        homeworks = Homework.objects.filter(courseId=course_id)

        # 提取所有相关的作业信息
        homework_info = []
        for hw in homeworks:
            # 判断作业状态
            status = ""
            if hw.startTime and hw.endTime:
                if current_time < hw.startTime:
                    status = "未开始"
                elif hw.startTime <= current_time <= hw.endTime:
                    status = "进行中"
                else:
                    status = "已结束"

            homework_data = {
                'homeworkId': hw.homeworkId,
                'startTime': hw.startTime.strftime("%Y-%m-%d %H:%M:%S") if hw.startTime else None,
                'endTime': hw.endTime.strftime("%Y-%m-%d %H:%M:%S") if hw.endTime else None,
                'homeworkDes': hw.homeworkDes,
                'nowStatus': status
            }
            homework_info.append(homework_data)

        return SuccessResponse('Homeworks retrieved successfully for course.', {
            'homeworks': homework_info
        })

    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))
    

@require_http_methods(["GET"])
def get_homeworks_by_course_forStu(request):
    # Getting the query parameters
    course_id = request.GET.get('courseId')
    student_id = request.GET.get('studentId')
    
    if not course_id or not student_id:
        return FailResponse('No courseId or studentId provided.')

    try:
        # 获取当前时间
        current_time = timezone.now()

        # 获取与此 courseId 关联的所有 Homework 实例
        homeworks = Homework.objects.filter(courseId=course_id)

        # 提取所有相关的作业信息
        homework_info = []
        for hw in homeworks:
            # 获取学生提交的答案ID
            student_answer = Answer.objects.filter(homeworkId=hw.homeworkId, studentId=student_id).first()
            answer_id = student_answer.answerId if student_answer else None

            # 判断作业状态
            if hw.startTime and hw.endTime:
                if current_time < hw.startTime:
                    status = "未开始"
                elif hw.startTime <= current_time <= hw.endTime:
                    status = "进行中"
                elif current_time > hw.endTime and answer_id is None:
                    status = "超时未提交"
                elif current_time > hw.endTime:
                    status = "已结束"
            else:
                status = "状态未知"

            homework_data = {
                'homeworkId': hw.homeworkId,
                'startTime': hw.startTime.strftime("%Y-%m-%d %H:%M:%S") if hw.startTime else None,
                'endTime': hw.endTime.strftime("%Y-%m-%d %H:%M:%S") if hw.endTime else None,
                'homeworkDes': hw.homeworkDes,
                'nowStatus': status,
                'answerId': answer_id
            }
            homework_info.append(homework_data)

        return SuccessResponse('Homeworks retrieved successfully for course.', {
            'homeworks': homework_info
        })

    except Exception as e:
        return FailResponse('Unexpected error occurred: ' + str(e))
    
@get_response(['course', 'class', 'teacher'])
def get_score_distribution(request, params):
    
    course_name = params.get('course')
    class_field = params.get('class')
    teacher_name = params.get('teacher')

    # 构建查询条件
    query = Q()
    if course_name:
        course_ids = Course.objects.filter(courseName=course_name).values_list('courseId', flat=True)
        query &= Q(homeworkId__courseId__in=course_ids)

    if class_field:
        query &= Q(studentId__class_field=class_field)

    if teacher_name:
        teacher_ids = User.objects.filter(userName=teacher_name, roleType=1).values_list('userId', flat=True)
        teaching_ids = Teaching.objects.filter(teacherId__in=teacher_ids).values_list('teachingId', flat=True)
        query &= Q(studentId__selecting__teachingId__in=teaching_ids)

    # 查询满足条件的答案
    answers = Answer.objects.filter(query)
    total_answers = answers.count()

    # 分数段统计
    score_distribution = {'gradeNum1': 0, 'gradeNum2': 0, 'gradeNum3': 0, 'gradeNum4': 0, 'gradeNum5': 0}
    for answer in answers:
        total_score = sum([float(score) for score in answer.finalScore.split('￥！') if score])

        if total_score >= 90:
            score_distribution['gradeNum1'] += 1
        elif 80 <= total_score < 90:
            score_distribution['gradeNum2'] += 1
        elif 70 <= total_score < 80:
            score_distribution['gradeNum3'] += 1
        elif 60 <= total_score < 70:
            score_distribution['gradeNum4'] += 1
        else:
            score_distribution['gradeNum5'] += 1

    # 转换为百分比
    for key in score_distribution:
        score_distribution[key] = (score_distribution[key] / total_answers) * 100 if total_answers > 0 else 0

    return SuccessResponse('Score distribution retrieved successfully.', score_distribution)
    

    


    

    

    

