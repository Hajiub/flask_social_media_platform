import os
import uuid
from werkzeug.utils import secure_filename

class SaveProfilePicture:
    def __init__(self, app, user):
        self.app = app
        self.user = user

    def save_profile_picture(self, pic):
        if pic:
            filename = self.unique_filename(pic)
            path = self.save_path(filename)
            pic.save(path)
            return self.relative_path(filename)
        return None

    def unique_filename(self, pic):
        uuid1_value = uuid.uuid1()
        return str(uuid1_value) + secure_filename(pic.filename)

    def save_path(self, filename):
        return os.path.join(
            self.app.config['UPLOAD_FOLDER'],
            self.user.email,
            'profile_pictures',
            filename
        )

    def relative_path(self, filename):
        return os.path.join('profile_pictures', filename)
