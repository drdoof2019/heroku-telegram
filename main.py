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
yukselis_orani = 1.005
dusus_orani = 0.995
bekleme_suresi = 10
while True:
    i=1
    datas.clear()
    #print("sleeep5")
    time.sleep(bekleme_suresi)
    #print("wokeup5")
    datas = get_data()

    for mem_elem in memory_for_USDT:
        #print("mem_elem",mem_elem)
        for data_elem in datas:
            #print("data_elem",data_elem)
            fiyat_dustu = False
            fiyat_yukseldi = False
            volum_dustu = False
            volum_yukseldi = False
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

                if volum_dustu and fiyat_dustu:
                    caption = f"{data_elem['symbol']}: Signal Type:Sell\nPrice:{data_elem['lastPrice']} PriceChange:%{float(mem_elem[1])/float(data_elem['lastPrice']):.2f}\nVolume:{float(data_elem['volume']):.2f},VolumeChange:%{float(mem_elem[2])/float(data_elem['volume']):.2f}"
                    print(caption)
                    caption = caption.replace(".","\.")
                    telegram_ops.send_text_to_telegram(caption)
                elif volum_yukseldi and fiyat_yukseldi:
                    caption = f"{data_elem['symbol']}: Signal Type:BUY\nPrice:{data_elem['lastPrice']}, PriceChange:%{float(data_elem['lastPrice'])/float(mem_elem[1]):.2f}\nVolume:{float(data_elem['volume']):.2f},VolumeChange:%{float(mem_elem[2])/float(data_elem['volume']):.2f}"
                    print(caption)
                    caption = caption.replace(".","\.")
                    telegram_ops.send_text_to_telegram(caption)
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
