import random
from django.shortcuts import render
from django.http import JsonResponse
import django.http.request
from PeerLearningAPP.utilities.request_util import JsonRes
import json
from PeerLearningAPP.models import User, Assignment, Course, Teaching, Homework, Answer, Selecting
import PeerLearningAPP.middleware.user.token_middleware as token_middleware
from PeerLearningAPP.utilities.request_util import post_response, get_response, SuccessResponse, FailResponse , session_required, role_required, role
import PeerLearningAPP.views.assignment_views as assign

# 1. 为某一个课程生成作业记录
# 2. 为某一个作业遍历所有成员生成答案
# 3. 为作业分配批改任务
# 4. 为每一个任务生成批改记录
# 5. 。。。

NONES = ["你", "我", "他", "你们", "我们", "他们", "原神", "米哈游", "米国", "美利坚", "星铁", "元神"]
ADJECTIVES = ["可恶的", "可怕的", "超级的", "聪明的", "无所不用其极的", "可笑的", "奇葩的"]
ADVERBS = ["狡猾地", "很快地", "罪大恶极地", "千方百计地", "可怜地", "苦苦", "漫不经心地", "满脸不屑地"]
VERBS = ["欺骗", "负责", "忽悠", "吸引", "奈何", "惩罚"]
ASKS = ["怎么", "如何", "怎样", "哪样", "通过甚么途径"]
ENDS = ["了", "吗", "了吗", "啊"]
POINTS = ["?", "!", "?!"]
SPLITER = "￥！"

@get_response(["course_id"])
def generate_data_view(request, params):
# def generate_data_view(request):
    course_id = int(params["course_id"])
    # course_id = 1113
    if(len(Course.objects.filter(courseId = course_id)) != 1):
        return FailResponse(f"id 为 {course_id} 的课程不存在")
    generate_all(course_id)
    return SuccessResponse(f"成功 id 为 {course_id} 课程生成数据！", {})

def generate_all(course_id : int):
    homework = generate_homework(course_id)
    generate_answer(homework)
    make_assignment()
    generate_assignment(homework)
    calculte_final_score()
    
    


def generate_homework(course_id : int) -> Homework:
    course = Course.objects.get(courseId = course_id)
    teacher = Teaching.objects.get(courseId = course.courseId).teacherId
    # 获取当前HomeworkId的最大值
    all_homeworks = Homework.objects.all()
    max_homeworkId = 0
    for homework in all_homeworks:
        if homework.homeworkId > max_homeworkId:
            max_homeworkId = homework.homeworkId
    homework = Homework.objects.create(
            teacherId=teacher,
            homeworkId=max_homeworkId+1,
            content=generate_homework_content(),
            courseId=course
        )
    return homework

def generate_answer(homework : Homework):
    all_answer = Answer.objects.all()
    max_answerId = 0
    for answer in all_answer:
        if answer.answerId > max_answerId:
            max_answerId = answer.answerId
    question_count = count_questions(homework.content)
    all_selectings = Selecting.objects.filter(teachingId = Teaching.objects.get(courseId = homework.courseId))
    for selecting in all_selectings:
        max_answerId += 1
        Answer.objects.create(
                answerId = max_answerId,
                homeworkId=homework,
                answer=generate_answer_content(question_count),
                studentId=selecting.studentId,
                finalScore=-1,
                # performanceWeight=data.get('performanceWeight', 0),
                # engagementWeight=data.get('engagementWeight', 0),
                # rightnessWeight=data.get('rightnessWeight', 0)
            )
        
        
    
def make_assignment() -> bool:
    assign.assign_homework_to_students()
    
def generate_assignment(homework : Homework):
    relevant_answers = Answer.objects.filter(homeworkId = homework)
    relevant_assignments = Assignment.objects.filter(answer__in=relevant_answers)
    relevant_assignments_with_related_data = relevant_assignments.select_related('student', 'answer', 'teacher')
    for assignment in relevant_assignments_with_related_data:
        comment = random_ask_sentence()
        Assignment.objects.filter(assignmentId = assignment.assignmentId).update(
            isFinished = 1,
            grade = generate_grades(homework),
            comments = f"<p>{comment}</p>"
        )
        
def calculte_final_score():
    assign.get_final_score()
    
def count_questions(content : str) -> int:
    return content.count(SPLITER) + 1

def generate_grades(homework : Homework) -> str:
    count = count_questions(homework.content)
    grades = []
    for i in range(count):
        grades.append(str(random.randint(1,int(100/count))))
    return SPLITER.join(grades)
    
def generate_homework_content() -> str:
    question_size = random.randint(1, 5)
    qs = []
    for i in range(question_size):
        qs.append(random_ask_sentence())
    return SPLITER.join(qs)

def generate_answer_content(count : int) -> str:
    question_size = random.randint(1, 5)
    qs = []
    for i in range(count):
        qs.append(random_ask_sentence())
    return SPLITER.join(qs)
        
    
    
def random_ask_sentence() -> str:
    result = ""
    if random_bool() :
        result += random.choice(ADJECTIVES)
    result += random.choice(NONES)
    result += random.choice(ASKS)
    if random_bool() :
        result += random.choice(ADVERBS)
    result += random.choice(VERBS)
    if random_bool() :
        result += random.choice(ADJECTIVES)
    result += random.choice(NONES)
    result += random.choice(ENDS)
    result += random.choice(POINTS)
    return result
    
    
def random_bool() -> bool:
    return random.choice([True, False])