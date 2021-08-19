from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Announcement

UserModel = get_user_model()


class PostListTest(TestCase):
    def test_post_list_page_return_success(self):
        response = self.client.get(reverse('blog-home'))
        posts = response.context['posts']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class PostDetailsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='bori',
            password='parola123',
        )
        self.post = Post.objects.create(
            title='Valid title',
            content='Valid content.',
            author_id=self.user.id,
        )

    def test_blog_post_details_with_user_logged_in_return_success(self):
        self.client.force_login(self.user)

        self.assertEqual(Post.objects.count(), 1)
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_blog_post_details_without_user_logged_in_return_success(self):
        self.assertEqual(Post.objects.count(), 1)
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')


class CreateBlogPostTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='bori',
            password='parola123',
        )

    def test_create_blog_post_when_there_is_user_return_success(self):
        data = {'title': 'Uppercase letter',
                'content': 'Content.',
                }
        self.client.force_login(self.user)

        response = self.client.post('/post/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_blog_post_when_there_is_no_user_return_failure(self):
        data = {
            'title': 'Uppercase letter',
            'content': 'Content.',
        }
        response = self.client.post('/post/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)


class DeleteBlogPostView(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='bori',
            password='parola123',
        )
        self.post = Post.objects.create(
            title='Valid title',
            content='Valid content.',
            author_id=self.user.id,
        )
        self.delete_url = reverse('post-delete', args=[self.post.id])

    def test_delete_blog_post_view_with_user_logged_in_return_success(self):
        self.client.force_login(self.user)
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_blog_post_view_no_user_logged_in_return_failure(self):
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)


class AnnouncementPostListTest(TestCase):
    def test_post_list_page_return_success(self):
        response = self.client.get(reverse('announcement-home'))
        announcement_posts = response.context['announcements']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/announcements.html')


class AnnouncementDetailsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='bori',
            password='parola123',
        )
        self.announcement = Announcement.objects.create(
            title='Valid title',
            content='Valid content.',
            author_id=self.user.id,
        )

    def test_blog_announcement_details_with_user_logged_in_return_success(self):
        self.client.force_login(self.user)

        self.assertEqual(Announcement.objects.count(), 1)
        response = self.client.get(reverse('announcement-details', args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/announcement_detail.html')

    def test_blog_announcement_details_without_user_logged_in_return_success(self):
        self.assertEqual(Announcement.objects.count(), 1)
        response = self.client.get(reverse('announcement-details', args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/announcement_detail.html')
