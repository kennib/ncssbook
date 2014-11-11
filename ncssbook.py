#!/usr/bin/env python3
from tornado.ncss import Server, ncssbook_log

from db import DoesNotExistError, IntegrityError, Post, User


LOGIN_HTML = open('static/html_plates/login.html', 'rU').read()
logger = ncssbook_log


def index(response):
    form_id = response.get_field('form_id', 'front')
    if form_id == 'front':
        response.write(LOGIN_HTML)
    elif form_id == 'login':
        user = response.get_field('user')
        try:
            user = User.get(user=user)
            set_user(response, user)
            response.redirect('/profile')
        except DoesNotExistError:
            response.redirect('/')
    elif form_id == 'signup':
        user = response.get_field('user')
        passwd1 = response.get_field('passwd1')
        #passwd2 = response.get_field('passwd2')
        first = response.get_field('first')
        last = response.get_field('last')
        dob = response.get_field('dob')
        logger.info('adding user {} ({} {}) with passwd {}'.format(user, first, last, passwd1))
        if user and first and last and passwd1:
            try:
                user = User.add(user=user, passwd=passwd1, first=first, last=last, dob=dob)
                set_user(response, user)
                response.redirect('/profile')
            except IntegrityError:
                response.write(LOGIN_HTML)
        else:
            response.write(LOGIN_HTML)


def get_user(response):
    user_id = response.get_secure_cookie('user_id')
    user = None
    if user_id is None:
        response.redirect('/')
    else:
        try:
            user = User.get(id=int(user_id))
        except DoesNotExistError:
            response.redirect('/')
    return user


def set_user(response, user):
    response.set_secure_cookie('user_id', str(user.id))


def logout(response):
    response.clear_cookie('user_id')
    response.redirect('/')


def profile(response, profile_id=None):
    user = get_user(response)
    if user is None:
        return

    if profile_id is None:
        profile = user
    else:
        profile = User.get(id=profile_id)

    content = open('static/html_plates/profile.html', 'rU').read()
    content = content.replace('<% first_name %>', profile.first)
    content = content.replace('<% last_name %>', profile.last)
    content = content.replace('<% profile_id %>', str(profile.id))
    response.write(content)


def render_wall(response, wall_id):
    for post in Post.iter(wall=wall_id):
        author = User.get(id=post.user)
        response.write("<hr><h4>%s</h4><p>%s</p>" % (author.fullname(), post.msg))


def wall(response):
    user = get_user(response)
    if user is None:
        return

    profile_id = response.get_field('profile_id')
    render_wall(response, profile_id)


def post(response):
    user = get_user(response)
    if user is None:
        return

    profile_id = response.get_field('profile_id')
    wall = User.get(id=profile_id)
    msg = response.get_field('msg')
    user.add_post(wall, msg)
    render_wall(response, wall.id)


def search(response):
    pass


server = Server()
server.register('/', index)
server.register('/logout', logout)
server.register('/profile', profile)
server.register('/profile/([0-9]+)$', profile)
server.register('/wall', wall)
server.register('/post', post)
server.register('/search', search)
server.run()
