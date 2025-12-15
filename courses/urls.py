from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DomainViewSet, DisciplineViewSet, TrackViewSet, LevelViewSet, CourseViewSet,
    ChapterViewSet, ContentViewSet, ReviewViewSet, FavouriteViewSet, CourseEnrollmentViewSet,
  CourseProgressViewSet, CourseDetailBySlug, ContentDetailBySlug, my_courses
)

router = DefaultRouter()
router.register(r'domains', DomainViewSet)
router.register(r'disciplines', DisciplineViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'contents', ContentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'favourites', FavouriteViewSet)
router.register(r'course-enrollment', CourseEnrollmentViewSet)
router.register(r'progress', CourseProgressViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path("courses/user/my-courses/", my_courses),
    path('courses/slug/<path:slug>/', CourseDetailBySlug.as_view(), name='course-detail-by-slug'),
    path('contents/slug/<path:slug>/', ContentDetailBySlug.as_view(), name='content-detail-by-slug'),

   
]
