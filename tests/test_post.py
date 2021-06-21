import unittest
from app.models import Post, User


class PostModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Ammoh = User(username='Ammoh', password='kip', email='kiprotichamos76@gmail.com')
        self.new_blog = Post(id=1, title='Test', content='This is a test blog', user_id=self.user_natasha.id)

    def tearDown(self):
        Post.query.delete()
        User.query.delete()