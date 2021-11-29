# posts/tests/test_urls.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.models import Post, Group

from http import HTTPStatus

User = get_user_model()


class YatubeURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        cls.user = User.objects.create_user(username='shuki')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст для теста',
        )
        cls.group = Group.objects.create(
            title='supergroup',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )
        cls.templates_url_guest_users = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{cls.group.slug}/',
            'posts/post_detail.html': f'/posts/{cls.post.pk}/',
            'posts/profile.html': f'/profile/{cls.post.author}/',
            'users/login.html': '/auth/login/',
            'users/logged_out.html': '/auth/logout/',
            'users/signup.html': '/auth/signup/'
        }
        cls.templates_url_authorized_users = {
            'posts/post_create.html': ('/create/'
                                       or f'/posts/{cls.post.pk}/edit/'),
            'users/password_change_done.html': '/auth/password_change/done/',
            'users/password_change.html': '/auth/password_change/',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def urls_check(self, client, dict):
        for address in dict.values():
            with self.subTest(address=address):
                response = client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def templates_check(self, client, dict):
        for template, address in dict.items():
            with self.subTest(address=address):
                response = client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting(self):
        response = self.guest_client.get('/prosto_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_guests_users_urls(self):
        self.urls_check(self.guest_client, self.templates_url_guest_users)

    def test_authorized_users_urls(self):
        self.urls_check(self.authorized_client,
                        self.templates_url_authorized_users)

    def test_templates(self):
        clients = (self.guest_client, self.authorized_client)
        templates = (self.templates_url_guest_users,
                     self.templates_url_authorized_users)
        for clnt, dict in zip(clients, templates):
            self.templates_check(clnt, dict)
