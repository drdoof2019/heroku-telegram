import requests
import json
import time
import telegram_ops
import datetime
from decimal import Decimal
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



if __name__ == '__main__':

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
    yukselis_orani = 1.005
    yukselis_orani = Decimal(yukselis_orani)
    dusus_orani = 0.995
    dusus_orani = Decimal(dusus_orani)
    bekleme_suresi = 4 #saniye
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

        if len(detected_coins_for_buy_signal) != 0:
            for data in detected_coins_for_buy_signal: #0>coinname 1>time 2>price 3>volume
                if data[1] < datetime.datetime.now()-datetime.timedelta(minutes=5):
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

                    share_me(data[0],first_price,first_volume,last_price,last_volume,"BUY")

                    #delete shared coin
                    for elem in detected_coins_for_buy_signal:
                        if elem[0] == data[0]:
                            detected_coins_for_buy_signal.remove(elem)


        if len(detected_coins_for_sell_signal) != 0: # Tespitinin üzerinden 5 dakika geçenleri siler
            for data in detected_coins_for_sell_signal: #0>coinname 1>time
                if data[1] < datetime.datetime.now()-datetime.timedelta(minutes=5):
                    detected_coins_for_sell_signal.remove(data)

            for data in detected_coins_for_sell_signal:
                count = 0
                for searching_data in detected_coins_for_sell_signal:
                    if data[0] == searching_data[0]:
                        count += 1
                if count >= 3: # 3 veya daha fazla kez tespit edilenleri paylaşır
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

                    share_me(data[0],first_price,first_volume,last_price,last_volume,"SELL")

                    #delete shared coin
                    for elem in detected_coins_for_sell_signal:
                        if elem[0] == data[0]:
                            detected_coins_for_sell_signal.remove(elem)



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
                        if Decimal(data_elem['lastPrice'])*yukselis_orani < Decimal(mem_elem[1]): # 1%'den fazla düşmüş
                            fiyat_dustu = True

                        if Decimal(data_elem['lastPrice'])*dusus_orani > Decimal(mem_elem[1]): # 1%'den fazla yükselmiş
                            fiyat_yukseldi = True

                        if Decimal(data_elem['volume'])*yukselis_orani < Decimal(mem_elem[2]): # 1%'den fazla düşmüş
                            volum_dustu = True

                        if Decimal(data_elem['volume'])*dusus_orani > Decimal(mem_elem[2]): # 1%'den fazla yükselmiş
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
