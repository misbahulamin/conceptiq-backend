from django.contrib import admin
from .models import (
    Domain,
    Discipline,
    Track,
    Level,
    Course,
    Chapter,
    Content,
    Review,
    Favourite,
    CourseProgress
)

# -----------------------
# Domain, Discipline, Track
# -----------------------
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
    list_filter = ('domain',)
    search_fields = ('name',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
    list_filter = ('domain',)
    search_fields = ('name',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -----------------------
# Courses
# -----------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'discipline', 'track', 'teacher', 'status', 'price', 'price_unit')
    list_filter = ('domain', 'discipline', 'track', 'status', 'language')
    search_fields = ('title', 'teacher__user__username')
    ordering = ('title',)


# -----------------------
# Chapters & Contents
# -----------------------
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'parent', 'order')
    list_filter = ('course',)
    search_fields = ('title',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'type', 'order')
    list_filter = ('chapter', 'type')
    search_fields = ('title',)


# -----------------------
# User Behavior
# -----------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    list_filter = ('course', 'rating', 'created_at')
    search_fields = ('student__user__username', 'course__title')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('student__user__username', 'course__title')




@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'chapter', 'content', 'completed', 'last_accessed')
    list_filter = ('course', 'completed')
    search_fields = ('student__user__username', 'course__title')
