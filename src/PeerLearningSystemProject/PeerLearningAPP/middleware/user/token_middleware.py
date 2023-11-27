from PeerLearningAPP.utilities.basic_util import generate_random_string
from PeerLearningAPP.models import User


# def generate_token() -> str:
#     loop = True
#     while(loop):
#         token = generate_random_string(64)
#         if (not User.objects.filter(token = token).exists()):
#             loop = False
    
#     return token

# def check_token(token:str) -> User:
#     if(token == "NULL_NOT_LOGIN"):
#         return None
#     u = User.objects.filter(token = token)
#     if(u.exists()):
#         return u[0]
#     else:
#         return None