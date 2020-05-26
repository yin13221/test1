from . import db
from django.http import JsonResponse, HttpResponse


def login(request):
    data = request.GET.dict()
    data.pop("language")
    print(data)
    sql = "select openid from user"
    openid = db.query_list(sql)
    print(openid)
    openid = [i["openid"] for i in openid]
    print(openid)
    if data.get("openid") not in openid:
        sql = """
            insert into user(openid,nickName,gender,city,province,country,avatarUrl) values 
            (%(openid)s,%(nickName)s,%(gender)s,%(city)s,%(province)s,%(country)s,%(avatarUrl)s)
        """
        db.update(sql, args=data)
    return True


def upload(request):
    # image = "http://tmp/" + str(request.FILES.get("images"))
    data = request.GET.dict()
    # print(data)
    openid = data.pop("user")
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(openid,))
    data["userid"] = userid["id"]
    print(data)
    sql = """
        insert into good(g_name,price,g_type,g_desc,userid) values
            (%(name)s,%(price)s,%(type)s,%(desc)s,%(userid)s)
    """
    db.update(sql, args=data)
    sql = "select id from good where g_name=%(name)s and price=%(price)s and g_type=%(type)s and g_desc=%(desc)s and userid=%(userid)s"
    id = db.query_one(sql, args=data)
    return JsonResponse({"id": id})


def uploadphoto(request):
    photo = request.FILES.get("images")
    _photo = photo.read()
    data = request.POST.dict()["id"]
    sql = "update good set pic=%s where id=%s"
    db.update(sql, args=(_photo, data))


def photo(request, id):
    sql = 'select pic from good where id = %s'
    data = db.query_one(sql, args=(id,))
    photo = data.get("pic")
    response = HttpResponse(photo, content_type='image/jpg')
    return response


def goods(request):
    sql = "select g.id,g.g_name,g.price,g.g_type,g.g_desc,g.userid from good g where id<=31"
    data = db.query_list(sql)
    return JsonResponse({"goods": data})


def find_good(request, id):
    sql = "select g.id,g.g_name,g.price,g.g_type,g.g_desc,g.userid from good g where id=%s"
    good = db.query_one(sql, args=(id,))
    if good is None:
        return JsonResponse({"status": True, "msg": ""})
    return JsonResponse({"good": good})


def good_class(request):
    c = request.GET.dict()["key"]
    sql = "select g.id,g.g_name,g.price,g.g_type,g.g_desc,g.userid from good g where g_type=%s"
    data = db.query_list(sql, args=(c,))
    return JsonResponse({"goods": data})


def setCart(request):
    data = request.GET.dict()
    goodid = data["id"]
    user = data["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select * from cart where goodid=%s and userid=%s"
    ishave = db.query_one(sql, args=(goodid, userid))
    if ishave:
        if ishave["state"] == "dead" or ishave["state"] == "over":
            sql = "update cart set state=%s,num=%s,checked=%s where goodid=%s and userid=%s"
            db.update(sql, args=("alive", 1, "", goodid, userid))
        else:
            num = ishave["num"]
            num += 1
            sql = "update cart set num=%s where goodid=%s and userid=%s"
            db.update(sql, args=(num, goodid, userid))
    else:
        sql = "insert into cart(goodid,userid,checked,state,num) values (%s,%s,%s,%s,%s)"
        db.update(sql, args=(goodid, userid, "", "alive", 1))


def confirm(request):
    data = request.GET.dict()
    if "cart" in data.keys():
        cartid = data.pop("cart")
        cartid = cartid.split(",")
        for i in cartid:
            sql = "update cart set state=%s where id=%s"
            db.update(sql, args=("over", int(i)))
    user = data.pop("user")
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    data["userid"] = userid
    data["state"] = "false"
    sql = "insert into dd(userid,good,addrid,sumprice,state,create_time) values (%(userid)s,%(good)s,%(addrid)s,%(sum)s,%(state)s,now())"
    db.update(sql, args=data)
    sql = "select money from user where id=%s"
    money = db.query_one(sql, args=(data["userid"],))["money"]
    money -= float(data["sum"])
    sql = "update user set money=%s where id=%s"
    db.update(sql, args=(money, data["userid"]))


def getCart(request):
    user = request.GET.dict()["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select c.id c_id,c.checked,c.num,g.id g_id,g.g_name,g.price from cart c left join good g on c.goodid=g.id where c.userid=%s and c.state=%s"
    data = db.query_list(sql, args=(userid, "alive"))
    sum = 0
    for i in data:
        if i["checked"] == "true":
            sum += float(i["num"]) * float(i["price"])
    sum = round(sum, 2)
    return JsonResponse({"data": data, "sum": sum})


def getcheckCart(request):
    user = request.GET.dict()["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select c.id c_id,c.checked,c.num,g.id g_id,g.g_name,g.price from cart c left join good g on c.goodid=g.id where c.userid=%s and c.state=%s and checked=%s"
    data = db.query_list(sql, args=(userid, "alive", "true"))
    sum = 0
    for i in data:
        sum += float(i["num"]) * float(i["price"])
    sum = round(sum, 2)
    return JsonResponse({"data": data, "sum": sum})


def changecheck(request):
    id = request.GET.dict()["id"]
    sql = "select * from cart where id=%s"
    data = db.query_one(sql, args=(id,))
    checked = data["checked"]
    print(data)
    print("checked:", checked)
    if checked == "":
        checked = "true"
    else:
        checked = ""
    print("checked:", checked)
    sql = "update cart set checked=%s where id=%s"
    db.update(sql, args=(checked, id))


def checkall(request):
    data = request.GET.dict()
    key = data["key"]
    if key == "true":
        key = "true"
    else:
        key = ""
    user = data["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "update cart set checked=%s where userid=%s"
    db.update(sql, args=(key, userid))


def changenum(request):
    data = request.GET.dict()
    id = data["id"]
    key = data["key"]
    sql = "select num from cart where id=%s"
    num = db.query_one(sql, args=(id,))["num"]
    print(num)
    if key == "-":
        num -= 1
        if num == 0:
            sql = "update cart set state=%s where id=%s"
            db.update(sql, args=("dead", id))
        else:
            sql = "update cart set num=%s where id=%s"
            db.update(sql, args=(num, id))
    else:
        num += 1
        sql = "update cart set num=%s where id=%s"
        db.update(sql, args=(num, id))


def setAddr(request):
    data = request.GET.dict()
    user = data.pop("user")
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    data["userid"] = userid
    sql = "insert into addr(s_name,tel,dq,addr,userid) values (%(name)s,%(tel)s,%(dq)s,%(addr)s,%(userid)s)"
    db.update(sql, args=data)


def updateAddr(request):
    data = request.GET.dict()
    sql = "update addr set s_name=%(name)s,tel=%(tel)s,dq=%(dq)s,addr=%(addr)s where id=%(id)s"
    db.update(sql, args=data)


def delAddr(request, id):
    sql = "delete from addr where id=%s"
    db.update(sql, args=(id,))


def getAddr(request):
    user = request.GET.dict()["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select * from addr where userid=%s"
    data = db.query_list(sql, args=(userid,))
    print(data)
    return JsonResponse({"addr": data})


def getfirstAddr(request):
    user = request.GET.dict()["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select * from addr where userid=%s"
    data = db.query_list(sql, args=(userid,))[0]
    print(data)
    return JsonResponse({"addr": data})


def Addr(request, id):
    sql = "select * from addr where id=%s"
    data = db.query_one(sql, args=(id,))
    return JsonResponse({"addr": data})


def getdd(request):
    user = request.GET.dict()["user"]
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    sql = "select * from dd where userid=%s"
    data = db.query_list(sql, args=(userid,))
    for i in data:
        good = i.pop("good")
        good = good.split(",")
        goods = []
        for j in good:
            id = j.split("-")[0]
            num = j.split("-")[1]
            sql = "select g.id g_id,g.g_name,g.price from good g where id=%s"
            good = db.query_one(sql, args=(id,))
            good["num"] = num
            goods.append(good)
        i["good"] = goods
    return JsonResponse({"dd": data})


def comment(request):
    data = request.GET.dict()
    user = data.pop("user")
    sql = "select id from user where openid=%s"
    userid = db.query_one(sql, args=(user,))["id"]
    data["userid"] = userid
    sql = "insert into comment(goodid,userid,star,content) values (%(goodid)s,%(userid)s,%(star)s,%(content)s)"
    db.update(sql, args=data)


def getcomm(request, id):
    sql = "select * from comment where goodid=%s"
    data = db.query_list(sql, args=(id,))
    return JsonResponse({"desc": data})


def getmoney(request):
    user = request.GET.dict()["user"]
    sql = "select money from user where openid=%s"
    money = db.query_one(sql, args=(user,))["money"]
    return JsonResponse({"money": money})
