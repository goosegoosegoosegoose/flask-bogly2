from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class BoglyTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        user = User(first_name='Monkey', last_name='Mark', image_url='https://cdn.iconscout.com/icon/premium/png-256-thumb/hello-1-336715.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        Post.query.delete()
        post = Post(title="Which Banana", content="This banana", user_id=int(user.id))
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.session.rollback()

    def test_users_form(self):
        with app.test_client() as client:
            res = client.post('/users/new', data={'first_name': 'Michael', 'last_name': 'Matthews', 'image_url': 'https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-256x256.jpg'})
            
            self.assertEqual(res.status_code, 302)

    def test_users_redirect(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)


    def test_edit_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/edit', data={'first_name': 'bongo', 'last_name': 'bungo', 'image_url': 'https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-256x256.jpg'})

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, f'http://localhost/users/{self.user_id}')

    def test_user_delete(self):
        with app.test_client() as client:
            res = client.post(f'users/{self.user_id}/delete')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)


    def test_delete_redirect(self):
        with app.test_client() as client:
            res = client.post(f'users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)