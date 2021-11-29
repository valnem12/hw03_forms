from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст для теста',
        )
        cls.group = Group.objects.create(
            title='supergroup',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )

    def object(self):
        return PostModelTest.post

    def correct_object_name(self, text):
        self.assertEqual(str(text), text)

    def forms_check(self, dict, flag='help_text'):
        for value, expected in dict.items():
            with self.subTest(value=value):
                if flag == 'name':
                    self.assertEqual(
                        self.object()
                        ._meta.get_field(value).verbose_name, expected)
                else:
                    self.assertEqual(
                        self.object()
                        ._meta.get_field(value).help_text, expected)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        text = self.object().text
        self.correct_object_name(text[:15])
        self.assertEqual(str(text[:15]), text[:15])

        task_group = PostModelTest.group
        title = task_group.title
        self.correct_object_name(title)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'author': 'Автор',
            'group': 'Группа',
        }
        self.forms_check(field_verboses, 'name')

    def test_help_text(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        self.forms_check(field_help_text, )
