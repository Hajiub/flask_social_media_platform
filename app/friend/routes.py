from . import friend
from flask_login import current_user


@friend.route('/add_friend/<int:friend_id>')
def add_friend(friend_id):
    return f"{current_user.id} --> {friend_id}"