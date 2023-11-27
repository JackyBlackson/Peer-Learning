from PeerLearningAPP.models import Answer, Homework
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
import json
from django.db.models import Q,Max
from PeerLearningAPP.models import Homework, User,Answer
from PeerLearningAPP.utilities.request_util import SuccessResponse, FailResponse
from PeerLearningAPP.models import Answer, Assignment, Homework

@require_http_methods(["GET"])
def get_answer_details(request):
    answer_id = request.GET.get('answerId')
    # if not answer_id:
    #     return FailResponse('No answerId provided.')

    
        # 获取对应的 Answer 实例
    answer = Answer.objects.get(pk=answer_id)
    answer_data = {
        'finalScore': answer.finalScore,
        'gptSim': answer.gptSim,
        'otherSim': answer.otherSim,
        'answer':answer.answer
    }

    # 获取与此 Answer 关联的所有 Assignment 的 comments
    assignments = Assignment.objects.filter(answer=answer)
    comments = []
    

    joined_comments = "     \n".join(comments)

    # 获取关联的 Homework 的 stdAns 和 content
    homework = answer.homeworkId
    homework_data = {
        'stdAns': homework.standAns,
        'content': homework.content
    }

    return SuccessResponse('Answer details retrieved successfully.', {
        'answerData': answer_data,
        'comments': joined_comments,
        'homeworkData': homework_data
    })






@require_http_methods(["POST"])
def create_answer(request):

    data = json.loads(request.body)

    # 检查是否存在相同 homeworkId 和 studentId 的答案
    existing_answer = Answer.objects.filter(
        homeworkId=data['homeworkId'], 
        studentId_id=data['studentId']
    ).first()

    if existing_answer:
        # 如果存在，更新现有答案
        existing_answer.answer = data.get('answer', '')
        existing_answer.finalScore = data.get('finalScore', -1)
        existing_answer.save()
        message = 'Answer updated successfully.'
    else:
        # 如果不存在，创建新答案
        homework = Homework.objects.get(pk=data['homeworkId'])

        # 获取当前最大的 answerId
        max_answer_id = Answer.objects.all().aggregate(Max('answerId'))['answerId__max'] or 0
        new_answer_id = max_answer_id + 1

        existing_answer = Answer.objects.create(
            answerId=new_answer_id,
            homeworkId=homework,
            answer=data.get('answer', ''),
            studentId_id=data['studentId'],
            finalScore=data.get('finalScore', -1)
        )
        message = 'Answer created successfully.'

    return SuccessResponse(message, model_to_dict(existing_answer))



# Delete an answer
@require_http_methods(["POST"])
def delete_answer(request):
    try:
        data = json.loads(request.body)
        Answer.objects.get(pk=data['answerId']).delete()
        return SuccessResponse('Answer deleted successfully.', {})
    except Answer.DoesNotExist:
        return FailResponse('Answer not found.')


# Search for answers
# Update an answer
@require_http_methods(["POST"])
def update_answer(request):
    try:
        data = json.loads(request.body)
        answer = Answer.objects.get(pk=data['answerId'])

        # Update the provided fields
        update_fields = []
        for field in ['answer']:
            if field in data:
                setattr(answer, field, data[field])
                update_fields.append(field)

        # Save the changes
        answer.save(update_fields=update_fields)

        return SuccessResponse('Answer updated successfully.', model_to_dict(answer))
    except Answer.DoesNotExist:
        return FailResponse('Answer not found.')

