# # coding=utf-8

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch
# # 加载模型和令牌化器
# MODEL_PATH = "/bjtu_shixun/peer_learning/src/PeerLearningSystemProject/PeerLearningAPP/pretrained_model/gptzzz/model_config"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# def check_Gpt_util(target, model, tokenizer):
#     text = target
#     inputs = tokenizer(text, return_tensors='pt')
#     with torch.no_grad():
#         outputs = model(**inputs)
#     if outputs.logits[0][0] > outputs.logits[0][1]:
#         print("human")
#         return 0
#     else:
#         print("gpt")
#         return 1
    
    
   


