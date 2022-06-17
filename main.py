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

while True:
    i=1
    datas.clear()
    #print("sleeep5")
    time.sleep(5)
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

                if float(data_elem['lastPrice'])*1.01 < float(mem_elem[1]): # 1%'den fazla düşmüş
                    #caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla DÜŞTÜ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                    #print(caption)
                    #caption = caption.replace(".","\.")
                    #telegram_ops.send_text_to_telegram(caption)
                    fiyat_dustu = True
                if float(data_elem['lastPrice'])*0.99 > float(mem_elem[1]): # 1%'den fazla yükselmiş
                    # caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla YÜKSELDİ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                    # print(caption)
                    # caption = caption.replace(".","\.")
                    # telegram_ops.send_text_to_telegram(caption)
                    fiyat_yukseldi = True

                if float(data_elem['volume'])*1.01 < float(mem_elem[2]): # 1%'den fazla düşmüş
                    # caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla DÜŞTÜ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
                    # print(caption)
                    # caption = caption.replace(".","\.")
                    # telegram_ops.send_text_to_telegram(caption)
                    volum_dustu = True
                if float(data_elem['volume'])*0.99 > float(mem_elem[2]): # 1%'den fazla yükselmiş
                    # caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla YÜKSELDİ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
                    # print(caption)
                    # caption = caption.replace(".","\.")
                    # telegram_ops.send_text_to_telegram(caption)
                    volum_yukseldi = True

                if volum_dustu and fiyat_dustu:
                    caption = f"{data_elem['symbol']} Fiyatı ve Volümü %1'den fazla DÜŞTÜ\.Sanırım bu bir Sat sinyali\."
                    telegram_ops.send_text_to_telegram(caption)
                elif volum_yukseldi and fiyat_yukseldi:
                    caption = f"{data_elem['symbol']} Fiyatı ve Volümü %1'den fazla YÜKSELDİ\.Sanırım bu bir Al sinyali\."
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
