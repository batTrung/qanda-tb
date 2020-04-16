import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from core.helpers import get_random_obj
from core.models import Category
from qanda.models import Answer, Question

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=int, default=200, help='Number users')
        parser.add_argument('-c', '--category', type=int, default=10, help='Number categories')
        parser.add_argument('-q', '--question', type=int, default=10, help='Number of questions for each user')
        parser.add_argument('-a', '--answer', type=int, default=10, help='Number of answers for each question')

    def handle(self, *args, **kwargs):
        num_u = kwargs['user']
        num_c = kwargs['category']
        num_q = kwargs['question']
        num_a = kwargs['answer']

        self.stdout.write("Cleaning database...")

        User.objects.exclude(is_superuser=True).delete()
        Category.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()

        self.stdout.write(self.style.HTTP_NOT_MODIFIED(f"Creating users..."))

        users = [
            User(
                username=get_random_string(6),
                password='matkhau123') for i in range(num_u)
        ]
        User.objects.bulk_create(users)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED(f"Creating categories..."))

        categories = [
            Category(
                title=f"Category-{ i }",
                slug=f'category-slug-{ i }') for i in range(num_c)
        ]
        Category.objects.bulk_create(categories)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED(f"Creating questions..."))

        for user in User.objects.all():
            questions = [
                Question(
                    title=f"Question { user.username } { i }",
                    slug=f"question-slug-{ user.username }-{ i }",
                    user=user,
                    category=get_random_obj(Category),
                    content="""
                        Django is a high-level Python Web framework that encourages rapid development and clean,
                        pragmatic design. Built by experienced developers, it takes care of much of the hassle
                        of Web development, so you can focus on writing your app without needing to reinvent the
                        wheel. It’s free and open source.
                    """,
                    total_views=random.randint(1, 200),
                ) for i in range(num_q)
            ]
            Question.objects.bulk_create(questions)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED(f"Creating answers..."))
        for question in questions:
            answers = [
                Answer(
                    user=get_random_obj(User),
                    content='Good question!',
                    question=question,
                ) for i in range(10)
            ]
            Answer.objects.bulk_create(answers)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                    CREATE SUCCESS:
                    { num_u } users,
                    { num_c } categories,
                    { num_q*num_u } questions,
                    { num_a*num_q*num_u } answers
                """))
