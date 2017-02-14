#!/usr/bin/env python
# coding=utf8

import logging
import simplejson
from tornado.web import RequestHandler
from lib.route import route
from model import *
import uuid
from handler import MobileHandler


@route(r'/', name='mobile_app')
class MobileAppHandler(MobileHandler):
    def get(self):
        self.write("czj api")


@route(r'/getvcode', name='mobile_getvcode')
class MobileGetVCodeAppHandler(RequestHandler):
    """
    @apiGroup auth
    @apiVersion 1.0.0
    @api {get} /mobile/getvcode 01. 获取验证码
    @apiDescription 获取验证码

    @apiParam {String} mobile 电话号码
    @apiParam {Int} flag 验证码类型： 0注册 1忘记密码 2绑定手机号 3提现

    @apiSampleRequest /mobile/getvcode
    """
    def get(self):
        result = {'flag': 0, 'msg': '', "data": {}}
        mobile = self.get_argument('mobile', None)
        flag = self.get_argument('flag', None)
        if mobile and flag:
            pass
        else:
            result['flag'] = 1
            result['msg'] = '请传入正确的手机号码'
        self.write(simplejson.dumps(result))


@route(r'/checkregvcode', name='mobile_checkregvcode')
class MobileCheckRegVCodeAppHandler(RequestHandler):
    """
    @apiGroup auth
    @apiVersion 1.0.0
    @api {post} /mobile/checkregvcode 02. 检查申请入驻验证码
    @apiDescription 检查申请入驻验证码

    @apiParam {String} mobile 电话号码
    @apiParam {String} vcode 验证码

    @apiSampleRequest /mobile/checkregvcode
    """

    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = {'flag': 0, 'msg': '', "data": {}}
        mobile = self.get_body_argument('mobile', None)
        vcode = self.get_body_argument('vcode', None)
        if mobile and vcode:
            VCode.select()
            pass
        else:
            result['flag'] = 1
            result['msg'] = '请传入正确的手机号码与验证码'
        self.write(simplejson.dumps(result))


@route(r'/mobile/reg', name='mobile_reg')  # 手机端注册
class MobileRegHandler(RequestHandler):
    """
    @apiGroup auth
    @apiVersion 1.0.0
    @api {post} /mobile/reg 03. 商家申请入驻平台
    @apiDescription 商家申请入驻平台

    @apiParam {String} mobile 电话号码
    @apiParam {String} password 密码

    @apiSampleRequest /mobile/reg
    """

    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = {'flag': 0, 'msg': '', "data": {}}
        mobile = self.get_body_argument("mobile", None)

        self.write(simplejson.dumps(result))


@route(r'/mobile/login', name='mobile_login')  # 手机端登录
class MobileLoginHandler(RequestHandler):
    """
    @apiGroup auth
    @apiVersion 1.0.0
    @api {post} /mobile/login 04. 登录
    @apiDescription 通过手机号密码登录系统

    @apiParam {String} mobile 电话号码
    @apiParam {String} password 密码

    @apiSampleRequest /mobile/login
    """
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        logging.info('get in')
        result = {'flag': 0, 'msg': '', "data": {}}
        mobile = self.get_body_argument("mobile", None)
        password = self.get_body_argument("password", None)
        if mobile and password:
            logging.info('get in :' + mobile + '; pw=' + password)
            try:
                user = User.get(User.mobile == mobile)
                logging.info('get in 22')
                if user.check_password(password):
                    logging.info('get in 233')
                    if user.active > 0:
                        logging.info('get in 244')
                        token = 'mt:' + str(uuid.uuid4())
                        logging.info('token=' + token)
                        result['flag'] = 1
                        result['data']['type'] = user.store.store_type
                        result['data']['token'] = token
                        result['data']['uid'] = user.id
                        self.application.memcachedb.set(token, str(user.id), 7200)
                        user.updatesignin()
                    else:
                        logging.info('get in 200')
                        result['msg'] = "此账户被禁止登录，请联系管理员。"
                else:
                    logging.info('get in 299')
                    result['msg'] = "用户名或密码错误"
            except Exception, e:
                logging.info('get in 299009')
                result['msg'] = "此用户不存在"
        else:
            logging.info('get in 3')
            result['msg'] = "请输入用户名或者密码"
        self.write(simplejson.dumps(result))
        self.finish()

















