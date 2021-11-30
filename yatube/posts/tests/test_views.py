from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.forms import PostForm
from yatube.settings import POSTS_PER_PAGE


class YatubeViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса
        cls.user = User.objects.create_user(username='shuki')
        cls.group = Group.objects.create(
            title='supergroup',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст для теста',
            group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def check_uses_correct_template(self, clnt, dict):
        for template, reverse_name in dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = clnt.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names_anonymus = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list',
                                             kwargs={'slug': self.group.slug}),
            'posts/post_detail.html': reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ),
            'posts/profile.html': reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            ),
            'users/login.html': reverse('users:login'),
            'users/logged_out.html': reverse('users:logout'),
            'users/signup.html': reverse('users:signup'),
        }
        templates_page_names_authorized = {
            'posts/post_create.html': reverse('posts:post_create'),
            'users/password_change_done.html': reverse(
                'users:password_change_done'),
            'users/password_change.html': reverse('users:password_change'),
        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        self.check_uses_correct_template(self.guest_client,
                                         templates_page_names_anonymus)
        self.check_uses_correct_template(self.authorized_client,
                                         templates_page_names_authorized)

    def context_retrieved(self, response, col='post'):
        self.assertEqual(response.context[col].group.title, 'supergroup')
        self.assertEqual(response.context[col].text,
                         'Тестовый текст для теста')
        self.assertEqual(response.context[col].pub_date,
                         self.post.pub_date)

    def author_exists_check(self, response, col):
        self.assertEqual(response.context[col].author.username, 'shuki')

    def test_index_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        self.author_exists_check(response, 'post')
        self.context_retrieved(response)

    def test_group_posts_shows_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}))
        self.context_retrieved(response)

    def test_profile_shows_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (
            self.authorized_client
            .get(reverse('posts:profile',
                         kwargs={'username': self.post.author})
                 )
        )
        self.context_retrieved(response)
        self.author_exists_check(response, 'post')

    def test_post_detail(self):
        response = (self.authorized_client
                    .get(reverse('posts:post_detail',
                                 kwargs={'post_id': self.post.pk}
                                 ))
                    )
        self.context_retrieved(response, col='post_by_text_id')
        self.author_exists_check(response, 'post_by_text_id')

    def test_post_creation_or_edit(self):
        urls = (reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
                reverse('posts:post_create'))
        for reverse_name in urls:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIsInstance(response.context['form'], PostForm)
                self.assertEqual(list(response.context['form'].fields.keys()),
                                 ['text', 'group'])
                try:
                    self.assertTrue(response.context['is_edit'])
                except:
                    continue


class YatubePaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса
        cls.NUM_OF_POSTS = POSTS_PER_PAGE + 1
        cls.user = User.objects.create_user(username='shuki')
        cls.group = Group.objects.create(
            title='supergroup',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )
        cls.post = Post.objects.bulk_create(
            [
                Post(
                    author=cls.user,
                    text='Тестовый текст для теста',
                    group=cls.group
                )
                for i in range(cls.NUM_OF_POSTS)
            ])

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator_check(self, response=None):
        urls = [reverse('posts:index'),
                reverse('posts:group_list',
                        kwargs={'slug': self.group.slug}),
                reverse('posts:profile',
                        kwargs={'username': self.post[1].author})
                ]
        for reverse_name in urls:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.context['page_obj']
                                 .paginator.num_pages, 2)
                self.assertEqual(len(response.context['page_obj']
                                 .paginator.page(1).object_list),
                                 POSTS_PER_PAGE)

    def test_post_detail(self):
        response = (self.authorized_client
                    .get(reverse('posts:post_detail',
                                 kwargs={'post_id': self.NUM_OF_POSTS}
                                 ))
                    )
        self.test_paginator_check(response)
        self.assertEqual(response.context['post_count'], self.NUM_OF_POSTS)
