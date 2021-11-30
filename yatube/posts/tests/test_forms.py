import shutil
import tempfile

from posts.forms import PostForm
from posts.models import Post, Group, User
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='shuki')
        cls.group = Group.objects.create(
            title='test',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст для теста',
            group=cls.group)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в PostForm."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        # Подготавливаем данные для передачи в форму
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        self.assertTrue(PostForm(form_data).is_valid())
        response = self.authorized_client.post(
            '/create/',
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile',
            # here is cls.post in use
            kwargs={'username': self.post.author}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с нашим group
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма создает запись в PostForm."""
        update_url = reverse('posts:post_edit',
                             kwargs={'post_id': self.post.pk})
        form_data = {
            'text': 'Тестовый текст для теста 25',
            'group': self.group.id
        }
        response = self.authorized_client.post(update_url, form_data)
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=self.group.id
            ).exists()
        )
