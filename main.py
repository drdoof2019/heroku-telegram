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
            if data_elem['symbol'] in mem_elem:
                if float(data_elem['lastPrice'])*1.01 < float(mem_elem[1]): # 1%'den fazla düşmüş
                    caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla DÜŞTÜ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                    print(caption)
                    caption = caption.replace(".","\.")
                    telegram_ops.send_text_to_telegram(caption)
                if float(data_elem['lastPrice'])*0.99 > float(mem_elem[1]): # 1%'den fazla yükselmiş
                    caption = f"{data_elem['symbol']}:{mem_elem[0]} FİYATı son taramaya göre %1'den fazla YÜKSELDİ. Eski Fiyat:{mem_elem[1]}, Yeni Fiyat:{data_elem['lastPrice']}"
                    print(caption)
                    caption = caption.replace(".","\.")
                    telegram_ops.send_text_to_telegram(caption)

                if float(data_elem['volume'])*1.01 < float(mem_elem[2]): # 1%'den fazla düşmüş
                    caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla DÜŞTÜ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
                    print(caption)
                    caption = caption.replace(".","\.")
                    telegram_ops.send_text_to_telegram(caption)
                if float(data_elem['volume'])*0.99 > float(mem_elem[2]): # 1%'den fazla yükselmiş
                    caption = f"{data_elem['symbol']}:{mem_elem[0]} VOLUMü son taramaya göre %1'den fazla YÜKSELDİ. Eski Volume:{float(mem_elem[2]):.2f}, Yeni Volume:{float(data_elem['volume']):.2f}"
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
