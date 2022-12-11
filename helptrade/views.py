from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import json
import requests

from bs4 import BeautifulSoup
import re
import ast
import time


def start(request):
    return render(request, 'start.html')


def home(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)
    return render(request, 'home.html', {'json_object': json_object['accs'].items()})


def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)

            json_object = {
              "accs":{"acc1": {
              "key":"key1",
              "name_acc":"monstr1",
              "log_pr":"log1",
              "pass_pr":"pass1",
              "ip_port":"ip_port1",
              "purchase":"1",
              "cent":{"1":{"stat":["100", "200"]}, "2":{"asdbsd":["300", "400"]}, "3":{"":["", ""]}, "4":{"":["", ""]}, "5":{"j":["", ""]}}
              },
              "acc2": {
              "key":"key2",
              "name_acc":"monstr2",
              "log_pr":"log2",
              "pass_pr":"pass2",
              "ip_port":"ip_port2",
              "purchase":"2",
              "cent":{"1":{"stat":["100", "200"]}, "2":{"asdbsd":["300", "400"]}, "3":{"":["", ""]}, "4":{"":["", ""]}, "5":{"":["", ""]}}
              },
              "acc3": {
              "key":"key2",
              "name_acc":"monstr2",
              "log_pr":"log2",
              "pass_pr":"pass2",
              "ip_port":"ip_port2",
              "purchase":"2",
              "cent":{"1":{"stat":["100", "200"]}, "2":{"asdbsd":["300", "400"]}, "3":{"":["", ""]}, "4":{"":["", ""]}, "5":{"":["", ""]}}
              },
              "acc4": {
              "key":"key2",
              "name_acc":"monstr2",
              "log_pr":"log2",
              "pass_pr":"pass2",
              "ip_port":"ip_port2",
              "purchase":"2",
              "cent":{"1":{"stat":["100", "200"]}, "2":{"asdbsd":["300", "400"]}, "3":{"":["", ""]}, "4":{"":["", ""]}, "5":{"":["", ""]}}
              }
              },
              "purchase":{"1": {
              "AK-47 | Frontside Misty (Well-Worn)": "0",
              "AK-47 | The Empress (Well-Worn)": "0",
              "M4A1-S | Mecha Industries (Field-Tested)": "0",
              "M4A4 | Neo-Noir (Field-Tested)": "0",
              "M4A4 | 龍王 (Dragon King) (Field-Tested)": "0",
              "StatTrak™ AK-47 | Uncharted (Minimal Wear)": "0",
              "StatTrak™ AK-47 | Vulcan (Battle-Scarred)": "0",
              "StatTrak™ Desert Eagle | Oxide Blaze (Factory New)": "0",
              "StatTrak™ P250 | Asiimov (Battle-Scarred)": "0",
              "StatTrak™ USP-S | Orion (Minimal Wear)": "0"
              },
              "2": {
              "2AK-47 | Frontside Misty (Well-Worn)": "2",
              "2AK-47 | The Empress (Well-Worn)": "0",
              "2M4A1-S | Mecha Industries (Field-Tested)": "0",
              "2M4A4 | Neo-Noir (Field-Tested)": "0",
              "2M4A4 | 龍王 (Dragon King) (Field-Tested)": "0",
              "2StatTrak™ AK-47 | Uncharted (Minimal Wear)": "0",
              "2StatTrak™ AK-47 | Vulcan (Battle-Scarred)": "0",
              "2StatTrak™ Desert Eagle | Oxide Blaze (Factory New)": "0",
              "2StatTrak™ P250 | Asiimov (Battle-Scarred)": "0",
              "2StatTrak™ USP-S | Orion (Minimal Wear)": "2"
              }},
              "setting_telegram": {
              "work_or_stop":"0",
              "nickname":"Denchik",
              "key_sms":"abra-cadabra",
              "phone":"380...",
              "key_tel":"abra-cadabra",
              "chat_id":"123"
              }
            }
            with open(f'{username}.json', 'w') as f:
                json.dump(json_object, f, default=str)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('start')
            else:
                return redirect('/signup')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('start')


def main(request):
    return render(request, 'main.html')


def one_ac(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        # acc = 'acc1'
        acc = request.GET['num_acc']
        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)
        key = json_object['accs'][acc]

        return render(request, 'one_ac.html', {'key': key['key'],
                                               'name_acc': key['name_acc'],
                                               'log_pr': key['log_pr'],
                                               'pass_pr': key['pass_pr'],
                                               'ip_port': key['ip_port'],
                                               'purchase': key['purchase'],
                                               'num_acc': acc})


def purchase(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        acc = request.GET['acc']
        purchase_num = request.GET['purchase']
        purchase = purchase_num
        key_acc = request.GET['key']
        name_acc = request.GET['name_acc']
        log_pr = request.GET['log_pr']
        pass_pr = request.GET['pass_pr']
        ip_port = request.GET['ip_port']

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        key = list(json_object['purchase'][purchase].keys())
        value = list(json_object['purchase'][purchase].values())

        cent_keys = list(json_object['accs'][acc]['cent'].keys())

        cent_name_list1 = list(json_object['accs'][acc]['cent'][cent_keys[0]].keys())
        cent_name1 = cent_name_list1[0]
        min_price1 = json_object['accs'][acc]['cent'][cent_keys[0]][cent_name1][0]
        max_price1 = json_object['accs'][acc]['cent'][cent_keys[0]][cent_name1][1]

        cent_name_list2 = list(json_object['accs'][acc]['cent'][cent_keys[1]].keys())
        cent_name2 = cent_name_list2[0]
        min_price2 = json_object['accs'][acc]['cent'][cent_keys[1]][cent_name2][0]
        max_price2 = json_object['accs'][acc]['cent'][cent_keys[1]][cent_name2][1]

        cent_name_list3 = list(json_object['accs'][acc]['cent'][cent_keys[2]].keys())
        cent_name3 = cent_name_list3[0]
        min_price3 = json_object['accs'][acc]['cent'][cent_keys[2]][cent_name3][0]
        max_price3 = json_object['accs'][acc]['cent'][cent_keys[2]][cent_name3][1]

        cent_name_list4 = list(json_object['accs'][acc]['cent'][cent_keys[3]].keys())
        cent_name4 = cent_name_list4[0]
        min_price4 = json_object['accs'][acc]['cent'][cent_keys[3]][cent_name4][0]
        max_price4 = json_object['accs'][acc]['cent'][cent_keys[3]][cent_name4][1]

        cent_name_list5 = list(json_object['accs'][acc]['cent'][cent_keys[4]].keys())
        cent_name5 = cent_name_list5[0]
        min_price5 = json_object['accs'][acc]['cent'][cent_keys[4]][cent_name5][0]
        max_price5 = json_object['accs'][acc]['cent'][cent_keys[4]][cent_name5][1]

        return render(request, 'purchase.html', {'market_hash_name1': key[0], 'price_max1': value[0],
                                                 'market_hash_name2': key[1], 'price_max2': value[1],
                                                 'market_hash_name3': key[2], 'price_max3': value[2],
                                                 'market_hash_name4': key[3], 'price_max4': value[3],
                                                 'market_hash_name5': key[4], 'price_max5': value[4],
                                                 'market_hash_name6': key[5], 'price_max6': value[5],
                                                 'market_hash_name7': key[6], 'price_max7': value[6],
                                                 'market_hash_name8': key[7], 'price_max8': value[7],
                                                 'market_hash_name9': key[8], 'price_max9': value[8],
                                                 'market_hash_name10': key[9], 'price_max10': value[9],

                                                 'cent_name1': cent_name1,
                                                 'min_price1': min_price1,
                                                 'max_price1': max_price1,

                                                 'cent_name2': cent_name2,
                                                 'min_price2': min_price2,
                                                 'max_price2': max_price2,

                                                 'cent_name3': cent_name3,
                                                 'min_price3': min_price3,
                                                 'max_price3': max_price3,

                                                 'cent_name4': cent_name4,
                                                 'min_price4': min_price4,
                                                 'max_price4': max_price4,

                                                 'cent_name5': cent_name5,
                                                 'min_price5': min_price5,
                                                 'max_price5': max_price5,

                                                 'key': key_acc,
                                                 'name_acc': name_acc,
                                                 'log_pr': log_pr,
                                                 'pass_pr': pass_pr,
                                                 'ip_port': ip_port,
                                                 'purchase': purchase,
                                                 'num_acc': acc
                                                 })


def reverse(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        purchase_num = request.GET['purchase']
        purchase = purchase_num
        key_acc = request.GET['key']
        name_acc = request.GET['name_acc']
        log_pr = request.GET['log_pr']
        pass_pr = request.GET['pass_pr']
        ip_port = request.GET['ip_port']
        acc = request.GET['acc']

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)
        # account_details = json_object[acc]
        key = list(json_object['purchase'][purchase].keys())

        json_object['accs'][acc]['key'] = key_acc
        json_object['accs'][acc]['name_acc'] = name_acc
        json_object['accs'][acc]['log_pr'] = log_pr
        json_object['accs'][acc]['pass_pr'] = pass_pr
        json_object['accs'][acc]['ip_port'] = ip_port
        json_object['accs'][acc]['purchase'] = purchase_num

        cent_name1 = request.GET['cent_name1']
        x = list(json_object['accs'][acc]['cent']['1'].keys())[0]
        json_object['accs'][acc]['cent']['1'][cent_name1] = json_object['accs'][acc]['cent']['1'].pop(x)
        x = list(json_object['accs'][acc]['cent']['1'].keys())[0]
        min_price1 = request.GET['min_price1']
        json_object['accs'][acc]['cent']['1'][x][0] = min_price1
        max_price1 = request.GET['max_price1']
        json_object['accs'][acc]['cent']['1'][x][1] = max_price1

        cent_name2 = request.GET['cent_name2']
        x = list(json_object['accs'][acc]['cent']['2'].keys())[0]
        json_object['accs'][acc]['cent']['2'][cent_name2] = json_object['accs'][acc]['cent']['2'].pop(x)
        x = list(json_object['accs'][acc]['cent']['2'].keys())[0]
        min_price2 = request.GET['min_price2']
        json_object['accs'][acc]['cent']['2'][x][0] = min_price2
        max_price2 = request.GET['max_price2']
        json_object['accs'][acc]['cent']['2'][x][1] = max_price2

        cent_name3 = request.GET['cent_name3']
        x = list(json_object['accs'][acc]['cent']['3'].keys())[0]
        json_object['accs'][acc]['cent']['3'][cent_name3] = json_object['accs'][acc]['cent']['3'].pop(x)
        x = list(json_object['accs'][acc]['cent']['3'].keys())[0]
        min_price3 = request.GET['min_price3']
        json_object['accs'][acc]['cent']['3'][x][0] = min_price3
        max_price3 = request.GET['max_price3']
        json_object['accs'][acc]['cent']['3'][x][1] = max_price3

        cent_name4 = request.GET['cent_name4']
        x = list(json_object['accs'][acc]['cent']['4'].keys())[0]
        json_object['accs'][acc]['cent']['4'][cent_name4] = json_object['accs'][acc]['cent']['4'].pop(x)
        x = list(json_object['accs'][acc]['cent']['4'].keys())[0]
        min_price4 = request.GET['min_price4']
        json_object['accs'][acc]['cent']['4'][x][0] = min_price4
        max_price4 = request.GET['max_price4']
        json_object['accs'][acc]['cent']['4'][x][1] = max_price4

        cent_name5 = request.GET['cent_name5']
        x = list(json_object['accs'][acc]['cent']['5'].keys())[0]
        json_object['accs'][acc]['cent']['5'][cent_name5] = json_object['accs'][acc]['cent']['5'].pop(x)
        x = list(json_object['accs'][acc]['cent']['5'].keys())[0]
        min_price5 = request.GET['min_price5']
        json_object['accs'][acc]['cent']['5'][x][0] = min_price5
        max_price5 = request.GET['max_price5']
        json_object['accs'][acc]['cent']['5'][x][1] = max_price5

        user_price1 = request.GET['price1']
        json_object['purchase'][purchase][key[0]] = user_price1

        user_price2 = request.GET['price2']
        json_object['purchase'][purchase][key[1]] = user_price2

        user_price3 = request.GET['price3']
        json_object['purchase'][purchase][key[2]] = user_price3

        user_price4 = request.GET['price4']
        json_object['purchase'][purchase][key[3]] = user_price4

        user_price5 = request.GET['price5']
        json_object['purchase'][purchase][key[4]] = user_price5

        user_price6 = request.GET['price6']
        json_object['purchase'][purchase][key[5]] = user_price6

        user_price7 = request.GET['price7']
        json_object['purchase'][purchase][key[6]] = user_price7

        user_price8 = request.GET['price8']
        json_object['purchase'][purchase][key[7]] = user_price8

        user_price9 = request.GET['price9']
        json_object['purchase'][purchase][key[8]] = user_price9

        user_price10 = request.GET['price10']
        json_object['purchase'][purchase][key[9]] = user_price10

        with open(f'{username}.json', 'w') as f:
            json.dump(json_object, f, default=str)
        return render(request, 'reverse.html', {'name1': key[0], 'max_price1': user_price1,
                                                'name2': key[1], 'max_price2': user_price2,
                                                'name3': key[2], 'max_price3': user_price3,
                                                'name4': key[3], 'max_price4': user_price4,
                                                'name5': key[4], 'max_price5': user_price5,
                                                'name6': key[5], 'max_price6': user_price6,
                                                'name7': key[6], 'max_price7': user_price7,
                                                'name8': key[7], 'max_price8': user_price8,
                                                'name9': key[8], 'max_price9': user_price9,
                                                'name10': key[9], 'max_price10': user_price10,
                                                })


def change(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)
    return render(request, 'change.html', {'json_object': json_object})


def changed(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        message = eval(request.POST['message'])

        with open(f'{username}.json', 'w') as f:
            json.dump(message, f, default=str)

        return render(request, 'changed.html')


def transaction(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
    return render(request, 'transaction.html')


def transaction_result(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        key1 = request.GET['key1']
        key2 = request.GET['key2']
        money = request.GET['money']
        pay_pass = 'c9i4n0e6o911'
        url = 'https://market.csgo.com/api/v2/money-send/' + money + '/' + key2 + '?pay_pass=' + pay_pass + '&key=' + key1
        url1 = money + '/' + key2 + '?pay_pass=***&key=' + key1
        response = requests.get(url, headers={'Accept': 'application/json'}, params={})
        data = response.json()
    return render(request, 'transaction_result.html', {'data': data, 'url': url1})


def sms_settings(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        work_or_stop = json_object['setting_telegram']['work_or_stop']
        nickname = json_object['setting_telegram']['nickname']
        key_sms = json_object['setting_telegram']['key_sms']
        phone = json_object['setting_telegram']['phone']
        key_tel = json_object['setting_telegram']['key_tel']
        chat_id = json_object['setting_telegram']['chat_id']

    return render(request, 'sms_settings.html', {'work_or_stop': work_or_stop,
                                                 'nickname': nickname,
                                                 'key_sms': key_sms,
                                                 'phone': phone,
                                                 'key_tel': key_tel,
                                                 'chat_id': chat_id,
                                                 })


def sms_set_res(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        work_or_stop = request.GET['work_or_stop']
        nickname = request.GET['nickname']
        key_sms = request.GET['key_sms']
        phone = request.GET['phone']
        key_tel = request.GET['key_tel']
        chat_id = request.GET['chat_id']

        json_object['setting_telegram']['work_or_stop'] = work_or_stop
        json_object['setting_telegram']['nickname'] = nickname
        json_object['setting_telegram']['key_sms'] = key_sms
        json_object['setting_telegram']['phone'] = phone
        json_object['setting_telegram']['key_tel'] = key_tel
        json_object['setting_telegram']['chat_id'] = chat_id

        with open(f'{username}.json', 'w') as f:
            json.dump(json_object, f, default=str)

    return render(request, 'sms_set_res.html', {'work_or_stop': work_or_stop,
                                                'nickname': nickname,
                                                'key_sms': key_sms,
                                                'phone': phone,
                                                'key_tel': key_tel,
                                                'chat_id': chat_id,
                                                })


def set_prices(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
    return render(request, 'set_prices.html')


def set_prices_res1(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        number_purchase = str(request.GET['number_purchase'])
        key_market = str(request.GET['key_market'])
        dollar_rub = float(request.GET['dollar_rub'])

        skin_name = list(json_object['purchase'][number_purchase].keys())
        skin_price = list(json_object['purchase'][number_purchase].values())

        skin_name0 = skin_name[0]

        a = 0
        while True:
            try:
                url = f'https://steamcommunity.com/market/listings/730/{skin_name0}'
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
                responce = requests.get(url, headers=header, timeout=20).text
                soup = BeautifulSoup(responce, 'lxml')
                java_sc = soup.find_all('script', type='text/javascript')
                java_sc_price = java_sc[-1].text
                res_str = java_sc_price.replace(';', '')
                match = re.search(r"var line1=(.+)", res_str)

                # print("\nЦена проданных предметов на стиме (уже проданных!): ")
                if match:
                    old_info = ast.literal_eval(match.group(1))
                    # print(old_info)
                    x = 0
                    price_sell0 = []
                    for i in range(10):
                        x -= 1
                        date = old_info[x][0]
                        price_usd = old_info[x][1]
                        price_rub = price_usd * float(dollar_rub)
                        price_rub = float('{:.3f}'.format(price_rub))

                        price_sell0.append(f'{price_rub} ____RUB________________ {date} $')
            except:
                a += 1
                if a == 2:
                    price_sell0 = ['error steam']
                    break
                time.sleep(2)
                continue
            break

        a = 0
        while True:
            try:
                url = f'https://market.csgo.com/api/v2/search-item-by-hash-name-specific?key={key_market}&hash_name={skin_name0}'
                response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)

                data = response.json()

                length = len(data['data'])

                if length > 7:
                    length = 6

                classit_instance = {}
                for i in range(length):
                    classit = data['data'][i]['class']
                    instance = data['data'][i]['instance']
                    res = f'{classit}_{instance}'
                    # print(res)
                    classit_instance[res] = i

                classit_instance = list(classit_instance.keys())
                price_buy = {}
                sell_buy_market_csgo0 = []
                for cls_ins in classit_instance:

                    try:
                        url = f'https://market.csgo.com/api/v2/prices/class_instance/RUB.json'
                        response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)
                        data = response.json()
                        sell_buy_market_csgo0.append(
                            f"Цена продажи: {data['items'][cls_ins]['price']} руб., Цена ордера: {data['items'][cls_ins]['buy_order']} руб.")
                    except:
                        pass
            except:
                a += 1
                if a == 2:
                    sell_buy_market_csgo0 = ['error market csgo']
                    break
                time.sleep(2)
                continue
            break

        a = 0
        while True:
            try:
                url = f'https://market.csgo.com/api/v2/get-list-items-info?key={key_market}&list_hash_name[]={skin_name0}'
                response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)
                data = response.json()

                length = len(data['data'][skin_name0]['history'])

                if length > 20:
                    length = 20
                sold_mar_csgo0 = []
                for i in range(length):
                    date = data['data'][skin_name0]['history'][i][0]
                    price_sell_m = data['data'][skin_name0]['history'][i][1]
                    sold_mar_csgo0.append(f'Цена: {price_sell_m} руб.      {time.ctime(int(date))}')
            except:
                a += 1
                if a == 2:
                    sold_mar_csgo0 = ['Error sold market csgo']
                    break
                time.sleep(2)
                continue
            break

        skin_name1 = skin_name[1]
        #
        # a = 0
        # while True:
        #     try:
        #         url = f'https://steamcommunity.com/market/listings/730/{skin_name1}'
        #         header = {
        #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
        #         responce = requests.get(url, headers=header, timeout=20).text
        #         soup = BeautifulSoup(responce, 'lxml')
        #         java_sc = soup.find_all('script', type='text/javascript')
        #         java_sc_price = java_sc[-1].text
        #         res_str = java_sc_price.replace(';', '')
        #         match = re.search(r"var line1=(.+)", res_str)
        #
        #         # print("\nЦена проданных предметов на стиме (уже проданных!): ")
        #         if match:
        #             old_info = ast.literal_eval(match.group(1))
        #             # print(old_info)
        #             x = 0
        #             price_sell1 = []
        #             for i in range(10):
        #                 x -= 1
        #                 date = old_info[x][0]
        #                 price_usd = old_info[x][1]
        #                 price_rub = price_usd * float(dollar_rub)
        #                 price_rub = float('{:.3f}'.format(price_rub))
        #
        #                 price_sell1.append(f'{price_rub} ____RUB________________ {date} $')
        #     except:
        #         a += 1
        #         if a == 2:
        #             price_sell1 = ['error steam']
        #             break
        #         time.sleep(2)
        #         continue
        #     break
        #
        # a = 0
        # while True:
        #     try:
        #         url = f'https://market.csgo.com/api/v2/search-item-by-hash-name-specific?key={key_market}&hash_name={skin_name1}'
        #         response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)
        #
        #         data = response.json()
        #
        #         length = len(data['data'])
        #
        #         if length > 7:
        #             length = 6
        #
        #         classit_instance = {}
        #         for i in range(length):
        #             classit = data['data'][i]['class']
        #             instance = data['data'][i]['instance']
        #             res = f'{classit}_{instance}'
        #             # print(res)
        #             classit_instance[res] = i
        #
        #         classit_instance = list(classit_instance.keys())
        #         price_buy = {}
        #         sell_buy_market_csgo1 = []
        #         for cls_ins in classit_instance:
        #
        #             try:
        #                 url = f'https://market.csgo.com/api/v2/prices/class_instance/RUB.json'
        #                 response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)
        #                 data = response.json()
        #                 sell_buy_market_csgo1.append(
        #                     f"Цена продажи: {data['items'][cls_ins]['price']} руб., Цена ордера: {data['items'][cls_ins]['buy_order']} руб.")
        #             except:
        #                 pass
        #     except:
        #         a += 1
        #         if a == 2:
        #             sell_buy_market_csgo1 = ['error market csgo']
        #             break
        #         time.sleep(2)
        #         continue
        #     break
        #
        # a = 0
        # while True:
        #     try:
        #         url = f'https://market.csgo.com/api/v2/get-list-items-info?key={key_market}&list_hash_name[]={skin_name1}'
        #         response = requests.get(url, headers={'Accept': 'application/json'}, timeout=20)
        #         data = response.json()
        #
        #         length = len(data['data'][skin_name1]['history'])
        #
        #         if length > 20:
        #             length = 20
        #         sold_mar_csgo1 = []
        #         for i in range(length):
        #             date = data['data'][skin_name1]['history'][i][0]
        #             price_sell_m = data['data'][skin_name1]['history'][i][1]
        #             sold_mar_csgo1.append(f'Цена: {price_sell_m} руб.      {time.ctime(int(date))}')
        #     except:
        #         a += 1
        #         if a == 2:
        #             sold_mar_csgo1 = ['Error sold market csgo']
        #             break
        #         time.sleep(2)
        #         continue
        #     break
        #
        #
        skin_name2 = skin_name[2]
        skin_name3 = skin_name[3]
        skin_name4 = skin_name[4]
        skin_name5 = skin_name[5]
        skin_name6 = skin_name[6]
        skin_name7 = skin_name[7]
        skin_name8 = skin_name[8]
        skin_name9 = skin_name[9]

        skin_price0 = skin_price[0]
        skin_price1 = skin_price[1]
        skin_price2 = skin_price[2]
        skin_price3 = skin_price[3]
        skin_price4 = skin_price[4]
        skin_price5 = skin_price[5]
        skin_price6 = skin_price[6]
        skin_price7 = skin_price[7]
        skin_price8 = skin_price[8]
        skin_price9 = skin_price[9]

    return render(request, 'set_prices_res1.html', {'skin_name0': skin_name0, 'skin_price0': skin_price0,
                                                    'skin_name1': skin_name1, 'skin_price1': skin_price1,
                                                    'skin_name2': skin_name2, 'skin_price2': skin_price2,
                                                    'skin_name3': skin_name3, 'skin_price3': skin_price3,
                                                    'skin_name4': skin_name4, 'skin_price4': skin_price4,
                                                    'skin_name5': skin_name5, 'skin_price5': skin_price5,
                                                    'skin_name6': skin_name6, 'skin_price6': skin_price6,
                                                    'skin_name7': skin_name7, 'skin_price7': skin_price7,
                                                    'skin_name8': skin_name8, 'skin_price8': skin_price8,
                                                    'skin_name9': skin_name9, 'skin_price9': skin_price9,

                                                    'number_purchase': number_purchase,
                                                    'key_market': key_market,
                                                    'dollar_rub': dollar_rub,

                                                    'price_sell0': price_sell0,
                                                    'sell_buy_market_csgo0': sell_buy_market_csgo0,
                                                    'sold_mar_csgo0': sold_mar_csgo0,

                                                    # 'price_sell1': price_sell1,
                                                    # 'sell_buy_market_csgo1': sell_buy_market_csgo1,
                                                    # 'sold_mar_csgo1': sold_mar_csgo1,
                                                    })


def set_prices_save(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name

        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)

        number_purchase = str(request.GET['number_purchase'])
        purchase = list(json_object['purchase'][number_purchase].keys())

        price0 = request.GET['price0']
        price1 = request.GET['price1']
        price2 = request.GET['price2']
        price3 = request.GET['price3']
        price4 = request.GET['price4']
        price5 = request.GET['price5']
        price6 = request.GET['price6']
        price7 = request.GET['price7']
        price8 = request.GET['price8']
        price9 = request.GET['price9']

        skin_name0 = purchase[0]
        skin_name1 = purchase[1]
        skin_name2 = purchase[2]
        skin_name3 = purchase[3]
        skin_name4 = purchase[4]
        skin_name5 = purchase[5]
        skin_name6 = purchase[6]
        skin_name7 = purchase[7]
        skin_name8 = purchase[8]
        skin_name9 = purchase[9]

        json_object['purchase'][number_purchase][skin_name0] = price0
        json_object['purchase'][number_purchase][skin_name1] = price1
        json_object['purchase'][number_purchase][skin_name2] = price2
        json_object['purchase'][number_purchase][skin_name3] = price3
        json_object['purchase'][number_purchase][skin_name4] = price4
        json_object['purchase'][number_purchase][skin_name5] = price5
        json_object['purchase'][number_purchase][skin_name6] = price6
        json_object['purchase'][number_purchase][skin_name7] = price7
        json_object['purchase'][number_purchase][skin_name8] = price8
        json_object['purchase'][number_purchase][skin_name9] = price9

        with open(f'{username}.json', 'w') as f:
            json.dump(json_object, f, default=str)

    return render(request, 'set_prices_save.html', {'number_purchase': number_purchase})


def json_page(request):
    username = None
    if request.user.is_authenticated and request.user.first_name:
        username = request.user.first_name
        res = open(f'{username}.json', 'r', encoding="utf-8")
        response = res.read()
        json_object = json.loads(response)
    return render(request, 'json_page.html', {'json_object': json_object})
