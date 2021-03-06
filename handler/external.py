#!/usr/bin/env python
# coding=utf8

from handler import BaseHandler
from lib.route import route
from model import *
import time


@route(r'/user/showInsurance/(\d+)')  # 保单展示
class showInsurance(BaseHandler):
    def get(self, oid):
        addr = self.get_argument('addr', "0")
        if not int(oid):
            return self.render('404.html')

        if addr == '1':
            if (int(oid)-97)%91:
                print 'False',(int(oid)-97)%91
                return self.render('404.html')
            oid = (int(oid)-97)/91
        else:
            if (int(oid)-997)%73:
                print 'True',(int(oid)-997)%73
                return self.render('404.html')
            oid = (int(oid)-997)/73

        o = InsuranceOrder.get(id=oid)

        insuranceitem = InsuranceItem.select().order_by(InsuranceItem.sort)
        dictI = []
        for i in insuranceitem:
            iValue = getattr(o.current_order_price, i.eName)
            if i.style == u'交强险':
                if iValue:
                    dictI.append(u"交强险: 交强险")
            elif i.style == u'商业险-主险' and iValue != 'false' and iValue:
                dictI.append(u'商业险-主险：' + i.name + u'(%s)'%iValue)
            elif i.style == u'商业险-附加险' and iValue != 'false' and iValue:
                dictI.append(u'商业险-附加险：' + i.name + u'(%s)' % iValue)

        self.render('admin/user/showInsurance.html', o=o, dictI=dictI, addr=addr)

@route(r'/user/showarticle/(\d+)')  # 活动详情展示
class showArticle(BaseHandler):
    def get(self, a_id):
        a_id = int(a_id) if a_id else 0
        try:
            article = JPushActive.get(id=a_id)
            self.render('admin/user/showArticle.html', article=article)
        except Exception:
            self.write('活动不存在，或者已下线')




















