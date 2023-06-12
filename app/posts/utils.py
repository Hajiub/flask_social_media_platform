
from flask import flash
import os, uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class CreatePost:
    pass


class PostUpdater:
    def __init__(self, current_app, current_user):
        self.current_app = current_app
        self.current_user = current_user

    def update_post_fields(self, post, form):
        self.update_post_image(post, form.data.get('image'))
        self.update_post_content(post, form.data.get('content'))

    def update_post_image(self, post, new_img):
        if post.post_img:
            self.remove_image(post.post_img)

        if new_img:
            try:
                img_name = self.generate_unique_image_name(new_img)
                self.save_image(new_img, img_name)
                post.post_img = os.path.join('post_images', img_name)
            except Exception as e:
                flash('An error occurred while updating the post image.', 'error')
                raise e
        else:
            post.post_img = None

    def update_post_content(self, post, content):
        post.content = content

    def remove_image(self, image_path):
        path = os.path.join(self.current_app.config['UPLOAD_FOLDER'], self.current_user.email, image_path)
        try:
            os.remove(path)
        except Exception as e:
            flash('An error occurred while removing the post image.', 'error')
            raise e

    def save_image(self, image, img_name):
        save_path = os.path.join(self.current_app.config['UPLOAD_FOLDER'], self.current_user.email, "post_images", img_name)
        try:
            image.save(save_path)
        except Exception as e:
            flash('An error occurred while saving the post image.', 'error')
            raise e

    def generate_unique_image_name(self, image):
        uuid1_value = uuid.uuid1()
        return str(uuid1_value) + secure_filename(image.filename)
