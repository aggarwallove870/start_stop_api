from django.db.models import Q
from datetime import datetime, date
from flexoffice_app.serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from accounts.serializers import ResultsSetPagination
from django.core.exceptions import ObjectDoesNotExist
from flexoffice.permissions import HRAndAdminPermA
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter


class AttendanceSheetViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSheet.objects.all().order_by('id')
    serializer_class = AttendanceSheetSerializer
    permission_classes = [HRAndAdminPermA, ]
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'attendance_date',)

    def create(self, request, *args, **kwargs):

        try:
            attendance_date = request.data.get('attendance_date')
            attendance_id = request.data.get('id')
            if attendance_date:
                date_value = datetime.strptime(attendance_date, '%Y-%m-%d')
                if date_value > datetime.now():
                    return Response({"error": "Can't create more then current date."},
                                    status=status.HTTP_510_NOT_EXTENDED)
                if AttendanceSheet.objects.filter(attendance_date=date_value):
                    attendance_data = AttendanceSheet.objects.get(attendance_date=date_value)
                else:
                    attendance_data = AttendanceSheet.objects.create(attendance_date=attendance_date)
            elif attendance_id and AttendanceSheet.objects.filter(id=attendance_id).exists():
                attendance_data = AttendanceSheet.objects.get(id=attendance_id)
            else:
                if AttendanceSheet.objects.filter(attendance_date=date.today()).exists():
                    attendance_data = AttendanceSheet.objects.get(attendance_date=date.today())
                else:
                    attendance_data = AttendanceSheet.objects.create(attendance_date=date.today())
            serializer = AttendanceSheetSerializer(attendance_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Attendance not created.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        pk = request.data.get('id')
        request.data['attended_by'] = request.user.id
        if request.data.get('holiday') is not None:
            if AttendanceSheet.objects.filter(id=request.data['id']).exists():
                sheet_id = request.data['id']
                data = AttendanceSheet.objects.get(id=sheet_id)
                data.is_holiday = bool(request.data['holiday'])
                data.save()
                serializer = AttendanceSheetSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Record Not Found..'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            record = Attendance.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found..'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('id')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'attendance_date',)

    def get_queryset(self):
        month = self.request.query_params.get('_month')
        year = self.request.query_params.get('_year')
        if month and year:
            queryset = Attendance.objects.filter(employee=self.request.user, attendance_date__month=int(month),
                                                 attendance_date__year=int(year)).order_by('id')
            return queryset
        else:
            if Attendance.objects.filter(employee=self.request.user, attendance_date=date.today()).exists():
                queryset = Attendance.objects.filter(employee=self.request.user, attendance_date=date.today()).order_by(
                    'id')
            else:
                queryset = Attendance.objects.create(employee=self.request.user, attendance_date=date.today())
        return queryset

    def put(self, request, *args, **kwargs):
        pk = request.data.get('id')
        if request.data.get('check_in') is not None or request.data.get('check_out') is not None:
            if pk:
                attendance_user = Attendance.objects.get(id=pk)
            else:

                if Attendance.objects.filter(employee=request.user, attendance_date=date.today()).exists():
                    attendance_user = Attendance.objects.get(employee=request.user, attendance_date=date.today())
                else:
                    attendance_user = Attendance.objects.create(employee=request.user, attendance_date=date.today())

            if request.data.get('check_in') is not None:
                if attendance_user.check_in is None:
                    attendance_user.check_in = datetime.now()
                else:
                    return Response({"error": "You already check in."}, status=status.HTTP_510_NOT_EXTENDED)
            if request.data.get('check_out') is not None:
                if attendance_user.check_out is None:
                    attendance_user.check_out = datetime.now()
                else:
                    return Response({"error": "You already check out."}, status=status.HTTP_510_NOT_EXTENDED)
            attendance_user.save()
            serializer = AttendanceSerializer(attendance_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendanceDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(Q(user_type='H') | Q(user_type='E'), is_active=True).exclude(
        is_superuser=True, ).order_by('id')
    serializer_class = AttendanceDetailSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get']
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'username', 'full_name')

    def get_serializer_context(self):
        return {'month': self.request.query_params.get('_month'), 'year': self.request.query_params.get('_year')}

    def get_queryset(self):
        if self.request.user.user_type != 'E':
            return self.queryset
        else:
            queryset = User.objects.filter(id=self.request.user.id).order_by('id')
            return queryset


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all().order_by('id')
    serializer_class = SalarySerializer
    permission_classes = [HRAndAdminPermA]
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    # search_fields = ('full_name', 'username', 'user_type')

    def put(self, request, *args, **kwargs):

        pk = request.data.get('id')
        try:
            record = Salary.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found..'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalarySerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        pk = request.query_params.get('id')
        print(pk)
        try:
            Salary.objects.get(pk=pk).delete()
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'Salary Detail Deleted.'}, status=status.HTTP_200_OK)


class SalaryBonusViewSet(viewsets.ModelViewSet):
    queryset = SalaryBonus.objects.all()
    serializer_class = SalaryBonusSerializer
    permission_classes = [HRAndAdminPermA]
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    # search_fields = ('full_name', 'username', 'user_type')

    def put(self, request, *args, **kwargs):

        pk = request.data.get('id')
        try:
            record = SalaryBonus.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found..'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalaryBonusSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        pk = request.query_params.get('id')
        print(pk)
        try:
            SalaryBonus.objects.get(pk=pk).delete()
        except ObjectDoesNotExist:
            return Response({'error': 'Record Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'Salary Detail Deleted.'}, status=status.HTTP_200_OK)

# class SalaryDetailViewSet(viewsets.ModelViewSet):

# queryset = SalaryDetail.objects.filter(created_at__month=date.month(), created_at__year=date.year())
# serializer_class = SalaryDetailSerializer
# permission_classes = [IsAuthenticated, ]
# # http_method_names = ['get']
# pagination_class = ResultsSetPagination
# filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
# search_fields = ('id', 'username', 'full_name')

# def get_serializer_context(self):
#     return {'month': self.request.query_params.get('_month'), 'year': self.request.query_params.get('_year')}

# def get_queryset(self):
#     if self.request.user.user_type != 'E':
#         return self.queryset
#     else:
#         queryset = User.objects.filter(id=self.request.user.id).order_by('id')
#         return queryset
