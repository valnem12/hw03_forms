from django.test import TestCase

from posts.models import Post, Group, User


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

    def correct_object_name(self, text):
        self.assertIsInstance(text, str)

    def forms_check(self, dict, field_text):
        for value, expected in dict.items():
            with self.subTest(value=value):
                obj_attr = getattr(self.post._meta.get_field(value),
                                   field_text)
                self.assertEqual(obj_attr, expected)

    def test_post_name_is_string(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.correct_object_name(self.post.text[:15])

    def test_group_name_is_string(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.correct_object_name(self.group.title)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'author': 'Автор',
            'group': 'Группа',
        }
        self.forms_check(field_verboses, 'verbose_name')

    def test_help_text(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        self.forms_check(field_help_text, 'help_text')
