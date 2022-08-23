from django.db.models import Q
from itsdangerous import TimedSerializer
from accounts.models import *
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.forms import LoginForm, SignupForm
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.serializers import *
from flexoffice.permissions import HRAndAdminPermA, CreateUserPermission
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes,APIView
from django.http import HttpResponse,HttpResponseGone,response
from accounts.serializers import TimeSerializer
class LogInViewSets(viewsets.ViewSet):
    permission_classes = [AllowAny, ]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        form = LoginForm(request=request, data=request.data)
        print(request.data.get('username'), "request.data('username')")
        request.session['username']=request.data.get('username')
        print(request.session['username'], "request.session['username']")
        if form.is_valid():
            token, created = Token.objects.get_or_create(user=form.get_user())
            return Response({'message': 'Login successful...', 'token': token.key,
                             'success': 'True',
                             'is_superuser': form.get_user().is_superuser},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpViewSets(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]
    print('___ABHINANDAN')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('password') is None:
            password = f"PASSWORD{request.data.get('username')}"
        else:
            password = request.data.pop('password')
        request.data['password2'] = password
        request.data['password1'] = password
        request.data['full_name'] = f"{request.data.get('first_name')} {request.data.get('last_name')}"
        form = SignupForm(data=request.data)
        if form.is_valid():
            data = form.save()
            if User.objects.filter(username=data.username).exists():
                serializer = UserSerializer(data)
                token, created = Token.objects.get_or_create(user=data)
                response = {'message': 'Sign-In Successful...', 'token': token.key, 'user': serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
        return Response({'error': form.errors}, status=status.HTTP_206_PARTIAL_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    # permission_classes = (AllowAny,)
    queryset = User.objects.all()
    print('___ABHINANDAN')
    serializer_class = UserSerializer
    permission_classes = [HRAndAdminPermA, CreateUserPermission]
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('full_name', 'username', 'user_type')

    def put(self, request, *args, **kwargs):
        paras = request.query_params.get('id')
        if paras is None:
            pk = request.data.get('id')
            try:
                record = User.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response({'error': 'Record Not Found..'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(record, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if User.objects.filter(pk=paras).exists():
                print('___ABHINANDAN')
                user_data = User.objects.get(pk=paras)
                serializer = UserSerializer(user_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({'error': 'Record Not Found..'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        pk = request.query_params.get('id')
        try:
            User.objects.get(pk=pk).delete()
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'Employee Deleted.'}, status=status.HTTP_200_OK)


class GetUserOnlyViewSet(viewsets.ModelViewSet):

    queryset = User.objects.filter(Q(user_type='H') | Q(user_type='E'), is_active=True).exclude(is_superuser=True,)
    serializer_class = UserSerializer
    http_method_names = ['get']
    permission_classes = [HRAndAdminPermA, ]


class LoginApiTracker(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.session['email'] = request.data.get('email')
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'session': request.session['email']
        }
        status_code = status.HTTP_200_OK
        
        return Response(response, status=status_code)



# from rest_framework.permissions import AllowAny
# @api_view(['POST'])  
# def time_user(request):
#     permission_classes = [AllowAny, ] 
#     get_username=request.data['username']
#     print(get_username)
#     if request.method == "POST":
#         get_start=request.data['start']
#         print(get_start,"------ GET START --------")
#         get_stop=request.data['stop']
#         print(get_stop,"------- GET STOP ----------")
#         serializer=TimerSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("succesfully ")
#         return HttpResponse('Please confirm your email addres o complete the registration') 


class TimeTracker(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, format=None):    
        userapp = User.objects.filter(username='abhinandan').get()
        start= request.query_params['start']
        if 'stop' in request.query_params:
            # print(request.query_params)
            stop = request.query_params['stop']
        else:
            stop = None

        if 'timespent' in request.query_params:
            timespent = request.query_params['timespent']
        else:
            timespent = None
            
            
        if Timer.objects.filter(user_id=userapp.id).exists():
            user = Timer.objects.get(user_id=userapp.id)
            print(user, 'username check krna')
            user.start=start
            user.stop=stop
            user.timespent=timespent
            user.save()
            response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Successfully Updated',
                    'data':'serializer.data'
                    }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        else:
            user= Timer.objects.create(start=start,user_id=userapp.id,stop=stop,timespent=timespent)
            response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Successfully Added',
            'data':'sss'
            }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)


