from datetime import datetime, timedelta


class TimeFilter:
    def __init__(self, app):
        self.app = app
        self.app.jinja_env.filters['time_ago'] = self.time_ago

    def time_ago(self, datetime_obj):
        now = datetime.now()
        diff = now - datetime_obj
        if diff.total_seconds() < 60:
            return 'Just now'
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() // 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() // 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        else:
            days = diff.days
            if days == 1:
                return 'Yesterday'
            elif days < 7:
                return f'{days} day{"s" if days != 1 else ""} ago'
            elif days < 30:
                weeks = days // 7
                return f'{weeks} week{"s" if weeks != 1 else ""} ago'
            elif days < 365:
                months = days // 30
                return f'{months} month{"s" if months != 1 else ""} ago'
            else:
                years = days // 365
                return f'{years} year{"s" if years != 1 else ""} ago'



