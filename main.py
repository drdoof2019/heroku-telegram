import requests
import json
import time
import telegram_ops


def get_data():
    r = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    datas = json.loads(r.text)
    return datas

unwanted_symbols = ['USTUSDT','USDPUSDT']
datas = get_data()
memory_for_USDT = []
for elem in datas:
    if elem['symbol'].endswith('USDT'): #or elem['symbol'].endswith('BUSD'):
        if elem['symbol'] not in unwanted_symbols:
            memory_for_USDT.append([elem['symbol'],elem['lastPrice'],elem['volume']])

        #print(i,")",elem['symbol'],elem['lastPrice'],elem['volume'])
        #i+=1
yukselis_orani = 1.01
dusus_orani = 0.99
bekleme_suresi = 5
while True:
    i=1
    datas.clear()
    #print("sleeep5")
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
    for data in datas:
        if data['symbol'] == 'BTCUSDT':
            TEN_BTC_VOL = 10*float(data['lastPrice'])
            break
    for mem_elem in memory_for_USDT:
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
                    if float(data_elem['lastPrice'])*yukselis_orani < float(mem_elem[1]): # 1%'den fazla düşmüş
                        #caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla DÜŞTÜ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                        #print(caption)
                        #caption = caption.replace(".","\.")
                        #telegram_ops.send_text_to_telegram(caption)
                        fiyat_dustu = True
                    if float(data_elem['lastPrice'])*dusus_orani > float(mem_elem[1]): # 1%'den fazla yükselmiş
                        # caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla YÜKSELDİ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                        # print(caption)
                        # caption = caption.replace(".","\.")
                        # telegram_ops.send_text_to_telegram(caption)
                        fiyat_yukseldi = True

                    if float(data_elem['volume'])*yukselis_orani < float(mem_elem[2]): # 1%'den fazla düşmüş
                        # caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla DÜŞTÜ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
                        # print(caption)
                        # caption = caption.replace(".","\.")
                        # telegram_ops.send_text_to_telegram(caption)
                        volum_dustu = True
                    if float(data_elem['volume'])*dusus_orani > float(mem_elem[2]): # 1%'den fazla yükselmiş
                        # caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla YÜKSELDİ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
                        # print(caption)
                        # caption = caption.replace(".","\.")
                        # telegram_ops.send_text_to_telegram(caption)
                        volum_yukseldi = True

                    if volum_dustu and fiyat_dustu: # SELL
                        baglanti = f"[Follow us on twitter](www.twitter.com)"
                        yuzde_fiyat = ((float(mem_elem[1])*100)/float(data_elem['lastPrice']))-100
                        yuzde_volum = ((float(mem_elem[2])*100)/float(data_elem['volume']))-100
                        if float(data_elem['quoteVolume']) > TEN_BTC_VOL:
                            caption = f"{data_elem['symbol']}: Signal Type:SELL\nPrice:{data_elem['lastPrice']}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{float(data_elem['volume']):.2f}, VolumeChange:%{yuzde_volum:.2f}\n10 BTC Volume : YES\n{baglanti}"
                        else:
                            caption = f"{data_elem['symbol']}: Signal Type:SELL\nPrice:{data_elem['lastPrice']}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{float(data_elem['volume']):.2f}, VolumeChange:%{yuzde_volum:.2f}\n10 BTC Volume : NO\n{baglanti}"
                        print(caption)
                        caption = caption.replace(".","\.")
                        telegram_ops.send_text_to_telegram(caption)
                    elif volum_yukseldi and fiyat_yukseldi: # BUY
                        baglanti = f"[Follow us on twitter](www.twitter.com)"
                        yuzde_fiyat = ((float(data_elem['lastPrice'])*100)/float(mem_elem[1]))-100
                        yuzde_volum = ((float(data_elem['volume'])*100)/float(mem_elem[2]))-100
                        if float(data_elem['quoteVolume']) > TEN_BTC_VOL:
                            caption = f"{data_elem['symbol']}: Signal Type:BUY\nPrice:{data_elem['lastPrice']}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{float(data_elem['volume']):.2f}, VolumeChange:%{yuzde_volum:.2f}\n10 BTC Volume : YES\n{baglanti}"
                        else:
                            caption = f"{data_elem['symbol']}: Signal Type:BUY\nPrice:{data_elem['lastPrice']}, PriceChange:%{yuzde_fiyat:.2f}\nVolume:{float(data_elem['volume']):.2f}, VolumeChange:%{yuzde_volum:.2f}\n10 BTC Volume : NO\n{baglanti}"
                        print(caption)
                        caption = caption.replace(".","\.")
                        telegram_ops.send_text_to_telegram(caption)
            except Exception as e:
                print(e)
                # print(i)
                # i+=1
                # print(data_elem['symbol'],mem_elem[0])
                # print(data_elem['lastPrice'],mem_elem[1])
                # print(data_elem['volume'],mem_elem[2])
                # print("--------------------------------------------")
                break
    memory_for_USDT.clear()
    for elem in datas:
        if elem['symbol'].endswith('USDT'): #or elem['symbol'].endswith('BUSD'):
            if elem['symbol'] not in unwanted_symbols:
                memory_for_USDT.append([elem['symbol'],elem['lastPrice'],elem['volume']])
