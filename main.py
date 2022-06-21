import requests
import json
import time
import telegram_ops
import datetime
from decimal import Decimal
import configparser
import os, sys
import platform
# ZAMAN : https://stackoverflow.com/questions/57267862/delete-an-object-automatically-after-5-minutes

def get_data():
    r = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    datas = json.loads(r.text)
    return datas

def share_me(coinname,first_price,first_volume,last_price,last_volume,type):
    if type == "BUY":
        print("!!!!!!!!!!!!!!!!! BUY IN SHARE ME !!!!!!!!!!!!!!!!!")
        try:
            baglanti = f"[Follow us on twitter](www.twitter.com)"
            yuzde_fiyat = ((Decimal(last_price)*100)/Decimal(first_price))-100
            yuzde_volum = ((Decimal(last_volume)*100)/Decimal(first_volume))-100
            caption = f"{coinname}: Signal Type:BUY\nPrice:{last_price}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{Decimal(last_volume):.2f}, VolumeChange:%{yuzde_volum:.2f}\n{baglanti}"
            print(caption)
            caption = caption.replace(".","\.")
            caption = caption.replace("-","\-")
            telegram_ops.send_text_to_telegram(caption)
        except Exception as e:
            print(e)
            print("error inside BUY in share_me")
            print(coinname)
            print("---------------------")

    elif type == "SELL":
        print("!!!!!!!!!!!!!!!!! SELL IN SHARE ME !!!!!!!!!!!!!!!!!")
        try:
            baglanti = f"[Follow us on twitter](www.twitter.com)"
            yuzde_fiyat = ((Decimal(first_price)*100)/Decimal(last_price))-100
            yuzde_volum = ((Decimal(first_volume)*100)/Decimal(last_volume))-100
            caption = f"{coinname}: Signal Type:SELL\nPrice:{last_price}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{Decimal(last_volume):.2f}, VolumeChange:%{yuzde_volum:.2f}\n{baglanti}"
            print(caption)
            caption = caption.replace(".","\.")
            caption = caption.replace("-","\-")
            telegram_ops.send_text_to_telegram(caption)
        except Exception as e:
            print(e)
            print("error inside SELL in share_me")
            print(coinname)
            print("---------------------")

def remove_values_from_list(the_list, val):
    temp_list = []
    for value in the_list:
        if value[0] != val:
            temp_list.append(value)
    #print("temp_list",temp_list)
    return temp_list

if __name__ == '__main__':
    #shared = False
    re="\033[1;31m"
    gr="\033[1;32m"
    cy="\033[1;36m"
    unwanted_symbols = ['SCBTC','GNOBTC','XVGBTC']
    detected_coins_for_sell_signal = []
    detected_coins_for_buy_signal = []
    datas = get_data()
    memory_for_USDT_BUSD_BTC = []
    for elem in datas:

        if elem['symbol'].endswith('USDT') or elem['symbol'].endswith('BUSD') or elem['symbol'].endswith('BTC'):
            if elem['symbol'] not in unwanted_symbols:
                memory_for_USDT_BUSD_BTC.append([elem['symbol'],elem['lastPrice'],elem['volume']])

            #print(i,")",elem['symbol'],elem['lastPrice'],elem['volume'])
            #i+=1
    print(memory_for_USDT_BUSD_BTC)
    time.sleep(9999)
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    if platform.system() == 'Windows':
        try:
            fiyat_oran = Decimal(cpass['cred']['fiyat_oran'])
            volume_oran = Decimal(cpass['cred']['volume_oran'])
            bekleme_suresi = int(cpass['cred']['bekleme_suresi'])
            silme_suresi = int(cpass['cred']['silme_suresi'])
            tespit_sayisi = int(cpass['cred']['tespit_sayisi'])
        except KeyError:
            os.system('cls')
            print(re+"[!] run python setup.py first !!\n")
            sys.exit(1)
    if platform.system() == 'Linux':
        try:
            fiyat_oran = Decimal(cpass['cred']['fiyat_oran'])
            volume_oran = Decimal(cpass['cred']['volume_oran'])
            bekleme_suresi = int(cpass['cred']['bekleme_suresi'])
            silme_suresi = int(cpass['cred']['silme_suresi'])
            tespit_sayisi = int(cpass['cred']['tespit_sayisi'])
        except KeyError:
            os.system('clear')
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)
    # # KULLANICI GİRDİLERİ
    # fiyat_oran = 0.3
    # volume_oran = 0.3
    # bekleme_suresi = 4 #saniye
    # tespit_sayisi = 3 #3 veya daha fazla kez tespit edilen coini paylaşır

    yukselis_orani_for_fiyat = 1 + (1*fiyat_oran/100)
    yukselis_orani_for_volume = 1 + (1*volume_oran/100)
    dusus_orani_for_fiyat = 1-(1*fiyat_oran/100)
    dusus_orani_for_volume = 1 - (1*volume_oran/100)
    yukselis_orani_for_fiyat = Decimal(yukselis_orani_for_fiyat)
    yukselis_orani_for_volume = Decimal(yukselis_orani_for_volume)
    dusus_orani_for_fiyat = Decimal(dusus_orani_for_fiyat)
    dusus_orani_for_volume = Decimal(dusus_orani_for_volume)
    # print("yukselis_orani_for_fiyat",yukselis_orani_for_fiyat)
    # print("dusus_orani_for_fiyat",dusus_orani_for_fiyat)
    # print("yukselis_orani_for_volume",yukselis_orani_for_volume)
    # print("dusus_orani_for_volume",dusus_orani_for_volume)
    # time.sleep(999)
    while True:
        i=1
        datas.clear()
        print(f"Sleeping for {bekleme_suresi} secs")
        time.sleep(bekleme_suresi)
        #print("wokeup5")
        datas = get_data()
        """
        {'symbol': 'BTCUSDT', 'priceChange': '-73.60000000', 'priceChangePercent': '-0.350', 'weightedAvgPrice': '20868.09155184',
        'prevClosePrice': '21035.94000000', 'lastPrice': '20962.35000000', 'lastQty': '0.53609000', 'bidPrice': '20962.34000000',
        'bidQty': '0.68150000', 'askPrice': '20962.35000000', 'askQty': '0.07607000', 'openPrice': '21035.95000000',
        'highPrice': '21510.20000000', 'lowPrice': '20232.00000000', 'volume': '97887.67507000', 'quoteVolume': '2042728965.15763180',
        'openTime': 1655380803215, 'closeTime': 1655467203215, 'firstId': 1410753274, 'lastId': 1412347054, 'count': 1593781}
        """
        # for data in datas: # Calculating 10btc price
        #     if data['symbol'] == 'BTCUSDT':
        #         TEN_BTC_VOL = 10*Decimal(data['lastPrice'])
        #         break
        coin_to_delete = []
        if len(detected_coins_for_buy_signal) != 0:
            for data in detected_coins_for_buy_signal: #0>coinname 1>time 2>price 3>volume
                if data[1] < datetime.datetime.now()-datetime.timedelta(minutes=silme_suresi):
                    detected_coins_for_buy_signal.remove(data) # Tespitinin üzerinden 5 dakika geçenleri siler

            for data in detected_coins_for_buy_signal:
                count = 0
                for searching_data in detected_coins_for_buy_signal:
                    if data[0] == searching_data[0]:
                        count += 1
                if count >= 3: # 3 veya daha fazla kez tespit edilenleri paylaşır
                    for elem in detected_coins_for_buy_signal:
                        if elem[0] == data[0]:
                            first_price = elem[2]
                            first_volume = elem[3]
                            break
                    for elem in reversed(detected_coins_for_buy_signal):
                        if elem[0] == data[0]:
                            last_price = elem[2]
                            last_volume = elem[3]
                            break
                    if data[0] in coin_to_delete: # Aynı coini 3 kere paylaşmasını engeller
                        continue
                    share_me(data[0],first_price,first_volume,last_price,last_volume,"BUY")
                    #shared = True
                    #add shared coin info to list for delete
                    coin_to_delete.append(data[0])
        #delete shared coins
        if len(coin_to_delete) != 0:
            for elem in coin_to_delete:
                detected_coins_for_buy_signal = remove_values_from_list(detected_coins_for_buy_signal,elem)
            coin_to_delete.clear()

        if len(detected_coins_for_sell_signal) != 0:
            for data in detected_coins_for_sell_signal: #0>coinname 1>time
                if data[1] < datetime.datetime.now()-datetime.timedelta(minutes=5):
                    detected_coins_for_sell_signal.remove(data) # Tespitinin üzerinden 5 dakika geçenleri siler

            for data in detected_coins_for_sell_signal:
                count = 0

                for searching_data in detected_coins_for_sell_signal:
                    if data[0] == searching_data[0]:
                        count += 1
                if count >= tespit_sayisi: # 3 veya daha fazla kez tespit edilenleri paylaşır

                    for elem in detected_coins_for_sell_signal:
                        if elem[0] == data[0]:
                            first_price = elem[2]
                            first_volume = elem[3]
                            break
                    for elem in reversed(detected_coins_for_sell_signal):
                        if elem[0] == data[0]:
                            last_price = elem[2]
                            last_volume = elem[3]
                            break
                    if data[0] in coin_to_delete: # Aynı coini 3 kere paylaşmasını engeller
                        continue
                    share_me(data[0],first_price,first_volume,last_price,last_volume,"SELL")
                    #shared = True
                    #add shared coin info to list for delete
                    coin_to_delete.append(data[0])
        #delete shared coins
        if len(coin_to_delete) != 0:
            for elem in coin_to_delete:
                detected_coins_for_sell_signal = remove_values_from_list(detected_coins_for_sell_signal,elem)
            coin_to_delete.clear()

        # Kontrol amaçlı
        # if shared == True:
        #     print('detected_coins_for_buy_signal\n',detected_coins_for_buy_signal)
        #     print('\ndetected_coins_for_sell_signal\n',detected_coins_for_sell_signal)
        #     time.sleep(555555)
        for mem_elem in memory_for_USDT_BUSD_BTC:
            #print("mem_elem",mem_elem)
            for data_elem in datas:
                #print("data_elem",data_elem)
                fiyat_dustu = False
                fiyat_yukseldi = False
                volum_dustu = False
                volum_yukseldi = False
                try:
                    if data_elem['symbol'] in mem_elem:
                        #print(data_elem['symbol'],data_elem['lastPrice'],mem_elem[1])
                        if Decimal(data_elem['lastPrice'])*yukselis_orani_for_fiyat < Decimal(mem_elem[1]): # 1%'den fazla düşmüş
                            fiyat_dustu = True

                        if Decimal(data_elem['lastPrice'])*dusus_orani_for_fiyat > Decimal(mem_elem[1]): # 1%'den fazla yükselmiş
                            fiyat_yukseldi = True

                        if Decimal(data_elem['volume'])*yukselis_orani_for_volume < Decimal(mem_elem[2]): # 1%'den fazla düşmüş
                            volum_dustu = True

                        if Decimal(data_elem['volume'])*dusus_orani_for_volume > Decimal(mem_elem[2]): # 1%'den fazla yükselmiş
                            volum_yukseldi = True

                        # if data_elem['symbol'] == 'BTCUSDT': # Suni sinyal için
                        #     fiyat_dustu = True
                        #     volum_dustu = True

                        if volum_dustu and fiyat_dustu: # SELL
                            detected_coins_for_sell_signal.append([data_elem['symbol'],datetime.datetime.now(),data_elem['lastPrice'],data_elem['volume']])#0>coinname 1>time 2>price 3>volume
                            print("detected_coins_for_sell_signal:")
                            for i in detected_coins_for_sell_signal:
                                print(i)

                        elif volum_yukseldi and fiyat_yukseldi: # BUY
                            detected_coins_for_buy_signal.append([data_elem['symbol'],datetime.datetime.now(),data_elem['lastPrice'],data_elem['volume']])#0>coinname 1>time 2>price 3>volume
                            print("detected_coins_for_buy_signal:")
                            for i in detected_coins_for_buy_signal:
                                print(i)

                except Exception as e:
                    print(e)
                    print(data_elem['symbol'])
                    # print("mem_elem[1]:",mem_elem[1],"\ndata_elem['lastPrice']:",data_elem['lastPrice'],"\nmem_elem[2]:",mem_elem[2],"\ndata_elem['volume']:",data_elem['volume'])
                    # print(data_elem)
                    print("--------------------------")
                    pass
        memory_for_USDT_BUSD_BTC.clear()
        for elem in datas:
            if elem['symbol'].endswith('USDT') or elem['symbol'].endswith('BUSD') or elem['symbol'].endswith('BTC'):
                if elem['symbol'] not in unwanted_symbols:
                    memory_for_USDT_BUSD_BTC.append([elem['symbol'],elem['lastPrice'],elem['volume']])
