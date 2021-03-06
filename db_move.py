#!/usr/bin/env python
# coding=utf8


'''
# 数据库迁移代码
# 思路：
# 1、首先迁移顶层没有外键依赖的数据。
# 2、其次迁移重要的有依赖的数据。
# 3、最后迁移日志类型的记录数据。
'''

# old database
import simplejson
from db_model import Delivery as Old_Delivery
from db_model import Area as Old_Area
from db_model import AdType as Old_AdType
from db_model import Ad as Old_Ad
from db_model import AdminUser as Old_AdminUser
from db_model import AdminLog as Old_AdminLog
from db_model import User as Old_User
from db_model import UserAddr as Old_UserAddr
from db_model import Score as Old_Score
from db_model import Withdraw as Old_Withdraw
from db_model import Feedback as Old_Feedback # 意见反馈
from db_model import PinPaiType as Old_PinPaiType
from db_model import PPTAttribute as Old_PPTAttribute
from db_model import PPTAQuantity as Old_PPTAQuantity
from db_model import PinPai as Old_PinPai
from db_model import Store as Old_Store
from db_model import StoreServerArea as Old_StoreServerArea
from db_model import Product as Old_Product
from db_model import ProductPic as Old_ProductPic
from db_model import ProductAttribute as Old_ProductAttribute
from db_model import ProductStandard as Old_ProductStandard # 商品发布
from db_model import CurrencyExchangeList as Old_CurrencyExchangeList # 积分兑换规则表
from db_model import Cart as Old_Cart
from db_model import Settlement as Old_Settlement
from db_model import BankCard as Old_BankCard
from db_model import Order as Old_Order # 订单
from db_model import Insurances as Old_Insurances  # 保险
from db_model import InsurancePrice as Old_InsurancePrice
from db_model import InsuranceOrder as Old_InsuranceOrder
from db_model import InsuranceOrderReceiving as Old_InsuranceOrderReceiving
from db_model import OrderItem as Old_OrderItem
from db_model import Hot_Search as Old_HotSearch
# newdatabase
from model_move import Delivery as New_Delivery
from model_move import Area as New_Area
from model_move import User as New_User
from model_move import AdminUser as New_AdminUser
from model_move import AdminUserLog as New_AdminUserLog
from model_move import Store as New_Store
from model_move import StoreAddress as New_StoreAddress
from model_move import StoreBankAccount as New_StoreBankAccount
from model_move import StoreArea as New_StoreArea
from model_move import MoneyRecord as New_MoneyRecord
from model_move import ScoreRecord as New_ScoreRecord
from model_move import Category as New_Category
from model_move import CategoryAttribute as New_CategoryAttribute
from model_move import CategoryAttributeItems as New_CategoryAttributeItems
from model_move import Brand as New_Brand
from model_move import BrandCategory as New_BrandCategory
from model_move import Product as New_Product
from model_move import ProductPic as New_ProductPic
from model_move import ProductAttributeValue as New_ProductAttributeValue
from model_move import ProductRelease as New_ProductRelease
from model_move import StoreProductPrice as New_StoreProductPrice
from model_move import ShopCart as New_ShopCart
from model_move import Settlement as New_Settlement
from model_move import Order as New_Order
from model_move import SubOrder as New_SubOrder
from model_move import OrderItem as New_OrderItem
from model_move import Insurance as New_Insurance
from model_move import InsuranceArea as New_InsuranceArea
from model_move import InsuranceItem as New_InsuranceItem
from model_move import InsurancePrice as New_InsurancePrice
from model_move import InsuranceOrderPrice as New_InsuranceOrderPrice
from model_move import InsuranceOrder as New_InsuranceOrder
from model_move import Block as New_Block
from model_move import BlockItem as New_BlockItem
from model_move import BlockItemArea as New_BlockItemArea
from model_move import Feedback as New_Feedback
from model_move import BankCard as New_BankCard
from model_move import HotSearch as New_HotSearch

imgurl = 'http://img.520czj.com'
'''
# 第一部分：无依赖的基础数据
'''
def move_hotsearch():
    old_hot = Old_HotSearch.select()
    old_data = [{
        'keywords':item.keywords,
        'quantity':item.quantity,
        'status':item.status,
        'last_time':item.last_time
    } for item in old_hot]

    New_HotSearch.insert_many(old_data).execute()
    print 'move hotsearch:', len(old_data)

# delivery:物流公司
delivery_map = {}

def move_delivery():
    old_delivery = Old_Delivery.select()
    dimg = {
        1:'http://img.520czj.com/image/2017/05/27/server1_20170527164411pSZiMHxQDnaCAwYTXtfBOboN.png',
        2:'http://img.520czj.com/image/2017/05/27/server1_20170527164450kbEPeCUcpsHNZLwyolOxSfYA.png',
        3:'http://img.520czj.com/image/2017/05/27/server1_20170527164507wPjrQpaAcVDCIhKHsyEfMqxm.png',
        4:'http://img.520czj.com/image/2017/05/27/server1_20170527164545LdQkeXxGjqnBTuvPUAWacpMO.png',
        5:'http://img.520czj.com/image/2017/05/27/server1_20170527164525ZwIbqopDuhviCJzYfPVGANtB.png',
        6:'http://img.520czj.com/image/2017/05/27/server1_20170527164617nvFldkMYcXIoSbVjfUgAZLyp.png',
        7:'http://img.520czj.com/image/2017/05/27/server1_20170527164630IALYMnQsvrPRwfjzUxqHEdbg.png',
        8:'http://img.520czj.com/image/2017/05/27/server1_20170527164644smAIaHCTXdVwLhGMvoifBEQK.png',
    }
    for item in old_delivery:
        delivery = New_Delivery.create(
            name=item.name,
            img=dimg[item.id]
        )

        delivery_map[item.id] = delivery.id
    print 'move delivery:', old_delivery.count()

# bank:银行卡类型
def move_bankcard():
    old_bankcard = Old_BankCard.select()
    old_data = [{
        'card_bin': item.card_bin,
        'bank_name': item.bank_name,
        'bank_id': item.bank_id,
        'card_name': item.card_name,
        'card_type': item.card_type,
        'bin_digits': item.bin_digits,
        'card_digits': item.card_digits,
        'demo': item.demo
    } for item in old_bankcard]

    New_BankCard.insert_many(old_data).execute()
    print 'move bankcard:', len(old_data)

# area: 区域
area_map = {}

def move_area():
    old_area = Old_Area.select()
    for item in old_area:
        area = New_Area.create(
            pid=item.pid if item.pid else None,
            code=item.code,
            has_sub=item.has_sub,
            name=item.name,
            spell=item.spell,
            spell_abb=item.spell_abb,
            show_color=item.show_color,
            show_itf=item.show_itf,
            show_btf=item.show_btf,
            image=item.image,
            sort=item.sort,
            is_delete=item.is_delete,
            is_site=item.is_site,
            is_scorearea=item.is_scorearea,
            is_lubearea=item.is_lubearea
        )

        area_map[item.id] = area.id
    print 'move area:', old_area.count()

'''
# 第二部分：互相依赖基础数据
'''
'''
# 商品分类部分
'''
# category:分类
category_map = {}

def move_category():
    old_category = Old_PinPaiType.select()
    for item in old_category:
        category = New_Category.create(
            name=item.name,
            sort=1,  # 旧的没有
            img_m=None,  # 旧的没有
            hot=1,  # 旧的没有,设置默认值：0
            active=item.flag
        )

        category_map[item.id] = category.id
    print 'move_category:', old_category.count()

# categoryattribute:类型属性
category_attribute_map = {}

def move_categoryattribute():
    old_attribute = Old_PPTAttribute.select()
    for item in old_attribute:
        attribute = New_CategoryAttribute.create(
            category=category_map[item.PinPaiType.id],
            name=item.name,
            ename=item.ename,
            sort=0,  # 旧的没有，设置默认值：0（有效）
            active=1,  # 旧的没有，设置默认值：1（有效）
        )

        category_attribute_map[item.id] = attribute.id
    print 'move_categoryattribute:', old_attribute.count()

# categoryattributeitem:类型属性具体类型
category_att_item_map = {}

def move_categoryattributeitem():
    old_item = Old_PPTAQuantity.select()
    for item in old_item:
        att_item = New_CategoryAttributeItems.create(
            category_attribute=category_attribute_map[item.PPTA_id.id],
            name=item.name,
            intro="默认",
            sort=0  # 旧的没有，设置默认值：0（有效）
        )
        category_att_item_map[item.id] = att_item.id
    print 'move_categoryattributeitem:%d' % old_item.count()

'''
# 商品品牌部分
'''
# brand:品牌
# 备注：保险品牌是否和商品品牌分开
brand_map = {}

def move_brand():
    old_brand = Old_PinPai.select()
    bimg = {
        'SK':'http://img.520czj.com/image/2017/06/01/server1_20170601175334WndwPBvCXehYyRcJuapMGTQF.jpg',
        'JDS':'http://img.520czj.com/image/2017/06/01/server1_20170601175436WfNoPAZOSYRMQgTXtadeGrFU.jpg',
        'DDE':'http://img.520czj.com/image/2017/06/01/server1_20170601175241mqPXrYtVWNkiLfCpIKJjyQHZ.jpg',
        'Mobil':'http://img.520czj.com/image/2017/06/01/server1_20170601183330gTDhpLetGxoMZuNUlrbIJfRi.jpg',
        'QP':'http://img.520czj.com/image/2017/06/01/server1_20170601175411CWOdMwzhxfIXjJtRDpqavEYo.jpg',
        'JSD':'http://img.520czj.com/image/2017/05/27/server1_20170527183913vXMEoJHufAnkDCbwmIqcpaZN.png',
    }
    for item in old_brand:
        if not item.name:
            continue
        if item.engname in bimg.keys():
            brandimg = bimg[item.engname]
        else:
            brandimg = imgurl+item.logo if item.logo else ''
        brand = New_Brand.create(
            name=item.name,
            engname=item.engname,
            pinyin=item.pinyin,
            logo=brandimg,
            intro=item.intro,
            hot=0,  # 旧的没有，设置默认值：0(否)
            sort=1,  # 旧的没有,设置默认值：1
            active=1
        )
        brand_map[item.id] = brand.id
    print 'move_brand:', old_brand.count()

# brandcategory:品牌产品类型
def move_brandcategory():
    old_brandcategory = Old_PinPai.select()  # 过滤后只余下新数据库brand对应的PinPai数据

    old_data = [{
        'brand': brand_map[item.id],
        'category': category_map[item.ptype.id]
    } for item in old_brandcategory]

    New_BrandCategory.insert_many(old_data).execute()
    print 'move brandcategory:', len(old_data)

'''
# 管理员账号
'''
# adminuser:管理员账户
adminuser_map = {}  # adminuser id 映射表，在转移的时候记录下来，后边有需要指向其的外键的时候替换即可
from db_model import Referee
def move_adminuser():
    New_AdminUser.delete().execute()
    old_adminuser = Old_AdminUser.select()
    for item in old_adminuser:
        try:
            referer = Referee.get(Referee.name==item.username).number
        except Exception,e:
            referer = ''
        roles = 'G'
        if item.username.find('张晓华')>=0 or item.username.find('王琳')>=0:
            roles += item.roles
        else:
            roles = item.roles

        adminuser = New_AdminUser.create(
            username=item.username,
            password=item.password,
            mobile=item.mobile,
            email=item.email,
            code=referer,  # 旧的没找到，暂时设置空
            realname=item.realname,
            roles=roles,
            area_code='0030' if item.username == '余飞' else '',
            signuped=item.signuped,
            lsignined=item.lsignined,
            active=item.isactive
        )
        adminuser_map[item.id] = adminuser.id
    print 'move admin user:', old_adminuser.count()

# adminuserlog: 管理账户日志
def move_adminuserlog():
    old_adminlog = Old_AdminLog.select().where(Old_AdminLog.user << adminuser_map.keys())
    old_data = [{
        'admin_user': adminuser_map[item.user.id],
        'created': item.dotime,
        'content': item.content
    } for item in old_adminlog]

    New_AdminUserLog.insert_many(old_data).execute()
    print 'move_adminlog', old_adminlog.count()
'''
# 店铺相关
'''
# store:店铺
store_map = {}
from db_model import RefereeUsers
def move_store():
    old_store = Old_Store.select()
    for item in old_store:
        try:
            user = Old_User.get(Old_User.store == item)
        except Exception:
            continue
        try:
            ref = RefereeUsers.get(RefereeUsers.store == item.id).refereeNum
        except Exception,e:
            ref = ''
        if user.grade == 5:
            grade = 1
            process_insurance = 1
        elif user.grade == 3:
            grade = 1
            process_insurance = 0
        else:
            grade = 2
            process_insurance = 0
        store = New_Store.create(
            store_type=grade,
            admin_code=ref,  # 旧的没有
            admin_user=None,  # 旧的没有
            name=item.name,
            area_code=item.area_code,
            address=item.address,
            legal_person=item.link_man,
            license_code=None,  # 旧的没有
            license_image=imgurl+item.image_license,
            store_image=imgurl+item.image,
            lng=item.x,
            lat=item.y,
            pay_password=None,  # 旧的没有
            intro=item.intro,
            linkman=item.link_man,
            mobile=item.mobile,
            price=user.cashed_money+user.score,  # 由店铺对应用户转移而来
            process_insurance=process_insurance,  # 旧的没有，暂时这样处理
            score=0,  # 旧的没有，不知道这样处理对不对
            active=item.check_state,
            created=item.created
        )

        store_map[item.id] = store.id
    print 'move store:', old_store.count()

# storebank:店铺账户
def move_storebankaccount():
    old_bank = Old_User.select().where(Old_User.store << store_map.keys())
    old_data = []
    for item in old_bank:
        if item.alipay_account:
            old_data.append({
                'store': store_map[item.store.id],
                'account_type': 1,  # 账户类型 0银联 1支付宝
                'alipay_truename': item.alipay_truename,
                'alipay_account': item.alipay_account,
                'bank_truename': '',
                'bank_account': '',
                'bank_name': '',
                'is_default': 0  # 旧的没有，设置默认值：0（否）
            })
        if item.bank_account:
            old_data.append({
                'store': store_map[item.store.id],
                'account_type': 0,  # 账户类型 0银联 1支付宝
                'alipay_truename': '',
                'alipay_account': '',
                'bank_truename': item.bank_truename,
                'bank_account': item.bank_account,
                'bank_name': item.bank_name,
                'is_default': 0  # 旧的没有，设置默认值：0（否）
            })

    New_StoreBankAccount.insert_many(old_data).execute()
    print 'move storebankaccount', old_bank.count()

# storearea:店铺服务区域
def move_storearea():
    old_area = Old_StoreServerArea.select()
    old_data = [{
        'area': area_map[item.aid.id],
        'store': store_map[item.sid.id]
    } for item in old_area]
    New_StoreArea.insert_many(old_data).execute()
    print 'move storearea:', old_area.count()

'''
# 店铺用户
'''
# user:用户账号
user_map = {}

def move_user():
    old_user = Old_User.select()
    for item in old_user:
        try:
            if (not item.store) or (not store_map.has_key(item.store.id)):
                continue
        except Exception:
            continue
        user = New_User.create(
            mobile=item.mobile,
            password=item.password,
            truename=item.nickname,
            role=item.userlevel,
            signuped=item.signuped,
            lsignined=item.lsignined,
            store=store_map[item.store.id],
            token=None,  # 旧的没有
            last_pay_type=1,  # 旧的没有，设置默认值：1
            active=item.isactive
        )
        user_map[item.id] = user.id
    print 'move users:', old_user.count()

# storeaddress:店铺收货地址
store_addr_map = {}
def move_storeaddress():
    old_user = Old_User.select().where(Old_User.store << store_map.keys())
    old_address = Old_UserAddr.select().where(Old_UserAddr.user << old_user)
    for item in old_address:
        storeaddress = New_StoreAddress.create(
                        store=store_map[item.user.store.id],
                        province=item.province,
                        city=item.city,
                        region=item.region,
                        address=item.address,
                        name=item.name,
                        mobile=item.mobile,
                        is_default=item.isdefault,
                        created=0,  # 旧的没有，设置默认值：0
                        create_by=user_map[item.user.id]
                    )
        store_addr_map[item.id] = storeaddress.id
    print 'move storeaddress:', old_address.count()

# scorerecord:积分流水
def move_scorerecord():
    old_record = Old_Score.select().where(Old_Score.user << user_map.keys())
    scoretype = {
        0:1,
        1:2
    }
    old_data = [{
        'user': user_map[item.user.id],
        'store': store_map[item.user.store.id],
        'ordernum': item.orderNum,
        'type': item.jftype,
        'process_type': scoretype[item.stype],
        'process_log': item.log,
        'score': item.score,
        'created': item.created,
        'status': item.isactive
    } for item in old_record]

    New_ScoreRecord.insert_many(old_data).execute()
    print 'move scorerecord:', len(old_data)

# moneyrecord:资金流水
def move_moneyrecord():
    old_record = Old_Withdraw.select().where(Old_Withdraw.user << user_map.keys())
    old_data = [{
        'user': user_map[item.user.id],
        'store': store_map[item.user.store.id],
        'process_type': 2,  # 1.0系统提现都为出钱。所以设置为2
        'type': 1,
        'process_message': item.processing_result,
        'process_log': '',
        'in_num': '',  # 旧的没有
        'out_account_type': item.account_type,
        'out_account_truename': item.account_truename,
        'out_account_account': item.account_account,
        'out_account_name': item.account_branchname,
        'money': item.sum_money,
        'status': item.status,
        'apply_time': item.apply_time,
        'processing_time': item.processing_time,
        'processing_by': adminuser_map[item.processing_by.id]
    } for item in old_record if item.user.store and item.processing_by]

    New_MoneyRecord.insert_many(old_data).execute()
    print 'move moneyrecord:', len(old_data)

# # block:广告区域
block_map = {}
'''
# 广告部分
'''
def move_block():
    block = New_Block.create(
        tag='banner',
        name='手机b端上方banner轮播位置',
        active=1  # 旧的没有，设置默认 值1（有效）
    )

    block_map[block.id] = block.id

    print 'move block:', 1

# blockitem：广告
block_item_map = {}

def move_blockitem():

    New_BlockItem.create(area_code='',block= 1,name='人保车险',link='czj://insurance/13',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527181018hmjKPAJzqkWLIauDBxwfNQTd.jpg')
    New_BlockItem.create(area_code='', block=1, name='安盛保险', link='czj://insurance/15',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527180904UVCJzBIlGWxndOXPKemvELbc.jpg')
    New_BlockItem.create(area_code='', block=1, name='太平洋保险', link='czj://insurance/12',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527181032McbqYutagRDsTyUGJFILhSXQ.jpg')
    New_BlockItem.create(area_code='', block=1, name='大地保险', link='czj://insurance/10',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527180922KTOStzdYavZfXPrERAjkQBuU.jpg')
    New_BlockItem.create(area_code='', block=1, name='国寿财', link='czj://insurance/11',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527180941PSwNaUJcjBTMOuFKmxzhCyEQ.jpg')
    New_BlockItem.create(area_code='', block=1, name='平安车险', link='czj://insurance/9',
                         img='http://img.520czj.com/image/2017/05/27/server1_20170527180958tbVqFrUywOpHhPKBRDlXAvLm.jpg')

    print 'move blockitem:', 6

# blockitemarea:广告投放区域
def move_blockitemarea():
    old_blockitem = Old_Ad.select()
    old_data = [{
            'block_item': 1,
            'area_code': ''
        },
        {
            'block_item': 2,
            'area_code': '0027'
        },
        {
            'block_item': 3,
            'area_code': '0004'
        },
        {
            'block_item': 4,
            'area_code': '00160016'
        },
        {
            'block_item': 5,
            'area_code': '00160016'
        },
        {
            'block_item': 6,
            'area_code': '00300004'
        }
    ]

    print 'move blockitemarea:', len(old_data)
    New_BlockItemArea.insert_many(old_data).execute()
'''
# 产品部分
'''
# product:产品
product_map = {}

def move_product():
    old_prodcut = Old_Product.select().where(Old_Product.is_index == 0)
    for item in old_prodcut:
        product = New_Product.create(
            name=item.name,
            brand=brand_map[item.pinpai.id],
            category=category_map[item.pinpai.ptype.id],
            resume=item.resume,
            unit='单位',  # 旧的没有，暂时设置，后期人工处理
            intro=item.intro.replace('src="','src="%s'%imgurl),
            cover=imgurl+item.cover if item.cover else '',
            is_score=item.is_score,
            created=item.created,
            active=item.status  # 旧的没有，暂时这样处理
        )
        try:
            if item.LA.count():
                for la in item.LA:
                    if la.level and la.classes and la.capacity and la.viscosity:
                        level  = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'level')
                        level_cls = New_CategoryAttributeItems.get(New_CategoryAttributeItems.name == la.level,
                                                                   New_CategoryAttributeItems.category_attribute == level.id)
                        print product.id,level.id,level_cls.id,la.level
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=level.id,
                            attribute_item=level_cls.id,
                            value=la.level
                        )
                        classes = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'classes')
                        classes_cls = New_CategoryAttributeItems.get(New_CategoryAttributeItems.name == la.classes,
                                                                   New_CategoryAttributeItems.category_attribute == classes.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=classes.id,
                            attribute_item=classes_cls.id,
                            value=la.classes
                        )
                        capacity = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'capacity')
                        capacity_cls = New_CategoryAttributeItems.get(New_CategoryAttributeItems.name == la.capacity,
                                                                     New_CategoryAttributeItems.category_attribute == capacity.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=capacity.id,
                            attribute_item=capacity_cls.id,
                            value=la.capacity
                        )
                        viscosity = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'viscosity')
                        viscosity_cls = New_CategoryAttributeItems.get(New_CategoryAttributeItems.name == la.viscosity,
                                                                     New_CategoryAttributeItems.category_attribute == viscosity.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=viscosity.id,
                            attribute_item=viscosity_cls.id,
                            value=la.viscosity
                        )
                    else:
                        continue
            if item.NA.count():
                for na in item.NA:
                    if na.configuration and na.CAN and na.size:
                        configuration = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'configuration')
                        configuration_cls = New_CategoryAttributeItems.get(New_CategoryAttributeItems.name == na.configuration,
                                                                       New_CategoryAttributeItems.category_attribute == configuration.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=configuration.id,
                            attribute_item=configuration_cls.id,
                            value=na.configuration
                        )
                        can = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'CAN')
                        can_cls = New_CategoryAttributeItems.get(
                            New_CategoryAttributeItems.name == na.CAN,
                            New_CategoryAttributeItems.category_attribute == can.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=can.id,
                            attribute_item=can_cls.id,
                            value=na.CAN
                        )
                        size = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'psize')
                        size_cls = New_CategoryAttributeItems.get(
                            New_CategoryAttributeItems.name == na.size,
                            New_CategoryAttributeItems.category_attribute == size.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=size.id,
                            attribute_item=size_cls.id,
                            value=na.size
                        )
                    else:
                        continue
            if item.RA.count():
                for ra in item.RA:
                    if ra.size and ra.lens:
                        size = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'jsize')
                        size_cls = New_CategoryAttributeItems.get(
                            New_CategoryAttributeItems.name == ra.size,
                            New_CategoryAttributeItems.category_attribute == size.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=size.id,
                            attribute_item=size_cls.id,
                            value=ra.size
                        )
                        lens = New_CategoryAttribute.get(New_CategoryAttribute.ename == 'lens')
                        lens_cls = New_CategoryAttributeItems.get(
                            New_CategoryAttributeItems.name == ra.size,
                            New_CategoryAttributeItems.category_attribute == size.id)
                        New_ProductAttributeValue.get_or_create(
                            product=product.id,
                            attribute=lens.id,
                            attribute_item=lens_cls.id,
                            value=ra.size
                        )
                    else:
                        continue
        except Exception,e:
            print e
            product.active = 0
            product.save()
            continue
        product_map[item.id] = product.id
    print 'move product:', old_prodcut.count()

# productpic:产品附图
def move_productpic():
    old_productpic = Old_ProductPic.select().where(Old_ProductPic.product << product_map.keys())
    old_data = [{
                    'product': product_map[item.product.id],
                    'pic': imgurl+item.path if item.path else '',
                    'sort': 0  # 旧的没有，设置为默认值：0
                } for item in old_productpic]
    print 'move productpic:', len(old_data)
    New_ProductPic.insert_many(old_data).execute()

# productattributevalue:产品型号
# def move_productattributevalue():
#     old_attribute = Old_ProductAttribute.select()
#     old_data = [{
#         'product': product_map[item.product.id],
#         'attribute': item.attribute,
#         'attribute_item': 0,  # 旧的没有，需要额外处理
#         'value': 0,  # 旧的没有，需要额外处理
#     } for item in old_attribute]
#
#     if old_data:
#         New_ProductAttributeValue.insert_many(old_data).execute()
#     print 'move productattributevalue:', len(old_data)

# productrelease:产品发布
product_release_map = {}

def move_productrelease():
    old_release = Old_ProductStandard.select().where(Old_ProductStandard.product << product_map.keys())
    step = 0
    for item in old_release:
        try:
            if not store_map.has_key(item.store.id):
                continue
        except Exception:
            continue

        release = New_ProductRelease.create(
            product=product_map[item.product.id],
            store=store_map[item.store.id],
            price=item.price,
            buy_count=item.orders,
            is_score=item.is_score,
            sort=item.weights,
            active=item.is_pass
        )
        step += 1
        product_release_map[item.id] = release.id
        product = New_Product.get(id=product_map[item.product.id])
        product.unit = item.unit
        product.save()

    print 'move productrelease:', step, '/', old_release.count()

# storeproductprice:店铺区域产品价格
store_product_price_map = {}

def move_storeproductprice():
    old_price = Old_ProductStandard.select().where(Old_ProductStandard.product << product_map.keys())
    step = 0
    for item in old_price:
        try:
            if not store_map.has_key(item.store.id):
                continue
        except Exception:
            continue
        price = New_StoreProductPrice.create(
            product_release=product_release_map[item.id],
            store=store_map[item.store.id],
            area_code=item.area_code,
            price=item.ourprice,
            score=item.scoreNum,  # 旧的没有，设置默认值：0
            created=item.add_time,
            active=1  # 旧的没有，设置默认值：1
        )
        step += 1
        store_product_price_map[item.id] = price.id
    print 'move storeproductprice:', step

'''
# 保险部分
'''
# insurance:保险公司
insurance_map = {}

def move_insurance():
    old_insurance = Old_Product.select().where(Old_Product.is_index == 1)
    ihs = {
        1: 1,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
    }
    iss = {
        1: 13,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 10,
        7: 11,
        8: 14,
        9: 5,
        10: 9,
        11: 8,
        12: 7,
        13: 15,
        14: 6,
        15: 12,
    }
    for item in old_insurance:
        insurance = New_Insurance.create(
            name=item.name,
            eName='',
            intro=item.resume[:50], #字符串长度太长，暂时设置为空
            logo=imgurl+item.cover,
            sort=0,  # 旧的没有，设置默认值：0
            hot=1,
            active=item.status  # 旧的没有，设置默认值：1（有效）
        )
        insurance.hot = ihs[insurance.id]
        insurance.sort = iss[insurance.id]
        insurance.save()
        insurance_map[item.id] = insurance.id
    print 'move insurance:', old_insurance.count()

# insuranceitems:保险子项目
insurance_item_map = {}

# def move_insuranceitems():
#     old_insurance_items = Old_Insurances.select()
#     for item in old_insurance_items:
#         insurance_item = New_InsuranceItem.create(
#             name=item.name,
#             eName=item.eName,
#             style=item.style,
#             style_id=1,  # 旧的数据库和model字段不匹配，暂时设置为1
#             sort=item.sort,
#         )
#         insurance_item_map[item.id] = insurance_item.id
#     print 'move insuranceitems:', old_insurance_items.count()

def move_insurancearea():
    old_area = Old_CurrencyExchangeList.select()
    old_data = []
    tmp = []
    for item in old_area:
        try:
            if item.iid.id == 0:
                continue
        except Exception:
            continue
        if (item.iid.id, item.area_code) in tmp:
            continue
        else:
            tmp.append((item.iid.id, item.area_code))
            old_data.append({
                'area_code': item.area_code,
                'insurance': insurance_map[item.iid.id],
                'lube_ok': 1,  # 旧的没有，设置默认值：1
                'score_ok': 1,  # 旧的没有，设置默认值：1
                'sort': 0,  # 旧的没有，设置默认值：0
                'active': item.iswork
            })
    print 'move insurancearea:', len(old_data)
    if old_data:
        New_InsuranceArea.insert_many(old_data).execute()

# insuranceprice:保额
# def move_insuranceprice():
#     old_price = Old_InsurancePrice.select()
#     old_data = [{
#         'insurance_item': insurance_item_map[item.pid.id],
#         'coverage': item.name,
#         'coveragenum': 0
#     } for item in old_price]
#     print 'move insuranceprice', len(old_data)
#     New_InsurancePrice.insert_many(old_data).execute()

# insurancescoreexchange:保险积分兑换规则
# def move_insuranceexchange():
#     old_exchange = Old_CurrencyExchangeList.select()
#     old_data = []
#     for item in old_exchange:
#         try:
#             if item.iid.id == 0:
#                 continue
#         except Exception:
#             continue
#         old_data.append({
#             'area_code': item.area_code,
#             'insurance': insurance_map[item.iid.id],
#             'created': item.localtime,
#
#             'business_exchange_rate': item.rate,
#             'business_exchange_rate2': 0,  # 旧的没有
#             'business_tax_rate': item.businessTaxRate,
#
#             'force_exchange_rate': item.forceRate,
#             'force_exchange_rate2': 0,  # 旧的没有
#             'force_tax_rate': item.forceTaxRate,
#
#             'ali_rate': item.aliRate,
#             'profit_rate': item.profitRate,
#             'base_money': item.baseMoney
#         })
#     print 'move insuranceexchange:', len(old_data)
#     New_InsuranceScoreExchange.insert_many(old_data).execute()


def _has_dic(src=[], dickey=None):
    for index, item in enumerate(src):
        if item['gift'] == dickey:
            return index
    else:
        return -1


'''
# 第三部分：互相依赖记录数据
'''
# feedback:反馈建议
def move_feedback():
    old_feedback = Old_Feedback.select().where(Old_Feedback.user << user_map.keys())
    old_data = [{
        'user': user_map[item.user.id],
        'suggest': item.content,
        'img': ''  # 旧的没有
    } for item in old_feedback]
    print 'move feedback:', len(old_data)
    New_Feedback.insert_many(old_data).execute()

# insuranceorderprice:保险报价单
insurance_order_price_map = {}

# def move_insuranceporderprice():
#     old_insurance_order_price = Old_InsuranceOrder.select().where(Old_InsuranceOrder.insurance << insurance_map.keys())
#     for item in old_insurance_order_price:
#         try:
#             adminuser = New_AdminUser.get(New_AdminUser.name == item.lasteditedby)
#         except Exception:
#             adminuser = New_AdminUser.get(New_AdminUser.id == 1)
#         insuranceorderprice = New_InsuranceOrderPrice.create(
#             insurance_order_id=0,  # 旧的没有
#             insurance=insurance_map[item.insurance.id],
#             created=item.ordered,  # 旧的没有
#             admin_user=adminuser,  # 旧的没有
#             gift_policy=item.LubeOrScore,
#             response=1,  # 旧的没有
#             status=1,  # 旧的没有
#             score=0,  # 旧的没有
#             cash=0,
#             total_price=item.price,  # 保险订单总价格
#             force_price=item.forceIprc,  # 交强险 价格
#             business_price=item.businessIprc,  # 商业险价格
#             vehicle_tax_price=item.vehicleTax,  # 车船税价格
#             sms_content=0,  # 旧的没有
#
#             # 交强险
#             forceI=0,  # 是否包含交强险
#             forceIPrice=0,
#
#             # 商业险-主险-车辆损失险
#             damageI=0,
#             damageIPrice=0,
#             damageIPlus=0,
#             damageIPlusPrice=0,
#
#             # 商业险-主险-第三者责任险，含保额
#             thirdDutyI=0,
#             thirdDutyIPrice=0,
#             thirdDutyIPlus=0,
#             thirdDutyIPlusPrice=0,
#
#             # 商业险-主险-机动车全车盗抢险
#             robbingI=0,
#             robbingIPrice=0,
#             robbingIPlus=0,
#             robbingIPlusPrice=0,
#
#             # 商业险-主险-机动车车上人员责任险（司机），含保额
#             driverDutyI=0,
#             driverDutyIPrice=0,
#             driverDutyIPlus=0,
#             driverDutyIPlusPrice=0,
#
#             # 商业险-主险-机动车车上人员责任险（乘客），含保额
#             passengerDutyI=0,
#             passengerDutyIPrice=0,
#             passengerDutyIPlus=0,
#             passengerDutyIPlusPrice=0,
#
#             # 商业险-附加险-玻璃单独破碎险
#             glassI=0,
#             glassIPrice=0,
#
#             # 商业险-附加险-车身划痕损失险，含保额
#             scratchI=0,
#             scratchIPrice=0,
#             scratchIPlus=0,
#             scratchIPlusPrice=0,
#
#             # 商业险-附加险-自燃损失险
#             fireDamageI=0,
#             fireDamageIPrice=0,
#             fireDamageIPlus=0,
#             fireDamageIPlusPrice=0,
#
#             # 商业险-附加险-发动机涉水损失险
#             wadeI=0,
#             wadeIPrice=0,
#             wadeIPlus=0,
#             wadeIPlusPrice=0,
#
#             # 商业险-附加险-机动车损失保险无法找到第三方特约金
#             thirdSpecialI=0,
#             thirdSpecialIPrice=0,
#         )
#         insurance_order_price_map[item.id] = insuranceorderprice.id
#     print 'move insuranceorderprice', old_insurance_order_price.count()

# insuranceorder:保险订单
def move_insuranceorder():
    old_order = Old_InsuranceOrder.select().where(Old_InsuranceOrder.insurance << insurance_map.keys())
    old_data = []
    paymentex = {
        1:1,
        6:2,
        7:3
    }
    for item in old_order:
        try:
            reciver = Old_InsuranceOrderReceiving.get(Old_InsuranceOrderReceiving.orderid == item)
        except Exception:
            continue
        try:
            adminuser = New_AdminUser.get(New_AdminUser.name == item.lasteditedby)
        except Exception:
            adminuser = New_AdminUser.get(New_AdminUser.id == 1)

        addr = reciver.address.decode('utf-8')

        forceI = 0
        if item.forceI:
            if item.forceI.find('t') >= 0:
                forceI = 1
            elif item.forceI.find('f') >= 0:
                forceI = 0
            elif item.forceI.find('万') >= 0 or item.forceI.find('千') >= 0:
                forceI = item.forceI

        damageI = 0
        if item.damageI:
            if item.damageI.find('t')>=0:
                damageI = 1
            elif item.damageI.find('f')>=0:
                damageI = 0
            elif item.damageI.find('万')>=0 or item.damageI.find('千')>=0:
                damageI = item.damageI

        damageSpecialI = 0
        if item.damageSpecialI:
            if item.damageSpecialI.find('t')>=0:
                damageSpecialI = 1
            elif item.damageSpecialI.find('f')>=0:
                damageSpecialI = 0
            elif item.damageSpecialI.find('万')>=0 or item.damageSpecialI.find('千')>=0:
                damageSpecialI = item.damageSpecialI

        thirdDutyI = 0
        if item.thirdDutyI:
            if item.thirdDutyI.find('t')>=0:
                thirdDutyI = 1
            elif item.thirdDutyI.find('f')>=0:
                thirdDutyI = 0
            elif item.thirdDutyI.find('万')>=0 or item.thirdDutyI.find('千')>=0:
                thirdDutyI = item.thirdDutyI

        thirdDutySpecialI = 0
        if item.thirdDutySpecialI:
            if item.thirdDutySpecialI.find('t')>=0:
                thirdDutySpecialI = 1
            elif item.thirdDutySpecialI.find('f')>=0:
                thirdDutySpecialI = 0
            elif item.thirdDutySpecialI.find('万')>=0 or item.thirdDutySpecialI.find('千')>=0:
                thirdDutySpecialI = item.thirdDutySpecialI

        robbingI = 0
        if item.robbingI:
            if item.robbingI.find('t')>=0:
                robbingI = 1
            elif item.robbingI.find('f')>=0:
                robbingI = 0
            elif item.robbingI.find('万')>=0 or item.robbingI.find('千')>=0:
                robbingI = item.robbingI

        robbingSpecialI = 0
        if item.robbingSpecialI:
            if item.robbingSpecialI.find('t')>=0:
                robbingSpecialI = 1
            elif item.robbingSpecialI.find('f')>=0:
                robbingSpecialI = 0
            elif item.robbingSpecialI.find('万')>=0 or item.robbingSpecialI.find('千')>=0:
                robbingSpecialI = item.robbingSpecialI

        driverDutyI = 0
        if item.driverDutyI:
            if item.driverDutyI.find('t')>=0:
                driverDutyI = 1
            elif item.driverDutyI.find('f')>=0:
                driverDutyI = 0
            elif item.driverDutyI.find('万')>=0 or item.driverDutyI.find('千')>=0:
                driverDutyI = item.driverDutyI

        driverDutySpecialI = 0
        if item.driverDutySpecialI:
            if item.driverDutySpecialI.find('t')>=0:
                driverDutySpecialI = 1
            elif item.driverDutySpecialI.find('f')>=0:
                driverDutySpecialI = 0
            elif item.driverDutySpecialI.find('万')>=0 or item.driverDutySpecialI.find('千')>=0:
                driverDutySpecialI = item.driverDutySpecialI

        passengerDutyI = 0
        if item.passengerDutyI:
            if item.passengerDutyI.find('t')>=0:
                passengerDutyI = 1
            elif item.passengerDutyI.find('f')>=0:
                passengerDutyI = 0
            elif item.passengerDutyI.find('万')>=0 or item.passengerDutyI.find('千')>=0:
                passengerDutyI = item.passengerDutyI

        passengerDutySpecialI = 0
        if item.passengerDutySpecialI:
            if item.passengerDutySpecialI.find('t')>=0:
                passengerDutySpecialI = 1
            elif item.passengerDutySpecialI.find('f')>=0:
                passengerDutySpecialI = 0
            elif item.passengerDutySpecialI.find('万')>=0 or item.passengerDutySpecialI.find('千')>=0:
                passengerDutySpecialI = item.passengerDutySpecialI

        glassI = 0
        if item.glassI:
            if item.glassI.find('t')>=0:
                glassI = 1
            elif item.glassI.find('f')>=0:
                glassI = 0
            elif item.glassI.find('万')>=0 or item.glassI.find('千')>=0:
                glassI = item.glassI

        scratchI = 0
        if item.scratchI:
            if item.scratchI.find('t')>=0:
                scratchI = 1
            elif item.scratchI.find('f')>=0:
                scratchI = 0
            elif item.scratchI.find('万')>=0 or item.scratchI.find('千')>=0:
                scratchI = item.scratchI

        scratchSpecialI = 0
        if item.scratchSpecialI:
            if item.scratchSpecialI.find('t')>=0:
                scratchSpecialI = 1
            elif item.scratchSpecialI.find('f')>=0:
                scratchSpecialI = 0
            elif item.scratchSpecialI.find('万')>=0 or item.scratchSpecialI.find('千')>=0:
                scratchSpecialI = item.scratchSpecialI

        normalDamageI = 0
        if item.normalDamageI:
            if item.normalDamageI.find('t')>=0:
                normalDamageI = 1
            elif item.normalDamageI.find('f')>=0:
                normalDamageI = 0
            elif item.normalDamageI.find('万')>=0 or item.normalDamageI.find('千')>=0:
                normalDamageI = item.normalDamageI

        normalDamageSpecialI = 0
        if item.normalDamageSpecialI:
            if item.normalDamageSpecialI.find('t')>=0:
                normalDamageSpecialI = 1
            elif item.normalDamageSpecialI.find('f')>=0:
                normalDamageSpecialI = 0
            elif item.normalDamageSpecialI.find('万')>=0 or item.normalDamageSpecialI.find('千')>=0:
                normalDamageSpecialI = item.normalDamageSpecialI

        wadeI = 0
        if item.wadeI:
            if item.wadeI.find('t')>=0:
                wadeI = 1
            elif item.wadeI.find('f')>=0:
                wadeI = 0
            elif item.wadeI.find('万')>=0 or item.wadeI.find('千')>=0:
                wadeI = item.wadeI

        wadeSpecialI = 0
        if item.wadeSpecialI:
            if item.wadeSpecialI.find('t')>=0:
                wadeSpecialI = 1
            elif item.wadeSpecialI.find('f')>=0:
                wadeSpecialI = 0
            elif item.wadeSpecialI.find('万')>=0 or item.wadeSpecialI.find('千')>=0:
                wadeSpecialI = item.wadeSpecialI

        thirdSpecialI = 0
        if item.thirdSpecialI:
            if item.thirdSpecialI.find('t')>=0:
                thirdSpecialI = 1
            elif item.thirdSpecialI.find('f')>=0:
                thirdSpecialI = 0
            elif item.thirdSpecialI.find('万')>=0 or item.thirdSpecialI.find('千')>=0:
                thirdSpecialI = item.thirdSpecialI

        iop = New_InsuranceOrderPrice.create(
            insurance_order_id=0,  # 旧的没有
            insurance=insurance_map[item.insurance.id],
            created=item.ordered,  # 旧的没有
            admin_user=adminuser,  # 旧的没有
            gift_policy=item.LubeOrScore,
            response=1,  # 旧的没有
            status=1,  # 旧的没有
            score=0,  # 旧的没有
            cash=0,
            total_price=item.price,  # 保险订单总价格
            force_price=item.forceIprc,  # 交强险 价格
            business_price=item.businessIprc,  # 商业险价格
            vehicle_tax_price=item.vehicleTax,  # 车船税价格
            sms_content=item.summary,  # 旧的没有

            # 交强险
            forceI=forceI,  # 是否包含交强险
            forceIPrice=item.forceIprc,

            # 商业险-主险-车辆损失险
            damageI=damageI,
            damageIPrice=0,
            damageIPlus=damageSpecialI,
            damageIPlusPrice=0,

            # 商业险-主险-第三者责任险，含保额
            thirdDutyI=thirdDutyI,
            thirdDutyIPrice=0,
            thirdDutyIPlus=thirdDutySpecialI,
            thirdDutyIPlusPrice=0,

            # 商业险-主险-机动车全车盗抢险
            robbingI=robbingI,
            robbingIPrice=0,
            robbingIPlus=robbingSpecialI,
            robbingIPlusPrice=0,

            # 商业险-主险-机动车车上人员责任险（司机），含保额
            driverDutyI=driverDutyI,
            driverDutyIPrice=0,
            driverDutyIPlus=driverDutySpecialI,
            driverDutyIPlusPrice=0,

            # 商业险-主险-机动车车上人员责任险（乘客），含保额
            passengerDutyI=passengerDutyI,
            passengerDutyIPrice=0,
            passengerDutyIPlus=passengerDutySpecialI,
            passengerDutyIPlusPrice=0,

            # 商业险-附加险-玻璃单独破碎险
            glassI=glassI,
            glassIPrice=0,

            # 商业险-附加险-车身划痕损失险，含保额
            scratchI=scratchI,
            scratchIPrice=0,
            scratchIPlus=scratchSpecialI,
            scratchIPlusPrice=0,

            # 商业险-附加险-自燃损失险
            fireDamageI=normalDamageI,
            fireDamageIPrice=0,
            fireDamageIPlus=normalDamageSpecialI,
            fireDamageIPlusPrice=0,

            # 商业险-附加险-发动机涉水损失险
            wadeI=wadeI,
            wadeIPrice=0,
            wadeIPlus=wadeSpecialI,
            wadeIPlusPrice=0,

            # 商业险-附加险-机动车损失保险无法找到第三方特约金
            thirdSpecialI=thirdSpecialI,
            thirdSpecialIPrice=0,
        )
        io = New_InsuranceOrder.create(
            ordernum= item.ordernum,
            user= user_map[item.user.id],
            store= store_map[item.store.id],
            current_order_price= iop.id,

            id_card_front= imgurl+item.idcard if item.idcard else '',
            id_card_back= imgurl+item.idcardback if item.idcardback else '',
            drive_card_front= imgurl+item.drivercard if item.drivercard else '',
            drive_card_back= imgurl+item.drivercard2 if item.drivercard2 else '',
            payment= paymentex[item.payment],
            ordered= item.ordered,

            delivery_to= reciver.contact,
            delivery_tel= reciver.mobile,
            delivery_province= addr[:addr.find(u'省')+1],
            delivery_city= addr[addr.find(u'省')+1:addr.find(u'市')+1],
            delivery_region= addr[addr.find(u'市'):addr.find(u'市')+3],
            delivery_address= reciver.paddress,
            deliver_company= '',
            deliver_num= '',

            status= -1 if item.status == 5 else item.status,
            cancel_reason= item.cancelreason,
            cancel_time= item.canceltime,
            sms_content= '',  # 就得没有，暂时设置，后期需要人工处理
            sms_sent_time= item.paytime,
            local_summary= item.localsummary,
            pay_time= item.paytime,
            deal_time= item.ordered,
            order_count= 0,
            pay_account= item.pay_account,
            trade_no= item.trade_no,
            user_del= item.userDel
        )

        iop.insurance_order_id = io.id
        iop.save()

    # New_InsuranceOrder.insert_many(old_data).execute()
    # print 'move insuranceorder:', len(old_data)

# settlement:结算
settlement_map = {}
def move_settlement():
    old_settlement = Old_Settlement.select().where(Old_Settlement.user << user_map.keys())
    for item in old_settlement:
        settlement = New_Settlement.create(
            user=user_map[item.user.id],
            sum_money=item.sum_money,
            created=item.created
        )
        settlement_map[item.id] = settlement.id
    print 'move settlement:', old_settlement.count()

# order:产品订单
order_map = {}

def move_Order():
    old_order = Old_Order.select().where(Old_Order.user << user_map.keys())
    paymentex = {
        7:3,
        6:2,
        1:1
    }
    for item in old_order:
        # try:
        #     if item.delivery:
        #         delivery=delivery_map[item.delivery.id]
        #         deliverynum = item.deliverynum
        #     else:
        #         delivery = None
        #         deliverynum = None
        # except Exception:
        #     pass
        if item.payment == 8:
            continue

        order = New_Order.create(
            ordernum=item.ordernum,
            user=user_map[item.user.id],
            buyer_store=store_map[item.user.store.id],  # 旧的没有，暂时设置0
            delivery_to=item.address.name,
            delivery_tel=item.address.mobile,
            delivery_province=item.address.province,
            delivery_city=item.address.city,
            delivery_region=item.address.region,
            delivery_address=item.address.address,
            # address=store_addr_map[item.address.id],
            # delivery=delivery,
            # delivery_num=deliverynum,
            ordered=item.ordered,
            payment=paymentex[item.payment],
            message=item.message,
            order_type=item.is_score+1,  # 付款方式 1金钱订单 2积分订单
            total_price=item.currentprice,  # 就得没有，暂时设置为这个
            total_score=item.scoreNum,
            pay_balance=item.pay_balance,
            pay_price=0,  # 旧的没有，暂时设置默认值
            pay_time=item.paytime,
            status= -1 if item.status == 5 else item.status,
            trade_no=item.trade_no,
            order_count=0,
            buyer_del=0  # 旧的没有，暂时设置
        )
        order_map[item.id] = order.id
    print 'move order:', old_order.count()

# orderitem:订单内容
def move_orderitem():
    old_orderitem = Old_OrderItem.select().where(Old_OrderItem.product_standard << product_release_map.keys())
    for item in old_orderitem:
        try:

            order = Old_Order.get(Old_Order.id == item.order.id)
            if not order_map.has_key(order.id):
                continue
            productstandard = Old_ProductStandard.get(Old_ProductStandard.id == item.product_standard.id)
        except Exception:
            continue
        try:
            settlement = Old_Settlement.get(Old_Settlement.id == order.settlement.id)
        except Exception:
            settlement = None

        try:
            if item.order.delivery:
                delivery=delivery_map[item.order.delivery.id]
                deliverynum = item.order.deliverynum
            else:
                delivery = None
                deliverynum = None
        except Exception:
            pass

        suborder = New_SubOrder.get_or_create(
            order=order_map[order.id],
            saler_store=store_map[item.product_standard.store.id],
            buyer_store=store_map[order.user.store.id],
            price=item.price,
            status=order.status,
            delivery=delivery,
            delivery_num=deliverynum,
            fail_reason=order.cancelreason,
            fail_time=order.canceltime,
            delivery_time=order.delivery_time,
            settlement=settlement_map[settlement.id] if settlement else None,
            saler_del=0,
            buyer_del=0
        )

        New_OrderItem.create(
            order=order_map[item.order.id],
            sub_order=suborder.id,  # 旧的没有，需要处理
            product=product_map[item.product.id],
            store_product_price=store_product_price_map[productstandard.id],
            quantity=item.quantity,
            price=item.price
        )

    print 'move orderitem:', old_orderitem.count()

# cart:购物车:购物车建议可以不导入
def move_cart():
    old_cart = Old_Cart.select().where(Old_Cart.user << user_map.keys())
    old_data = []
    for item in old_cart:
        try:
            if item.user.store.id:
                pass
        except Exception:
            continue
        old_data.append({
            'store': store_map[item.user.store.id],  # 旧的没有,是否指的是购买方
            'store_product_price': 1,  # 旧的没有,暂时设置，后期需要人工处理
            'quantity': item.quantity,
            'created': item.created
        })

    New_ShopCart.insert_many(old_data).execute()
    print 'move cart:', old_cart.count()


'''
# 从czj库导入补充数据
'''
from model_move import InsuranceItem as czjmoveInsuranceItem
from model_move import InsurancePrice as czjmoveInsurancePrice
from model_move import CarBrand as czjmoveCarBrand
from model_move import CarBrandFactory as czjmoveCarBrandFactory
from model_move import Car as czjmoveCar
from model_move import CarItemGroup as czjmoveCarItemGroup
from model_move import CarSK as czjmoveCarSK
from model_move import CarItem as czjmoveCarItem


from model import InsuranceItem as czjInsuranceItem
from model import InsurancePrice as czjInsurancePrice
from model import CarBrand as czjCarBrand
from model import CarBrandFactory as czjCarBrandFactory
from model import Car as czjCar
from model import CarItemGroup as czjCarItemGroup
from model import CarSK as czjCarSK
from model import CarItem as czjCarItem

def move_insuranceitem():
    old_it = czjInsuranceItem.select()
    old_data = [{
        'eName': item.eName,  # 英文名
        'name': item.name,  # 中文名
        'style': item.style,  # 分类名
        'style_id': item.style_id,  # 分类id 交强险1  商业险主险2  商业险附加险3
        'sort': item.sort  # 排序
    } for item in old_it]
    czjmoveInsuranceItem.insert_many(old_data).execute()
    print 'move insurance item',len(old_data)

def move_insuranceprice():
    old_it = czjInsurancePrice.select()
    old_data = [{
        'insurance_item': item.insurance_item,  # 子险种
        'coverage': item.coverage,  # 保险额度
        'coveragenum': item.coveragenum  # 保险额度数字
    } for item in old_it]
    czjmoveInsurancePrice.insert_many(old_data).execute()
    print 'move insurance price',len(old_data)

def move_carbrand():
    old_cb = czjCarBrand.select()
    old_data = [{
        'brand_name': item.brand_name,  # 汽车品牌
        'brand_pinyin_name': item.brand_pinyin_name,  # 汽车品牌拼音
        'logo': item.logo,  # 汽车品牌logo
        'brand_intro': item.brand_intro,  # 汽车品牌简介
        'brand_pinyin_first': item.brand_pinyin_first,  # 汽车品牌拼音首字母
        'catch_url': item.catch_url,  # 抓取详情页面路径
        'sort': item.sort,  # 同拼音下的排序
        'active': item.active  # 状态 0删除 1有效
    } for item in old_cb]
    czjmoveCarBrand.insert_many(old_data).execute()
    print 'move car brand',len(old_data)

def move_carbrandfactor():
    old_cbf = czjCarBrandFactory.select()
    old_data = [{
        'brand': item.brand,  # 汽车品牌
        'factory_name': item.factory_name,  # 汽车品牌厂家
        'logo': item.logo,  # 汽车品牌logo
        'factory_intro': item.factory_intro,  # 汽车品牌简介
        'sort': item.sort,  # 同品牌下的排序
        'active': item.active  # 状态 0删除 1有效
    } for item in old_cbf]
    czjmoveCarBrandFactory.insert_many(old_data).execute()
    print 'move carbrandfactory',len(old_data)

def move_car():
    old_c = czjCar.select()
    old_data = [{
        'car_name': item.car_name,# 汽车
        'car_pinyin_name': item.car_pinyin_name,# 汽车拼音
        'brand': item.brand,# 汽车品牌
        'factory': item.factory, # 汽车厂家
        'logo': item.logo,# 汽车logo，汽车的图片
        'catch_url': item.catch_url,# 抓取详情页面路径
        'stop_sale': item.stop_sale,# 停产？ 0正常销售 1已停产
        'sort':item.sort,  # 厂家或品牌下的排序
        'active': item.active  # 状态 0删除 1有效
    } for item in old_c]
    czjmoveCar.insert_many(old_data).execute()
    print 'move car',len(old_data)

caritemgroup = {}
def move_caritemgroup():
    old_c = czjCarItemGroup.select().where(czjCarItemGroup.id <= 5837)
    for item in old_c:
        cc = czjmoveCarItemGroup.create(
        car=item.car.id,  # 汽车
        group_name=item.group_name  # 汽车型号
        )
        caritemgroup[item.id]=cc.id
        print 'move carig:cc.id=',cc.id
    print 'move caritemgroup',old_c.count()
    #czjmoveCarItemGroup.insert_many(old_data).execute()

def move_carsk():
    old_c = czjCarSK.select()
    old_data = [{
        'name': item.name,  # 汽车
        'intro': item.intro,  # 汽车拼音
        'api_level': item.api_level,  # 汽车厂家
        'logo': item.logo,  # 汽车logo，汽车的图片
        'category': item.category,  # 抓取详情页面路径
        'active': item.active  # 状态 0删除 1有效
    } for item in old_c]
    czjmoveCarSK.insert_many(old_data).execute()
    print 'move carsk',len(old_data)

def move_caritem():
    old_c = czjCarItem.select()
    old_data = [{
        'car_item_name': item.car_item_name,  # 汽车型号
        'car': item.car,  # 汽车
        'group': caritemgroup[item.group.id],  # 所在分组
        'displacement': item.displacement,# 排量
        'gearbox': item.gearbox,  # 变速箱，AT自动，MT手动，8挡手自一体
        'actuator': item.actuator,  # 驱动方式，四驱，前驱，后驱
        'power': item.power,# 动力来源，汽油，柴油，电动，油电混合
        'sale_category': item.sale_category,  # 销售分组，如：在售，停售
        'catch_url': item.catch_url,  # 抓取详情页面路径
        'stop_sale': item.stop_sale,  # 停产？ 0正常销售 1已停产
        'sort': item.sort,  # 厂家或品牌下的排序
        'car_type': item.car_type,# 车型：suv或紧凑型车……
        'price': item.price,  # 指导价格
        'car_sk_engine_1': item.car_sk_engine_1,  # SK产品发动机推荐1
        'car_sk_engine_2': item.car_sk_engine_2,# SK产品发动机推荐2
        'car_sk_gearbox_1': item.car_sk_gearbox_1 if item.car_sk_gearbox_1 else None,  # SK产品变速箱推荐1
        'car_sk_gearbox_2': item.car_sk_gearbox_2 if item.car_sk_gearbox_2 else None,  # SK产品变速箱推荐2
        'brake_oil': item.brake_oil,  # SK产品刹车油
        'antifreeze_solution': item.antifreeze_solution,  # SK产品防冻液
        'active': item.active  # 状态 0删除 1有效
    } for item in old_c]
    czjmoveCarItem.insert_many(old_data).execute()
    print 'move car item',len(old_data)


# 地区返佣策略
from db_model import HelpCenter as Old_HelpCenter
from model_move import InsuranceArea
def move_lubeexchange():
    InsuranceArea.delete().execute()
    old_policy = Old_HelpCenter.select()
    tmp_area = []
    area_code_list = []
    for i in old_policy:
        if (i.area_code+i.iCompany) not in tmp_area:
            tmp_area.append(i.area_code+i.iCompany)
            area_code_list.append({'code': i.area_code, 'ic_name': i.iCompany})
    for al in area_code_list:
        i_list = []
        i_names = al['ic_name'].split('/')
        data = []
        for i_name in i_names:
            if i_name != u'太平':
                i_name += '%'
                insurance = New_Insurance.select().where(New_Insurance.name % i_name)
                i_id = insurance[0].id if insurance.count() > 0 else 0
            else:
                i_name = u'太平车险'
                insurance = New_Insurance.select().where(New_Insurance.name == i_name)
                i_id = insurance[0].id if insurance.count() > 0 else 0
            if i_id:
                i_list.append(i_id)
            else:
                print(u'---no i id--%s---' % i_name)
        for item in old_policy:
            if item.area_code == al['code']:
                try:
                    minp, maxp = item.price.split('-')
                    item_price = u'（%s）' % item.price
                except:
                    minp = item.price.strip(u'≥').strip(u'以上')
                    maxp = ''
                    item_price = u'%s以上' % minp
                if u'+' in item.insurance:
                    flag = 3
                elif u'单商业' in item.insurance:
                    flag = 2
                elif u'单交强' in item.insurance:
                    flag = 1
                else:
                    print(u'error: 不是单交强商业也不是商+交：%s' % item.id)
                gift_in = False
                for d in data:
                    if d['gift'] == item.driverGift:
                        d['items'].append({
                            'name': item.insurance + item_price,
                            'driver': item.driverGiftNum,
                            'store': item.party2GiftNum,
                            'minprice': minp,
                            'maxprice': maxp,
                            'flag': flag
                        })
                        gift_in = True
                if not gift_in:
                    data.append({
                        'gift': item.driverGift,
                        'items': [{
                            'name': item.insurance,
                            'driver': item.driverGiftNum,
                            'store': item.party2GiftNum,
                            'minprice': minp,
                            'maxprice': maxp,
                            'flag': flag
                        }]
                    })

        for i_id in i_list:
            InsuranceArea.create(
                area_code = al['code'],
                insurance = i_id,
                lube_ok = 1,
                dealer_store = 1,
                lube_policy = simplejson.dumps(data),
                cash_ok = 0,
                cash_policy = '',
                sort = 1,
                active = 1
            )

    ocs = Old_CurrencyExchangeList.select().where((Old_CurrencyExchangeList.iswork == 1) & (Old_CurrencyExchangeList.is_cash == 0))
    for oc in ocs:
        score_data = {"pr": 0,
                      "fer2": round(oc.forceRate * 100, 2),
                      "fer": round(oc.forceRate * 100),
                      "ftr": 0,
                      "ber2": round(oc.rate * 100),
                      "ber": round(oc.rate * 100),
                      "bm": 0,
                      "btr": 0,
                      "ar": 0}
        new_i = New_Insurance.select().where(New_Insurance.name == oc.iid.name)
        if new_i.count() > 0:
            i_id = new_i[0].id
            ias = InsuranceArea.select().where((InsuranceArea.insurance == i_id) & (InsuranceArea.area_code == oc.area_code))
            if ias.count() > 0:
                ias[0].cash_ok = 1
                ias[0].cash_policy = simplejson.dumps(score_data)
                ias[0].save()
            else:
                InsuranceArea.create(area_code=oc.area_code, insurance=i_id, lube_ok=0, dealer_store=1, lube_policy='',
                    cash_ok=1, cash_policy=simplejson.dumps(score_data), sort=1, active=1)
        else:
            print('---%s--' % oc.iid.name)


# 初始化地区经销商
def init_jingxiaoshang():
    service_store_mobile = ['15591601991', '18738808268', '18189180515', '18082239925', '13196328186',
                            '15909518062', '13571705078', '13772128583', '15909518079', '13323560933',
                            '18503516282', '18066546153', '18638886818', '13720628544']
    area_code_list = []
    area_store_list = []
    for m in service_store_mobile:
        try:
            ns = New_Store.get(mobile=m)
            if ns.area_code[:8] not in area_code_list:
                area_code_list.append(ns.area_code[:8])
                area_store_list.append({'area': ns.area_code[:8], 'store': ns.id})
        except Exception, e:
            print m
    for ac in area_store_list:
        area = ac['area'] + '%'
        for ia in InsuranceArea.select().where(InsuranceArea.area_code % area):
            ia.dealer_store = ac['store']
            ia.save()


# 初始化店铺的返佣规则
from model_move import SSILubePolicy as new_SSILubePolicy
def init_store_po():
    new_SSILubePolicy.delete().execute()
    for store in New_Store.select().where(New_Store.active == 1):
        for area_po in New_InsuranceArea.get_area_insurance(store.area_code):
            new_SSILubePolicy.create(store=store, insurance=area_po['insurance'], cash=area_po['cash'],
                                     dealer_store=area_po['dealer_store'], lube=area_po['lube'])

def update_store_po():
    for item in new_SSILubePolicy.select():
        if item.store.area_code.find(u'0027')==0:
            print item.store.area_code,item.id
            item.lube = '[{"items": [{"name": "\u5355\u5546\u4e1a\u9669", "driver": 3, "maxprice": "", "flag": 2, "minprice": "12500", "store": 17}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u966912500\u4ee5\u4e0a", "driver": 3, "maxprice": "", "flag": 3, "minprice": "12500", "store": 19}], "gift": "ZIC X9"}, {"items": [{"name": "\u5355\u5546\u4e1a\u9669", "driver": 3, "maxprice": "", "flag": 2, "minprice": "6000", "store": 16}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u96696000\u4ee5\u4e0a", "driver": 3, "maxprice": "", "flag": 3, "minprice": "6000", "store": 18}], "gift": "ZIC X7"}, {"items": [{"name": "\u5355\u5546\u4e1a\u9669", "driver": 3, "maxprice": "5399", "flag": 2, "minprice": "5100", "store": 15}, {"name": "\u5355\u5546\u4e1a\u9669\uff084900-5099\uff09", "driver": 3, "maxprice": "5099", "flag": 2, "minprice": "4900", "store": 14}, {"name": "\u5355\u5546\u4e1a\u9669\uff084600-4899\uff09", "driver": 3, "maxprice": "4899", "flag": 2, "minprice": "4600", "store": 13}, {"name": "\u5355\u5546\u4e1a\u9669\uff084300-4599\uff09", "driver": 3, "maxprice": "4599", "flag": 2, "minprice": "4300", "store": 12}, {"name": "\u5355\u5546\u4e1a\u9669\uff084100-4299\uff09", "driver": 3, "maxprice": "4299", "flag": 2, "minprice": "4100", "store": 11}, {"name": "\u5355\u5546\u4e1a\u9669\uff083800-4099\uff09", "driver": 3, "maxprice": "4099", "flag": 2, "minprice": "3800", "store": 10}, {"name": "\u5355\u5546\u4e1a\u9669\uff083500-3799\uff09", "driver": 3, "maxprice": "3799", "flag": 2, "minprice": "3500", "store": 9}, {"name": "\u5355\u5546\u4e1a\u9669\uff083300-3499\uff09", "driver": 3, "maxprice": "3499", "flag": 2, "minprice": "3300", "store": 8}, {"name": "\u5355\u5546\u4e1a\u9669\uff083000-3299\uff09", "driver": 3, "maxprice": "3299", "flag": 2, "minprice": "3000", "store": 7}, {"name": "\u5355\u5546\u4e1a\u9669\uff082700-2999\uff09", "driver": 3, "maxprice": "2999", "flag": 2, "minprice": "2700", "store": 6}, {"name": "\u5355\u5546\u4e1a\u9669\uff082500-2699\uff09", "driver": 3, "maxprice": "2699", "flag": 2, "minprice": "2500", "store": 5}, {"name": "\u5355\u5546\u4e1a\u9669\uff082200-2499\uff09", "driver": 3, "maxprice": "2499", "flag": 2, "minprice": "2200", "store": 4}, {"name": "\u5355\u5546\u4e1a\u9669\uff081900-2199\uff09", "driver": 3, "maxprice": "2199", "flag": 2, "minprice": "1900", "store": 3}, {"name": "\u5355\u5546\u4e1a\u9669\uff081700-1899\uff09", "driver": 2, "maxprice": "1899", "flag": 2, "minprice": "1700", "store": 3}, {"name": "\u5355\u5546\u4e1a\u9669\uff081400-1699\uff09", "driver": 2, "maxprice": "1699", "flag": 2, "minprice": "1400", "store": 2}, {"name": "\u5355\u5546\u4e1a\u96691300\u4ee5\u4e0a", "driver": 1, "maxprice": "", "flag": 2, "minprice": "1300", "store": 2}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff085100-5399\uff09", "driver": 3, "maxprice": "5399", "flag": 3, "minprice": "5100", "store": 17}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff084900-5099\uff09", "driver": 3, "maxprice": "5099", "flag": 3, "minprice": "4900", "store": 16}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff084600-4899\uff09", "driver": 3, "maxprice": "4899", "flag": 3, "minprice": "4600", "store": 15}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff084300-4599\uff09", "driver": 3, "maxprice": "4599", "flag": 3, "minprice": "4300", "store": 14}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff084100-4299\uff09", "driver": 3, "maxprice": "4299", "flag": 3, "minprice": "4100", "store": 13}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff083800-4099\uff09", "driver": 3, "maxprice": "4099", "flag": 3, "minprice": "3800", "store": 12}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff083500-3799\uff09", "driver": 3, "maxprice": "3799", "flag": 3, "minprice": "3500", "store": 11}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff083300-3499\uff09", "driver": 3, "maxprice": "3499", "flag": 3, "minprice": "3300", "store": 10}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff083000-3299\uff09", "driver": 3, "maxprice": "3299", "flag": 3, "minprice": "3000", "store": 9}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff082700-2999\uff09", "driver": 3, "maxprice": "2999", "flag": 3, "minprice": "2700", "store": 8}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff082500-2699\uff09", "driver": 3, "maxprice": "2699", "flag": 3, "minprice": "2500", "store": 7}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff082200-2499\uff09", "driver": 3, "maxprice": "2499", "flag": 3, "minprice": "2200", "store": 6}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff081900-2199\uff09", "driver": 3, "maxprice": "2199", "flag": 3, "minprice": "1900", "store": 5}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff081700-1899\uff09", "driver": 3, "maxprice": "1899", "flag": 3, "minprice": "1700", "store": 4}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff081400-1699\uff09", "driver": 3, "maxprice": "1699", "flag": 3, "minprice": "1400", "store": 3}, {"name": "\u4ea4\u5f3a\u9669+\u5546\u4e1a\u9669\uff081200-1399\uff09", "driver": 2, "maxprice": "1399", "flag": 3, "minprice": "1200", "store": 3}, {"name": "\ufeff\u5355\u4ea4\u5f3a\u9669\u4ee5\u4e0a", "driver": 1, "maxprice": "", "flag": 1, "minprice": "", "store": 1}], "gift": "ZIC X5"}]'
            item.save()

def update_store_address():
    New_StoreAddress.delete().where(New_StoreAddress.id >= 369).execute()
    new_store = New_Store.select()
    for store in new_store:
        if store.addresses.count() == 0:
            try:
                province = New_Area.get(New_Area.code == store.area_code[:4]).name
            except Exception:
                province = ''

            try:
                city = New_Area.get(New_Area.code == store.area_code[0:8]).name
            except Exception:
                city = ''
            try:
                region = New_Area.get(New_Area.code == store.area_code[0:12]).name
            except Exception:
                region = ''

            New_StoreAddress.create(
                store=store,
                province=province,
                city=city,
                region=region,
                address=store.address,
                name=store.linkman,
                mobile=store.mobile,
                is_default=0,
                created=0,  # 旧的没有，设置默认值：0
                create_by=1
            )
# 删除商品重复的规格参数
def auto_del_repeat_product_attr():
    need_del_PAV = []
    for p in New_Product.select():
        p_attrs = []
        for n in New_ProductAttributeValue.select().where(New_ProductAttributeValue.product == p):
            if n.attribute.id not in p_attrs:
                p_attrs.append(n.attribute.id)
            else:
                need_del_PAV.append(n.id)
    New_ProductAttributeValue.delete().where(New_ProductAttributeValue.id << need_del_PAV).execute()
    print('delete repeat product attribute value: total num=%s, ProductAttributeValue id: %s' %
          (len(need_del_PAV), str(need_del_PAV)))

def update_insurance_order():
    insurance_orders = New_InsuranceOrder.select()
    for item in insurance_orders:
        try:
            old = Old_InsuranceOrder.get(Old_InsuranceOrder.ordernum == item.ordernum)
        except:
            continue
        if old.lasteditedby:
            try:
                admin = New_AdminUser.get(New_AdminUser.username == old.lasteditedby).id
            except Exception:
                admin = 1
            item.current_order_price.admin_user = admin
            item.current_order_price.save()



def update_product_price():
    for nsp in New_StoreProductPrice.select():
        ops = Old_ProductStandard.select().join(Old_Store, on=(Old_Store.id == Old_ProductStandard.store)).\
            join(Old_Product, on=(Old_Product.id == Old_ProductStandard.product)).\
            where((Old_Store.mobile == nsp.store.mobile) & (Old_Product.name == nsp.product_release.product.name) &
                  (Old_ProductStandard.area_code == nsp.area_code)).order_by(Old_ProductStandard.id.desc())
        if ops.count() > 0:
            # if ops[0].pf_price != nsp.price:
            if ops.count() > 1:
                for op in ops:
                    if op.sale_status == 1 and op.is_sale == 1 and op.pf_price > 10 and op.pf_price != nsp.price:
                        print('count=%s, new_id=%s,o_id=%s, pf_price_%s, new_p=%s' % (ops.count(), nsp.id, op.id, op.pf_price, nsp.price))
                        # nsp.price = op.pf_price
                        # nsp.save()
                        break
        else:
            pass
            # print('---%s----%s--' % (nsp.id, nsp.store.mobile))

    for nsp in New_StoreProductPrice.select():
        ops = Old_ProductStandard.select().join(Old_Store, on=(Old_Store.id == Old_ProductStandard.store)).\
            join(Old_Product, on=(Old_Product.id == Old_ProductStandard.product)).\
            where((Old_Store.mobile == '18738808268') & (Old_Product.name == nsp.product_release.product.name) &
                  (Old_ProductStandard.area_code == nsp.area_code)).order_by(Old_ProductStandard.id.desc())
        if ops.count() > 0:
            # if ops[0].pf_price != nsp.price:
            ''' & (Old_ProductStandard.sale_status==1) &
                  (Old_ProductStandard.is_sale == 1) & (Old_ProductStandard.pf_price > 10)'''
            if ops.count() > 1:
                for op in ops:
                    if op.sale_status == 1 and op.is_sale == 1 and op.pf_price > 10 and op.pf_price != nsp.price:
                        print('count=%s, new_id=%s,o_id=%s, pf_price_%s, new_p=%s' % (ops.count(), nsp.id, op.id, op.pf_price, nsp.price))
                        # nsp.price = op.pf_price
                        # nsp.save()
                        break
        else:
            pass
            # print('---%s----%s--' % (nsp.id, nsp.store.mobile))

def select_price_mor_2000():
    ft = (New_StoreProductPrice.active == 1)
    # ft = (New_Store.mobile == '15139455929')   # '18738808268'
    ft &= (New_Category.id == 1)
    for n in New_StoreProductPrice.select().join(New_ProductRelease, on=(New_ProductRelease.id == New_StoreProductPrice.product_release))\
            .join(New_Store, on=(New_Store.id == New_StoreProductPrice.store))\
            .join(New_Product, on=(New_Product.id == New_ProductRelease.product))\
            .join(New_Category, on=(New_Product.category == New_Category.id)).where(ft):
        #print('--%s---%s---%s----%s---' % (n.id, n.price, n.store.name, n.product_release.product.name))
        ops = Old_ProductStandard.select().join(Old_Product, on=(Old_Product.id == Old_ProductStandard.product)).\
            join(Old_Store, on=(Old_Store.id == Old_ProductStandard.store)).\
            where((Old_ProductStandard.is_pass == 1) & (Old_ProductStandard.is_sale == 1) &
                  (Old_ProductStandard.sale_status == 1) & (Old_Product.name == n.product_release.product.name) &
                (Old_ProductStandard.area_code == n.area_code) & (Old_Store.mobile == n.store.mobile))
        if ops.count() > 0:
            for op in ops:
                print('old_p: id=%s, price=%s' % (op.id, op.pf_price))
                n.price = op.pf_price
                n.active = 1
                n.save()
        else:
            pass
            # print('new_p: id=%s, price=%s' % (n.id, n.price))
            # n.active = 0
            # n.save()
        #print('--------------------------------')

def get_all_old_product_price():
    opss = Old_ProductStandard.select(Old_Store.name, Old_Store.area_code, Old_Store.mobile, Old_Product.name,
                                      Old_ProductStandard.area_code, Old_ProductStandard.pf_price).\
        join(Old_Product, on=(Old_Product.id == Old_ProductStandard.product)).\
        join(Old_Store, on=(Old_Store.id == Old_ProductStandard.store)).\
        join(Old_PinPai, on=(Old_PinPai.id == Old_Product.pinpai)).\
        where((Old_ProductStandard.is_pass == 1) & (Old_ProductStandard.sale_status == 1) & (Old_Product.is_index == 0) &
              (Old_PinPai.id << [1,12,13,14,15,16,37,38,75,76,77])).\
        order_by(Old_Store.id.asc(), Old_ProductStandard.area_code.asc(), Old_Product.name.asc()).tuples()
    fp = open('products.csv', 'w')
    fp.write(u'店铺名,店铺地区,店铺地区code,电话,商品名,发布地区,发布地区code,发布价格\n'.encode('gb18030'))
    for ops in opss:
        store_addr = Old_Area().get_detailed_address(ops[1])
        release_area = Old_Area().get_detailed_address(ops[4])
        string = (u'%s,%s,%s,%s,%s,%s,%s,%s\n' % (ops[0], store_addr, ops[1], ops[2], ops[3], release_area, ops[4], ops[5]))
        print string
        fp.write(string.encode('gb18030'))
    fp.close()

def get_all_new_product_price():
    nspps = New_StoreProductPrice.select(New_Store.name, New_Store.area_code, New_Store.mobile, New_Product.name,
                                             New_StoreProductPrice.area_code, New_StoreProductPrice.price). \
        join(New_Store, on=(New_Store.id == New_StoreProductPrice.store)). \
        join(New_ProductRelease, on=(New_ProductRelease.id == New_StoreProductPrice.product_release)).\
        join(New_Product, on=(New_Product.id == New_ProductRelease.product)).\
        where((New_StoreProductPrice.active == 1) & (New_Product.category == 1)).\
        order_by(New_Store.id.asc(), New_StoreProductPrice.area_code.asc(), New_Product.name.asc()).tuples()
    fp = open('products_new.csv', 'w')
    fp.write(u'店铺名,店铺地区,店铺地区code,电话,商品名,发布地区,发布地区code,发布价格\n'.encode('gb18030'))
    for ops in nspps:
        store_addr = New_Area().get_detailed_address(ops[1])
        release_area = New_Area().get_detailed_address(ops[4])
        string = (u'%s,%s,%s,%s,%s,%s,%s,%s\n' % (ops[0], store_addr, ops[1], ops[2], ops[3], release_area, ops[4], ops[5]))
        print string
        fp.write(string.encode('gb18030'))
    fp.close()


def old_price():
    ft = (Old_ProductStandard.pf_price >= 1000)
    ft &= (Old_ProductStandard.sale_status==1)
    for n in Old_ProductStandard.select().where(ft):
        print('--%s---%s---%s----%s---' % (n.id, n.pf_price, n.store.name, n.product.name))


def get_product_name_attr():
    for np in New_Product.select().where(New_Product.category == 1):
        attr = ''
        p = False
        for item in np.attributes:
            attr += item.attribute_item.name + ','
            if item.attribute_item.name in np.name:
                if item.attribute_item.name == u'合成' and u'全合成' in np.name:
                    p = True
            elif item.attribute_item.name == u'其它':
                pass
            else:
                p = True
        if p:
            print('id=%s, name=%s, attr=%s' % (np.id, np.name, attr))

def get_hanzhong():
    area_code = '00270007' + '%'
    fp = open('store_mobile.txt', 'w')
    mobiles = ''
    for s in New_Store.select().where((New_Store.active == 1) & (New_Store.area_code % area_code)):
        mobiles += s.mobile + ','
    fp.write(mobiles.strip(','))
    fp.close()


def move_Referee():
    import time
    now = int(time.time())
    for r in Referee.select():
        if New_AdminUser.select().where(New_AdminUser.username == r.name).count() <= 0:
            New_AdminUser.create(username=r.name, password='e10adc3949ba59abbe56e057f20f883e', mobile='110', email='',
                                 code=r.number, area_code='', realname=r.name, roles='Y', signuped=now,
                                 lsignined=now, active=1)


if __name__ == '__main__':
    move_Referee()
    # get_all_old_product_price()
    # get_all_new_product_price()


    # move_hotsearch()    # 热搜
    # move_delivery()   # 物流公司
    # move_bankcard()   # 银行卡
    # move_area()   # 地区
    # move_category()   # 分类
    # move_categoryattribute()  # 分类和品牌关系
    # move_categoryattributeitem()
    # move_brand()
    # move_brandcategory()
    # move_adminuser()
    # # move_adminuserlog()
    # move_store()
    # move_storebankaccount()
    # move_storearea()
    # move_user()
    # move_storeaddress()
    # move_scorerecord()
    # move_moneyrecord()
	#
    # move_product()
    # move_productpic()
    # # move_productattributevalue()
    # move_productrelease()
    # move_storeproductprice()
    # move_insurance()
    # # move_insurancearea()
    # # move_insuranceexchange()
    # move_feedback()
    # # move_insuranceporderprice()
    # move_insuranceorder()
    # move_settlement()
    # move_Order()
    # move_orderitem()
    # move_cart()
    # move_insuranceitem()
    # move_insuranceprice()
    # move_block()
    # move_blockitem()
    # move_blockitemarea()
    # move_carbrand()
    # move_carbrandfactor()
    # move_car()
    # move_caritemgroup()
    # move_carsk()
    # move_caritem()
    # move_lubeexchange()
    # init_jingxiaoshang()
    # move_feedback()
    # auto_del_repeat_product_attr()
    # init_store_po()
    # update_store_po()
    # update_store_address()


















