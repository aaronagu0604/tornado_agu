#!/usr/bin/env python
# coding=utf8

from handler import AdminBaseHandler, BaseHandler
from lib.route import route
from model import *
import time


@route(r'/admin/login', name='admin_login')  # 后台登录
class LoginHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if username and password:
            try:
                user = AdminUser.get(AdminUser.username == username)
                if user.check_password(password):
                    if user.isactive == 1:
                        user.updatesignin()
                        self.session['admin'] = user
                        self.session.save()
                        self.redirect("/admin")
                        return
                    else:
                        self.flash("此账户被禁止登录，请联系管理员。")
                else:
                    self.flash("密码错误")
            except Exception, e:
                print e
                self.flash("此用户不存在")
        else:
            self.flash("请输入用户名或者密码")

        self.render("/admin/login.html", next=self.next_url)


@route(r'/admin/logout', name='admin_logout')  # 后台退出
class LogoutHandler(AdminBaseHandler):
    def get(self):
        if "admin" in self.session:
            del self.session["admin"]
            self.session.save()
        self.render('admin/login.html')


@route(r'/admin', name='admin_index')  # 后台首页
class IndexHandler(AdminBaseHandler):
    def get(self):
        report = {}
        minday = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime()), "%Y-%m-%d 0:0:0")))
        report['day_new_users'] = User.select().where((User.isactive == 1) & (User.signuped >= minday)).count()
        self.render('admin/index.html', report=report)
