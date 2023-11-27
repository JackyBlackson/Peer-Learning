from django.middleware.security import SecurityMiddleware
from django.utils.deprecation import MiddlewareMixin
class MyCorsMiddle(MiddlewareMixin):
    def process_response(self, request, response):
        # if request.method == 'OPTIONS':
        #     # 允许Content-Type类型
        #     # response['Access-Control-Allow-Headers'] = 'Content-Type'
        #     # 允许所有的header
        #     response['Access-Control-Allow-Headers']='*'
        #     # 允许某个ip+port
        #     # obj['Access-Control-Allow-Origin']='http://127.0.0.1:8000'
        # if request.method == 'OPTIONS':
        #     response['Access-Control-Allow-Headers'] = '*'  # 允许所有的header
        #     response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        allowed_origins = ['http://127.0.0.1:8080', 'http://127.0.0.1:8000', 'http://localhost:8080', 'http://localhost:8000', 'http://152.136.42.139:8000/']
        #origin = request.headers['Origin']
        print(request.headers)
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response['Access-Control-Allow-Credentials'] = 'true'  # 允许发送cookies
        return response