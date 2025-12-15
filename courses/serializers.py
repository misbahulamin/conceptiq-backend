from rest_framework import serializers
from .models import (
    Domain, Discipline, Track, Level, Course,
    Chapter, Content, Review, Favourite,
    CourseEnrollment, CourseProgress
)
from users.serializers import ProfileSerializer
from users.models import Profile


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"





# Nested serializers
class ContentSerializer(serializers.ModelSerializer):
    chapter_id = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(),
        source="chapter",
        write_only=True
    )

    chapter = serializers.SerializerMethodField()
    class Meta:
        model = Content
        fields = ["id", "chapter_id", "chapter", "title", "slug", "type", "order"]

    def get_chapter(self, obj):
        return obj.chapter.id if obj.chapter else None
    
# create a Content detail serializer with all fields
class ContentDetailSerializer(serializers.ModelSerializer):
    chapter_id = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(),
        source="chapter",
        write_only=True
    )
    chapter = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    class Meta:
        model = Content
        fields = "__all__"

    def get_chapter(self, obj):
        return obj.chapter.id if obj.chapter else None
    def get_course(self, obj):
        return obj.chapter.course.id if obj.chapter and obj.chapter.course else None

# class ChapterSerializer(serializers.ModelSerializer):
#     contents = ContentSerializer(many=True, read_only=True)
#     subchapters = serializers.SerializerMethodField()

#     class Meta:
#         model = Chapter
#         fields = ["id", "title", "description", "order", "subchapters", "contents"]

#     def get_subchapters(self, obj):
#         children = obj.get_children()
#         return ChapterSerializer(children, many=True).data

class ChapterSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    # Writable relationships
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="course",
        write_only=True
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(),
        source="parent",
        write_only=True,
        required=False,
        allow_null=True
    )

    # Read-only IDs for GET responses
    course = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = [
            "id",
            "course_id",    # writable
            "course",       # readable
            "parent_id",    # writable
            "parent",       # readable
            "title",
            "description",
            "order",
            "contents",
            "is_free"
        ]

    def get_course(self, obj):
        return obj.course.id if obj.course else None

    def get_parent(self, obj):
        return obj.parent.id if obj.parent else None




class CourseSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    discipline = DisciplineSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    teacher = ProfileSerializer(read_only=True)

    
    # Writable foreign key IDs
    domain_id = serializers.PrimaryKeyRelatedField(
        queryset=Domain.objects.all(), source='domain', write_only=True, required=False
    )
    discipline_id = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(), source='discipline', write_only=True, required=False
    )
    track_id = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(), source='track', write_only=True, required=False
    )
    level_id = serializers.PrimaryKeyRelatedField(
        queryset=Level.objects.all(), source='level', write_only=True, required=False
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(role='teacher'), source='teacher', write_only=True, required=False
    )

    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    discipline = DisciplineSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "about", "description", "teacher", 
            "price", "price_unit", "language", "status", "published_at", 
            "thumbnail", "thumbnail_url", "domain", "discipline", "track", "level", "chapters", "is_enrolled",
        ]

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        print(user)

        if not user or not user.is_authenticated:
            return False
        
        profile = getattr(user, "profile", None)
        if not profile:
            return False
        
        

        return CourseEnrollment.objects.filter(
            student=profile,
            course=obj
        ).exists()




class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class FavouriteSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)

    class Meta:
        model = Favourite
        fields = "__all__"


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = "__all__"



class CourseProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = CourseProgress
        fields = "__all__"
