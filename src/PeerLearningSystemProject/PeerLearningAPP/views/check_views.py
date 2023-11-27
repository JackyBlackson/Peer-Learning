from PeerLearningAPP.models import User, Answer  # Make sure you import Answer or whatever the model's name is.
import json
from django.shortcuts import render
from django.http import JsonResponse
import requests
import django.http.request
from PeerLearningAPP.utilities.request_util import JsonRes
from django.views.decorators.http import require_http_methods
import json
from PeerLearningAPP.pretrained_model.simhash.tests.test_simhash import *
from PeerLearningAPP.pretrained_model.gptzzz.gptCheck import *
from PeerLearningAPP.models import User
import PeerLearningAPP.middleware.user.token_middleware as token_middleware
from PeerLearningAPP.models import Answer
from PeerLearningAPP.utilities.request_util import SuccessResponse, FailResponse
import json

@require_http_methods(["POST"])
def SimhashDetect(request):
    if request.method != "POST":
        return FailResponse("Invalid request method.")

    body = json.loads(request.body)
    answerId = body.get("answerId")

    if answerId is None:
        return FailResponse("AnswerId not provided")

    try:
        target_answer = Answer.objects.get(pk=answerId)
        totalanswer_target = target_answer.answer
        max_similarity = 0
        similar_answer_id = None

        for answer in Answer.objects.exclude(pk=answerId):
            totalanswer = answer.answer.replace("￥！", "")
            similarity = checkSim(totalanswer_target, totalanswer)
            if similarity > max_similarity:
                max_similarity = similarity
                similar_answer_id = answer.answerId

        if max_similarity > 30:
            target_answer.otherSim = max_similarity
            target_answer.save()
            message = f"Found similar answer with id {similar_answer_id}, and similarity is {max_similarity}%"
            return SuccessResponse(message, {"maxSimilarity": max_similarity, "similarAnswerId": similar_answer_id})
        else:
            return SuccessResponse("No similar answers found above threshold.", {"maxSimilarity": max_similarity})

    except Answer.DoesNotExist:
        return FailResponse(f"No answer found with id {answerId}")
    except Exception as e:
        return FailResponse(f"An error occurred: {str(e)}")

def gptDetect(request):
    if request.method == "POST":
        body = json.loads(request.body)
        answerId = body.get("answerId")
        
        message = ""
        description = "No GPT-related content detected."  # Default description
        data = {}
        success = True
        
        if answerId is not None:
            try:
                target_answer = Answer.objects.get(pk=answerId)
                if not target_answer:
                    message = f"No answer found with id {answerId}"
                else:
                    answers_to_check = target_answer.answer.split('￥！')
                    gpt_related_found = False  # Flag to track if GPT-related content is found
                    
                    # for ans in answers_to_check:
                        # if check_Gpt_util(ans, model, tokenizer) == 1:
                        #     message = f"Answer contains information that might be generated by GPT."
                        #     description = "Detected content that might be generated by GPT."
                        #     gpt_related_found = True
                        #     break
                    
                    # If GPT-related content is found, update gptSim field
                    # if gpt_related_found:
                    #     target_answer.gptSim = 1.0  # You can set the similarity value accordingly
                    #     target_answer.save()  # Save the updated object
            except Exception as e:
                message = f"An error occurred: {str(e)}"
                success = False
        else:
            message = "AnswerId not provided"
            success = False
            

        
        res = {
            "status": success,
            "message": message,
            "description": description,  # Add the description to the response
            "code": 200 if success else 400,
            "data": [data]
        }
        
        return JsonRes(res)
    else:
        return JsonRes({"error": "Invalid request method."})
    

def queryAi(request):
    if request.method == "POST":
        # 从POST请求中获取'question'参数
        body = json.loads(request.body)
        question = body.get('question')

        # 初始化返回值
        success = False
        message = ""
        data = {}

        if question:
            # 云端AI的URL
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=24.1e99ca46c4b97044dde1b1bb803d08aa.2592000.1703258838.282335-39332759"
            ai_identity = "你好，假如你是一名悉心的家庭教师助手，我希望你能够回答我的一些问题（以上是提示词信息）: "
            full_question = ai_identity + question

            # 创建请求载荷
            payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": full_question
                    }
                ]
            })

            headers = {
                'Content-Type': 'application/json'
            }

            # 向云端AI发送请求
            response = requests.post(url, headers=headers, data=payload)


            answer = requests.request("POST", url, headers=headers, data=payload).text

            if answer:
                success = True
                message = "Successfully fetched answer from AI."
                data["answer"] = answer
                answer_data = json.loads(answer)
                result = answer_data.get("result")
            else:
                message = "Failed to get answer from AI."

        else:
            message = "Question parameter is missing."

        res = {
            "status": success,
            "description": message,
            "code": 200 if success else 400,
            "data": result  # 根据您提供的格式，将数据放在一个数组中
        }

        return JsonRes(res)
    else:
        return JsonRes({"error": "Invalid request method."})