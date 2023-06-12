#!/bin/bash

# Create the directory structure
mkdir -p app/static/css
mkdir -p app/static/images
mkdir -p app/templates
mkdir -p app/auth
mkdir -p app/profiles
mkdir -p app/posts
mkdir -p app/notifications
mkdir -p app/messages

# Create the files
touch app/static/css/styles.css
touch app/static/images/logo.png
touch app/templates/base.html
touch app/templates/home.html
touch app/templates/profile.html
touch app/templates/newsfeed.html
touch app/templates/create_post.html
touch app/templates/notifications.html
touch app/templates/messages.html
touch app/__init__.py
touch app/models.py
touch app/forms.py
touch app/auth/__init__.py
touch app/auth/routes.py
touch app/auth/utils.py
touch app/profiles/__init__.py
touch app/profiles/routes.py
touch app/profiles/utils.py
touch app/posts/__init__.py
touch app/posts/routes.py
touch app/posts/utils.py
touch app/notifications/__init__.py
touch app/notifications/routes.py
touch app/notifications/utils.py
touch app/messages/__init__.py
touch app/messages/routes.py
touch app/messages/utils.py
touch run.py
touch README.md
