from rest_framework import viewsets, permissions
from .models import (
    Domain, Discipline, Track, Level, Course, CourseEnrollment,
    Chapter, Content, Review, Favourite,
 CourseProgress
)
from .serializers import (
    DomainSerializer, DisciplineSerializer, TrackSerializer, LevelSerializer, CourseSerializer,
    ChapterSerializer, CourseEnrollmentSerializer, ReviewSerializer, FavouriteSerializer,
 CourseProgressSerializer, CourseDetailSerializer, ContentDetailSerializer
)

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.AllowAny]


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [permissions.AllowAny]


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.AllowAny]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class CourseDetailBySlug(RetrieveAPIView): 
    queryset = Course.objects.all() 
    serializer_class = CourseDetailSerializer 
    lookup_field = 'slug'
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


# class ChapterViewSet(viewsets.ModelViewSet):
#     queryset = Chapter.objects.all()
#     serializer_class = ChapterSerializer
#     permission_classes = [permissions.AllowAny]

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Chapter.objects.all()
        course_id = self.request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset



class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentDetailSerializer
    permission_classes = [permissions.AllowAny]


class ContentDetailBySlug(RetrieveAPIView): 
    queryset = Content.objects.all() 
    serializer_class = ContentDetailSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        content = self.get_object()
        chapter = content.chapter
        course = chapter.course
        user = request.user

        # 1️⃣ Free chapter → always allow
        if chapter.is_free:
            return super().retrieve(request, *args, **kwargs)

        # 2️⃣ Not logged in → block
        if not user.is_authenticated:
            return Response(
                {"detail": "Please login to view this content."},
                status=403
            )

        profile = getattr(user, "profile", None)
        if not profile:
            return Response(
                {"detail": "Profile not found."},
                status=403
            )

        # 3️⃣ Check if user purchased this course
        from .models import CourseEnrollment
        is_enrolled = CourseEnrollment.objects.filter(
            student=profile,
            course=course
        ).exists()

        if not is_enrolled:
            return Response(
                {"detail": "Purchase required to access this content."},
                status=403
            )

        # 4️⃣ enrolled → allow
        return super().retrieve(request, *args, **kwargs)



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.AllowAny]

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.AllowAny]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_courses(request):
    profile = request.user.profile
    
    enrollments = CourseEnrollment.objects.filter(student=profile)
    courses = [enrollment.course for enrollment in enrollments]
    
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

class CourseProgressViewSet(viewsets.ModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer
    permission_classes = [permissions.AllowAny]
