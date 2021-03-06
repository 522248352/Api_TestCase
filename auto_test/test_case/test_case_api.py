# coding=utf-8
import sys
import json
import random
import time

# 当你在IDE中启动解释器时，当前的工作目录就是项目目录，能顺利调用同项目中的模块；但是当你通过CMD命令行启动时，
# 当前工作目录为你启动解释器时所在的目录，如果当时的位置不是项目目录，那么项目目录中的模块就不会被找到，
# 因此运行的时候报错:ModuleNotFoundError: No Module named ...（在例子中我的当前目录是.../package2是项目目录底下的一个文件夹，不是项目目录，所以报错）
#
# 解决方法：
# 方法很简单，就是把模块路径提供给解释器：
# （推荐） 把模块路径放到环境变量中作为全局变量（sys.path能扫描到）。
# 在module2.py开头加入sys.path.append('../')：（'../'表示当前目录的父目录，也即这个项目的项目目录）
# 可以直接把项目路径加到path里

sys.path.append("D:\\eclipse-workspace\\Tests\\Api_TestCase")

from auto_test.config import global_parameter
from auto_test.public.data_base_conn import Data_Base_Conn
from auto_test.public.public_request import Public_Request

# 提现账户查询
def test_cash_account_enquiry():
    print("----------------------------提现账户查询--------------------------")
    paths = "/transaction/showWithdrawAccount.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 101


# 商户可用通道查询
def test_businessmen_can_use_channel():
    print("----------------------------商户可用通道查询--------------------------")
    paths = "/channel/showMerchantChannelType.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11

    db = Data_Base_Conn()
    sql = "SELECT count(*) from m_channeltype_map where mer_no='276944710478757888'"
    rows = db.play(sql=sql)
    vals = rows[0][0]
    assert vals == r_resu.json()["data"]["count"]


# 添加店铺
def test_create_shop():
    print("----------------------------添加店铺--------------------------")
    paths = "/channel/addChannel.htm"
    # maths = random.choice(range(1,100))

    pam = {"partnerId":global_parameter.PARTNERID,
           "merNo":global_parameter.MERNO_NO_USERID,
           "channelTypeId":104073509965275136,
           "channelName":"7181ebay"+str(int(time.time())),
           "url":"http://www.baiducom",
           "email":"856@qq.com",
           "paypalEmail":"test@qq.com",
           "paypalMerInfo":11,
           "paypalAccountImageId":184836625858199552}

    r_obj = Public_Request()

    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 20002
    mer_no = r_resu.json()["data"]["channelId"]
    # time.time()
    # print(time.localtime(time.time()))
    #
    # print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #
    # print(type(time.time()))
    # print(int(time.time()))

    db = Data_Base_Conn()
    sql = "SELECT * from m_channel_info where channel_id = '276560765987749888'"
    rows = db.play(sql=sql)
    print(len(rows))
    for row in rows:
        print(row)

    assert len(rows) == 1


# 图片上传
def test_picture_puload():
    print("----------------------------------图片上传------------------------------------")
    paths = "/upload/image.htm"
    pam = {"partnerId": global_parameter.PARTNERID}
    files_png = {"image": ("278.png", open("D:\\278.png", "rb"), "image/png", {})}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam, files_image=files_png)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 10021


# 图片上传-超过2M
def test_picture_puload_2m():
    print("----------------------------------图片上传超过2M------------------------------------")
    paths = "/upload/image.htm"
    pam = {"partnerId": global_parameter.PARTNERID}
    files_jpg = {"image": ("34231.jpg", open("D:\\34231.jpg", "rb"), "image/jpg", {})}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam, files_image=files_jpg)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 0
    assert r_resu.json()["code"] == 10020

# ebay订单报送
def test_ebay_order_submission():
    print("-------------------------------Ebay订单报送-----------------------------")
    paths = "/channelOrders/batchSendEbayOrders.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_HAVE_USERID, "channelTypeId": 104073509965275136,
           "channelId": 184836678295388160,
           "orders": ('''[{"ebayOrderId":"TEST1-1102-001","amountPaid":"123.98","amountPaidCurrency":"USD",
           "orderStatus":"Completed","paymentMethods":"PayPal","sellerEmail":"test@stodown.com",
           "shippingAddress":"4699 Old Ironsides Dr Ste 150  Santa Clara CA 95054-1858 United States",
           "shippingService":"USEconomyShippingFromGC","shippingAmount":"2","shippingCurrency":"USD",
           "totalAmount":"23.98","totalCurrency":"USD","subtotalAmount":"21.98","subtotalCurrency":"USD",
           "buyerUserId":"kyo857140","paidTime":"1537511875353","createdTime":"1537511875353",
           "storageTime":"1537511875353","sellerUserId":"xin7355","extendOrderId":"238020936017!250000152520959",
           "channelId":"184836678295388160","orderItems":[{"ebayTransactionId":"1102-001","ebayItemId":"302692199600",
           "itemTitle":"Non-Slip Bath Rug and Bathroom Rug Carpet, 16 x 24 inches","itemSite":"US",
           "buyerEmail":"test@aa.com","buyerFirstName":"wenjun","buyerLastName":"li","transactionPriceCurrency":"USD",
           "transactionPriceAmount":"10.99","ebayPlatform":"eBay","transactionQuantity":"1",
           "orderLineItemId":"302692199600-1498231110101","extendedOrderId":"238020936017!250000152520001",
           "ebayOrderId":"TEST1-1102-001","orderId":"154467748704010912"}]}]''')}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 60000


# 余额查询
def test_yu_e_select():
    print("----------------------------- 余额查询 -----------------------------")
    paths = "/merchant/showBalance.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11


# 余额查询-不传MERNO
def test_yu_e_select_no_merno():

    print("----------------------------- 余额查询-不传MERNO -----------------------------")
    paths = "/merchant/showBalance.htm"
    pam = {"partnerId": global_parameter.PARTNERID}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 0
    assert r_resu.json()["code"] == 10041


# 开户
def test_kyc_open_accounts():

    print("------------------------------------开户---------------------------")
    paths = "/merchant/kyc.htm"
    nums = random.choice("python")
    pam = {"partnerId": global_parameter.PARTNERID,
           "accountType": 1,
           "area": "中国",
           "country": "中国",
           "province": "上海",
           "address": "上海市上海",
           "city": "上海",
           "name": "企业法人",
           "idCard": 588596854788889652,
           "idCardImg1": 241354094869118976,
           "idCardImg2": 241354094869118976,
           "merName": "api开户"+nums,
           "businessNumber": 45821,
           "business": 241354094869118976}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths,parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))

    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 10021

    db = Data_Base_Conn()
    sql_m_merchant = "SELECT * from m_merchant where mer_no='276953392935501824'"
    sql_m_audit = "SELECT * FROM m_audit WHERE MER_NO='276953392935501824'"
    rows_m_merchant = db.play(sql=sql_m_merchant)
    assert len(rows_m_merchant) == 1
    # for row in rows_m_merchant:
    #     print(row)
    rows_m_audit = db.play(sql=sql_m_audit)
    assert len(rows_m_audit) == 1


# 账户查询
def test_zhang_hu_select():

    print("-------------------------账户查询------------------------------")
    paths = "/merchant/show.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))

    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 101


# 账户查询-merNo不填
def test_zhang_hu_select_no_merno():

    print("-------------------------账户查询-merNo不填------------------------------")
    paths = "/merchant/show.htm"
    pam = {"partnerId": global_parameter.PARTNERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(),indent=2, sort_keys=False, ensure_ascii=False))

    assert r_resu.json()["status"] == 0
    assert r_resu.json()["code"] == 10041


# 店铺查询
def test_dian_pu_select():

    print("-------------------------店铺查询------------------------------")
    paths = "/channel/showChannel.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))

    db = Data_Base_Conn()
    sql = "SELECT * from m_channel_info where mer_no='276944710478757888'"

    rows = db.play(sql=sql)
    print(len(rows),r_resu.json()["data"]["count"])
    assert len(rows) == r_resu.json()["data"]["count"]


# 店铺查询-查询固定id的店铺
def test_dian_pu_select_channerid():

    print("-------------------------店铺查询-查询固定id的店铺------------------------------")
    paths = "/channel/showChannel.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID, "channelId": 284182608722690048}
    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 101

    db = Data_Base_Conn()
    sql = "SELECT * from m_channel_info where CHANNEL_ID='284182608722690048'"
    rows = db.play(sql=sql)
    assert len(rows) == r_resu.json()["data"]["count"] == 1


# 付款转账类型查询
def test_zhuan_zhang_type_select():

    print("-------------------------付款转账类型查询------------------------------")
    paths = "/payment/getPaymentTypes.htm"
    pam = {"partnerId": global_parameter.PARTNERID,"merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(),indent=2, sort_keys=False, ensure_ascii=False))

    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11


# 付款转账汇率及手续费率查询-传金额
def test_zhuan_zhang_hui_lv_select():

    print("-------------------------付款转账汇率及手续费率查询-传金额------------------------------")
    paths = "/payment/getPaymentRateOrFee.htm"
    pam = {"partnerId": global_parameter.PARTNERID,
            "merNo": global_parameter.MERNO_NO_USERID,
            "receiveCurrency": "GBP",
            "paymentCurrency": "EUR",
            "paymentAmount": 1000
           }

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11


# 付款转账汇率及手续费率查询-不传金额

def test_zhuan_zhang_hui_lv_no_amount():

    print("-------------------------付款转账汇率及手续费率查询-不传金额------------------------------")
    paths = "/payment/getPaymentRateOrFee.htm"
    pam = {"partnerId": global_parameter.PARTNERID,
           "merNo": global_parameter.MERNO_NO_USERID,
           "receiveCurrency": "GBP",
           "paymentCurrency": "EUR"
           }

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)
    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))

    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11


# 转账申请
def test_zhuan_zhang_apply():

    print("-------------------------转账申请------------------------------")
    paths = "/payment/paymentApply.htm"
    pam = {"partnerId": global_parameter.PARTNERID,
           "merNo": global_parameter.MERNO_NO_USERID,
           "paymentType": 0,
           "country": "GBR",
           "apiInfo": """{"IBAN":"iban","BIC":"bic","Payee bank name":"payyname","Payee":"payee","Recipient Address":"address"}""",
           "receiveCurrency": "GBP",
           "paymentCurrency": "EUR",
           "paymentAmount": 1000,
           "registrationNumber": 2,
           "taxDocumentImageId": 241354094869118976
    }

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))

    transactionid = r_resu.json()["data"]["transactionId"]

    print(transactionid)

    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 101

    db = Data_Base_Conn()
    sql = "SELECT * FROM p_transaction where transaction_center_id =" + transactionid + "ORDER BY id desc"
    rows = db.play(sql=sql)

    assert len(rows) == 1


# 转账查询
def test_zhuan_zhang_select():

    print("-------------------------转账查询------------------------------")
    paths = "/payment/getPaymentRecords.htm"
    pam = {"partnerId": global_parameter.PARTNERID, "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 11

    db = Data_Base_Conn()
    sql = "SELECT * FROM p_transaction WHERE MER_NO =" + global_parameter.MERNO_NO_USERID
    rows = db.play(sql=sql)

    assert len(rows) == r_resu.json()["data"]["count"]

    isSuccess = False
    for row in rows:

        print(row[0])
        if str(row[0]) == str(277297765262983168):
            print(row[0])
            isSuccess = True
            break

    # assert isSuccess == True
    if isSuccess is True:
        assert 1 == 1
    else:
        assert 1 == 2


# 添加提现银行卡
def test_add_ti_xian_bank_card():

    print("-------------------------添加提现银行卡------------------------------")
    paths = "/transaction/addWithdrawAccount.htm"
    pam = {"partnerId": global_parameter.PARTNERID,
           "merNo": global_parameter.MERNO_NO_USERID,
           "withdrawAccountryCountry": "CHN",
           "currencyCode": "CNY",
           "bankAccount": str(int(time.time())),
           "contactPhone": "13055226325",
           "bankName": "中国银行",
           "branchBankName": "开户支行名称",
           "branchAddr": "开户支行地址"}

    r_obj = Public_Request()
    r_resu = r_obj.public_request(pas=paths, parameters=pam)

    print(json.dumps(r_resu.json(), indent=2, ensure_ascii=False, sort_keys=False))
    assert r_resu.json()["status"] == 1
    assert r_resu.json()["code"] == 40001

    db = Data_Base_Conn()
    sql = "SELECT * FROM m_withdraw where wdacc_id=" + r_resu.json()["data"]["wdaccId"]
    rows = db.play(sql=sql)
    print(type(rows))
    print(len(rows))
    assert len(rows) == 1
    print(rows[0][0])
    return r_resu.json()["code"]


# 提现银行账号-删除
def test_ti_xian_zhang_hao_delete():

    print("-------------------------提现银行账号-删除------------------------------")
    paths = "/transaction/deleteWithdrawAccount.htm"

    db = Data_Base_Conn()
    sql = "SELECT * FROM m_withdraw where MER_NO=" + global_parameter.MERNO_NO_USERID + "AND R_STATUS=1"
    rows = db.play(sql=sql)

    if len(rows) == 0:
        print("没有可以删除的提现账号，会导致越界")

    wdaid = rows[0][0]
    print(wdaid)

    pam = {"partnerId": global_parameter.PARTNERID,
           "merNo": global_parameter.MERNO_NO_USERID,
           "wdaccId": wdaid}

    r_obj = Public_Request()

    try:
        r_resu = r_obj.public_request(pas=paths, parameters=pam)
    except IndentationError as e:
        print(e)

    print(json.dumps(r_resu.json(), indent=2, sort_keys=False, ensure_ascii=False))


# 提现银行账号-删除-不传wdaccid
def test_ti_xian_zhang_hao_delete_no_wdaccid():

    print("-------------------------提现银行账号-删除-不传wdaccid------------------------------")
    paths = "/transaction/deleteWithdrawAccount.htm"
    pam = {"partnerId": global_parameter.PARTNERID,
           "merNo": global_parameter.MERNO_NO_USERID}

    r_obj = Public_Request()

    try:
        r_resu = r_obj.public_request(pas=paths, parameters=pam)
    except IndentationError as e:
        print(e)

    print(r_resu.text)
    print(r_resu.text.find("Error report"))
    assert r_resu.text.find("Error report") != -1


if __name__ == '__main__':

    test_dian_pu_select()
    # print(dir(time))
    # print(range.__doc__)
    a = set([1,2,3])
    print(a)
    print(sys.path)

