from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Profile
from courses.models import (
    Domain, Discipline, Track, Level, Course, Chapter, Content
)
import random


class Command(BaseCommand):
    help = "Seed database with 10 academic and 10 skill-based courses (with chapters and contents)."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding Academic & Skill-Based Courses..."))

        # -----------------------
        # 1. Domains
        # -----------------------
        academic_domain, _ = Domain.objects.get_or_create(name="Academic")
        skills_domain, _ = Domain.objects.get_or_create(name="Skill-Based")

        # -----------------------
        # 2. Disciplines
        # -----------------------
        academic_disciplines = [
            Discipline.objects.get_or_create(domain=academic_domain, name="Mathematics")[0],
            Discipline.objects.get_or_create(domain=academic_domain, name="Physics")[0],
            Discipline.objects.get_or_create(domain=academic_domain, name="Chemistry")[0],
            Discipline.objects.get_or_create(domain=academic_domain, name="Biology")[0],
            Discipline.objects.get_or_create(domain=academic_domain, name="History")[0],
        ]

        skill_disciplines = [
            Discipline.objects.get_or_create(domain=skills_domain, name="Programming")[0],
            Discipline.objects.get_or_create(domain=skills_domain, name="Design")[0],
            Discipline.objects.get_or_create(domain=skills_domain, name="Marketing")[0],
            Discipline.objects.get_or_create(domain=skills_domain, name="Business")[0],
            Discipline.objects.get_or_create(domain=skills_domain, name="Music")[0],
        ]

        # -----------------------
        # 3. Tracks
        # -----------------------
        academic_tracks = [
            Track.objects.get_or_create(domain=academic_domain, name="High School Science")[0],
            Track.objects.get_or_create(domain=academic_domain, name="University Studies")[0],
        ]
        skill_tracks = [
            Track.objects.get_or_create(domain=skills_domain, name="Web Development")[0],
            Track.objects.get_or_create(domain=skills_domain, name="Creative Skills")[0],
        ]

        # -----------------------
        # 4. Levels
        # -----------------------
        beginner, _ = Level.objects.get_or_create(name="Beginner")
        intermediate, _ = Level.objects.get_or_create(name="Intermediate")
        advanced, _ = Level.objects.get_or_create(name="Advanced")

        # -----------------------
        # 5. Teacher
        # -----------------------
        teacher = Profile.objects.filter(role="teacher").first()
        if not teacher:
            self.stdout.write(self.style.ERROR("❌ No teacher profile found. Please create one."))
            return

        # -----------------------
        # 6. Courses
        # -----------------------
        academic_courses_data = [
            ("Mathematics for Beginners", "Numbers, Algebra, Geometry", academic_disciplines[0]),
            ("Advanced Physics", "Mechanics, Thermodynamics, Quantum", academic_disciplines[1]),
            ("Organic Chemistry", "Carbon compounds, reactions, synthesis", academic_disciplines[2]),
            ("General Biology", "Cells, Genetics, Evolution", academic_disciplines[3]),
            ("World History", "Civilizations, Revolutions, Modern Times", academic_disciplines[4]),
            ("Linear Algebra", "Vectors, Matrices, Transformations", academic_disciplines[0]),
            ("Electromagnetism", "Fields, Circuits, Applications", academic_disciplines[1]),
            ("Inorganic Chemistry", "Elements, Periodic Table, Compounds", academic_disciplines[2]),
            ("Human Anatomy", "Systems, Organs, Health", academic_disciplines[3]),
            ("European History", "Renaissance, Wars, Politics", academic_disciplines[4]),
        ]

        skill_courses_data = [
            ("Python Bootcamp", "Python from basics to projects", skill_disciplines[0]),
            ("JavaScript Mastery", "Frontend development with JS", skill_disciplines[0]),
            ("UI/UX Design", "User interface & user experience", skill_disciplines[1]),
            ("Graphic Design", "Photoshop, Illustrator, Branding", skill_disciplines[1]),
            ("Digital Marketing", "SEO, SEM, Social Media", skill_disciplines[2]),
            ("Entrepreneurship 101", "Startup fundamentals", skill_disciplines[3]),
            ("Business Communication", "Effective communication for leaders", skill_disciplines[3]),
            ("Guitar for Beginners", "Chords, Strumming, Songs", skill_disciplines[4]),
            ("Music Theory", "Notes, Scales, Harmony", skill_disciplines[4]),
            ("Full Stack Development", "Frontend + Backend + Deployment", skill_disciplines[0]),
        ]

        def create_course(title, about, discipline, domain, tracks):
            course, created = Course.objects.get_or_create(
                title=title,
                defaults=dict(
                    about=about,
                    description=f"This is a complete course on {title}.",
                    teacher=teacher,
                    domain=domain,
                    discipline=discipline,
                    track=random.choice(tracks),
                    level=random.choice([beginner, intermediate, advanced]),
                    price=random.choice([0, 10, 20, 30]),
                    price_unit="usd",
                    status="published",
                ),
            )
            return course

        academic_courses = [create_course(title, about, disc, academic_domain, academic_tracks)
                            for title, about, disc in academic_courses_data]
        skill_courses = [create_course(title, about, disc, skills_domain, skill_tracks)
                         for title, about, disc in skill_courses_data]

        # -----------------------
        # 7. Chapters & Contents
        # -----------------------
        def seed_chapters_and_contents(course):
            num_chapters = random.randint(8, 10)
            for order in range(1, num_chapters + 1):
                chapter, _ = Chapter.objects.get_or_create(
                    course=course,
                    title=f"Chapter {order}: {course.title} Topic {order}",
                    defaults=dict(order=order),
                )
                # add 2–3 contents per chapter
                contents = [
                    ("lesson", f"Lesson {order}.{i} for {course.title}") for i in range(1, 3)
                ] + [("quiz", f"Quiz {order} for {course.title}")]
                for idx, (ctype, title) in enumerate(contents, start=1):
                    Content.objects.get_or_create(
                        chapter=chapter,
                        title=title,
                        defaults=dict(type=ctype, order=idx),
                    )

        for course in academic_courses + skill_courses:
            seed_chapters_and_contents(course)

        self.stdout.write(self.style.SUCCESS("✅ Seeded 10 Academic & 10 Skill-Based courses with chapters & contents."))
