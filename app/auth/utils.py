from pathlib import Path

class MakeFolder:
    def __init__(self, app, user):
        self.app = app
        self.user = user
    
    def make_folder(self):
        user_folder = Path(self.app.config['UPLOAD_FOLDER']) / self.user.email
        post_images_folder = user_folder / 'post_images'
        profile_pictures_folder = user_folder / 'profile_pictures'

        self._create_folder(user_folder)
        self._create_folder(post_images_folder)
        self._create_folder(profile_pictures_folder)
    
    def _create_folder(self, path):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create folder: {path}") from e
