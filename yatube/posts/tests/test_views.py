from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

from datetime import date

User = get_user_model()


class YatubeViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        cls.user = User.objects.create_user(username='shuki')
        cls.group = Group.objects.create(
            title='supergroup',
            slug='supergroup_8u8907272363',
            description='Тестовый group для теста',
        )
        cls.post = []
        for i in range(11):
            cls.post.append(Post.objects.create(
                author=cls.user,
                text='Тестовый текст для теста',
                pub_date=date.today(),
                group=cls.group)
            )

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
                kwargs={'post_id': self.post[1].pk}
            ),
            'posts/profile.html': reverse(
                'posts:profile',
                kwargs={'username': self.post[1].author}
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

    def context_retrieved(self, response, col='post', page=None):
        self.assertEqual(response.context[col].group.title, 'supergroup')
        self.assertEqual(response.context[col].text,
                         'Тестовый текст для теста')
        self.assertEqual(response.context[col].pub_date,
                         self.post[1].pub_date)
        if page:
            self.assertEqual(response.context['page_obj']
                             .paginator.num_pages, 2)
            self.assertEqual(len(response.context['page_obj']
                                 .paginator.page(1).object_list), 10)

    def test_index_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.context['post'].author.username, 'shuki')
        self.context_retrieved(response, page=1)

    def test_group_posts_shows_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}))
        self.context_retrieved(response, page=1)

    def test_profile_shows_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (
            self.authorized_client
            .get(reverse('posts:profile',
                         kwargs={'username': self.post[1].author})
                 )
        )
        self.context_retrieved(response, page=1)

    def test_post_detail(self):
        response = (self.authorized_client
                    .get(reverse('posts:post_detail',
                                 kwargs={'post_id': 2}
                                 ))
                    )
        self.context_retrieved(response, col='post_by_text_id')
        self.assertEqual(response.context['post_by_text_id']
                         .author.username, 'shuki')
        self.assertEqual(response.context['post_count'], 11)

    def forms_check(self, response):
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.forms_check(response)

    def test_post_edit(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': 2}))
        self.forms_check(response)
