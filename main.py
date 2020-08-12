from pathlib import Path
import re
import IP2Location
import operator
import geoip2.database
import geoip2.database

logs = []
q1Answ = {}
q2Answ = {}
q3Answ = [0, 0, 0, 0]
q4Answ = 0

def parser(logfile):
    if not Path(logfile):
        print("Лог-файла не существует")
        return False
    with open(logfile) as line:
        for myline in line:
            pattern = re.compile("shop_api\s*\|\s*([\d-]*)\s*([\d:]*)\s*\[([\dA-Z]*)\]\sINFO:\s([\d.]*)\s*https://all_to_the_bottom.com/([\S]*)")
            match = pattern.match(myline)  # проверяем соответствует ли регулярное выражение строке с позиции i
            tmp = match.groups()
            logs.append(tmp)

def main():
    logfile = input("Введите расположение файла c логами: ")
    if logfile:
        parser(logfile)
    else:
        print("Пустой ввод")
        return False

already_sorted = []
def q1():
    for x in logs:
        if(x[3] in already_sorted): continue
        with geoip2.database.Reader("C:\GeoLite2-Country_20200804\GeoLite2-Country.mmdb") as reader:
            try:
                response = reader.country(x[3]).country.name
            except Exception:
                #response = "-"
                IP2LocObj = IP2Location.IP2Location()
                IP2LocObj.open(
                    "C:\IP2Location-Python-master\data\IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN")
                rec = IP2LocObj.get_all(x[3])

                if(rec.country_long not in q1Answ):
                    q1Answ[rec.country_long] = 1
                else:
                    q1Answ[rec.country_long] = q1Answ[rec.country_long] + 1
            if (response not in q1Answ):
                q1Answ[response] = 1
            else:
                q1Answ[response] = q1Answ[response] + 1
            already_sorted.append(x[3])

def q2():
    for x in logs:
        with geoip2.database.Reader("C:\GeoLite2-Country_20200804\GeoLite2-Country.mmdb") as reader:
            try:
                response = reader.country(x[3]).country.name
            except Exception:
                # response = "-"
                IP2LocObj = IP2Location.IP2Location()
                IP2LocObj.open(
                    "C:\IP2Location-Python-master\data\IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN")
                rec = IP2LocObj.get_all(x[3])
                response = rec.country_long
                if (response not in q2Answ):
                    q2Answ[response] = 1
                else:
                    q2Answ[response] = q2Answ[response] + 1
            if ("fresh_fish" in x[4]):
                if (response not in q2Answ):
                    q2Answ[response] = 1
                else:
                    q2Answ[response] = q2Answ[response] + 1

def q3():
    for x in logs:
        if ("frozen_fish" in x[4]):
            tmp = x[1].split(":")
            h = int(tmp[0])
            m = int(tmp[1])
            if (h >= 0 and (h <= 5)):
                q3Answ[0] = q3Answ[0] + 1
                #print("1: " + str(tmp))
            elif (h >= 6 and (h <= 11)):
                q3Answ[1] = q3Answ[1] + 1
                #print("2: " + str(tmp))
            elif (h >= 12 and (h <= 17)):
                q3Answ[2] = q3Answ[2] + 1
                #print("3: " + str(tmp))
            elif (h >= 18 and (h < 24)):
                q3Answ[3] = q3Answ[3] + 1
                #print("4: " + str(tmp))

def q4():
    global q4Answ
    curD = logs[0][0]
    curH  = 0
    count = 0
    for x in logs:
        #print(str(curD) + " " + str(curH) + " " + str(count))
        tmp = x[1].split(":")
        if(x[0] == curD):
            if(tmp[0] == curH):
                count = count + 1
            else:
                curH = tmp[0]
                if(q4Answ < count): q4Answ = count
                count = 1
        else:
            curD = x[0]
            curH = tmp[0]
            if (q4Answ < count): q4Answ = count
            count = 1

cartsQ5 = {}
productsQ5 = {}
def q5():
    for x in range(len(logs)):
        if ("cart?" in logs[x][4]):
            ip = logs[x][3]
            for y in reversed(range(x)):
                if (ip == logs[y][3]):
                    pattern = re.compile(
                        ".*cart_id=(\d*)")
                    match = pattern.match(logs[x][4])
                    id = match.groups()[0]
                    if (id not in cartsQ5):
                        cartsQ5[id] = {"semi_manufactures": 0, "caviar": 0, "frozen_fish": 0, "fresh_fish": 0, "canned_food": 0}

                    if ("semi_manufactures" in logs[y][4]):
                        cartsQ5[id]["semi_manufactures"] = cartsQ5[id]["semi_manufactures"] + 1
                    if ("caviar" in logs[y][4]):
                        cartsQ5[id]["caviar"] = cartsQ5[id]["caviar"] + 1
                    if ("frozen_fish" in logs[y][4]):
                        cartsQ5[id]["frozen_fish"] = cartsQ5[id]["frozen_fish"] + 1
                    if ("fresh_fish" in logs[y][4]):
                        cartsQ5[id]["fresh_fish"] = cartsQ5[id]["fresh_fish"] + 1
                    if ("canned_food" in logs[y][4]):
                        cartsQ5[id]["canned_food"] = cartsQ5[id]["canned_food"] + 1
                break
    for x in cartsQ5:
        if (int(cartsQ5[x]["semi_manufactures"]) > 0):
            for y in cartsQ5[x]:
                if(y == "semi_manufactures"): continue
                if (y not in productsQ5):
                    productsQ5[y] = cartsQ5[x][y]
                else:
                    productsQ5[y] = productsQ5[y] + cartsQ5[x][y]

cartsQ6 = {}
sucPaysQ6 = 0
def q6():
    global sucPaysQ6
    for x in range(len(logs)):
        if ("cart?" in logs[x][4]):
            pattern = re.compile(
                ".*cart_id=(\d*)")
            match = pattern.match(logs[x][4])
            id = match.groups()[0]
            if (id not in cartsQ6):
                cartsQ6[id] = 1
            else:
                cartsQ6[id] = cartsQ6[id] + 1
    for x in logs:
        if ("success_pay" in x[4]):
            sucPaysQ6 = sucPaysQ6 + 1

ordersQ7 = {}
repeatedOrdersQ7 = {}
def q7():
    for x in logs:
        if("success" in x[4]):
            if (x[3] not in ordersQ7):
                ordersQ7[x[3]] = 1
            else:
                ordersQ7[x[3]] = ordersQ7[x[3]] + 1
                repeatedOrdersQ7[x[3]] = ordersQ7[x[3]]


main()

print("Всего записей: " + str(len(logs)))

print("1) Посетители из какой страны совершают больше всего действий на сайте?")
print("В формате: (country, visitors (different ip's))")
q1()
sorted_x = sorted(q1Answ.items(), key=operator.itemgetter(1))
for i in range(7): print(sorted_x[-i-1])
print()

print("2) Посетители из какой страны чаще всего интересуются товарами из категории “fresh_fish”?")
print("В формате: (country, visitors):")
q2()
sorted_x = sorted(q2Answ.items(), key=operator.itemgetter(1))
for i in range(6): print(sorted_x[-i-1])
print()

print("3) В какое время суток чаще всего просматривают категорию “frozen_fish”?")
q3()
print("[ночь, утро, день, вечер]: " + str(q3Answ))
print("Ответ: " + str(['ночь','утро','день','вечер'][q3Answ.index(max(q3Answ))]))
print()

print("4) Какое максимальное число запросов на сайт за астрономический час (c 00 минут 00 секунд до 59 минут 59 секунд)?")
q4()
print("Ответ: " + str(q4Answ))
print()


print("5) Товары из какой категории чаще всего покупают совместно с товаром из категории “semi_manufactures”?")
q5()
sorted_x = sorted(productsQ5.items(), key=operator.itemgetter(1))
print(sorted_x)
print("Ответ: " + str(sorted_x[-1][0]))
print()

print("6) Сколько брошенных (не оплаченных) корзин имеется??")
q6()
print("Всего корзинок: " + str(len(cartsQ6)))
print("Оплаченных корзинок: " + str(sucPaysQ6))
print("Неоплаченных корзинок: " + str(len(cartsQ6) - sucPaysQ6))
print()

print("7) Какое количество пользователей совершали повторные покупки??")
q7()
sorted_x = sorted(repeatedOrdersQ7.items(), key=operator.itemgetter(1))
#print(sorted_x)
print("Количество пользователей (с различными ip), которые совершали повторные покупки: ")
print(str(len(sorted_x)))
print()



