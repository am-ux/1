from yahooquery import Ticker
import pandas
import csv
#biblioteca yahooquery, pandas e csv

def get_tickers_from_csv():#faz uma lista de tickers ajustado ao 
    with open ('/home/am-user/Documents/py/tickers.csv', mode='r') as csv_arquivo: #apenas abre novo arquivo csv no diretorio indicado
        tickers_csv = csv.reader(csv_arquivo, delimiter=',')
        lista_tickers = []
        for row in tickers_csv: #row linha do csv --> apenas uma coluna de ticker
            ajuste = row[0] + ".SA" #ajusta ao formato yahooquery
            lista_tickers.append(ajuste)
        return lista_tickers

def get_ma(cotacoes):#calcula medias moveis para cada ticker da lista e retorna lista de medias moveis
    mov_avg = []
    ma20 = cotacoes.tail(20).mean()#calcula media movel de 20
    ma50 = cotacoes.tail(50).mean()#calcula media movel de 50
    ma100 = cotacoes.tail(100).mean()#calcula media movel de 100
    ma200 = cotacoes.tail(200).mean()#calcula media movel de 200
    ma400 = cotacoes.tail(400).mean()#calcula media movel de 400
    mov_avg.append(ma20)
    mov_avg.append(ma50)
    mov_avg.append(ma100)                  
    mov_avg.append(ma200)
    mov_avg.append(ma400)
    return mov_avg #retorna lista medias_moveis

"""
def fusao_tres_candles(ticker): #junta os ultimos tres candles
    ativo = Ticker(ticker) #chama funcao Ticker do yahooquery entrada eh o ticker
    hist = ativo.history('5d','1d')#retorna dataframe pandas com o historico de cotacoes do ticker ultimos 5 dias   
    hist_low_5d = hist["low"]#lista com o minimo dos ultimos 5 pregoes
    minimo = hist_low_5d.tail(3).min() #minimo dos minimos dos tres dia
    fechamento = hist["close"].tail(1).max()#fechamento do ultimo pregao
    fusao = [minimo, fechamento] #tres ultimos candles transofrmados em 1
    return fusao

def cruza_mm(candle,medias_moveis):#função que define quais media moveis o tres ultimos candles juntados em um cruzou
    minimo = min(candle)
    maximo = max(candle)
    cruza=[]
    for i in range(len(medias_moveis)):
        if (medias_moveis[i]>=minimo) and (medias_moveis[i]<maximo):
            cruza.append(1)
        else:
            cruza.append(0)
    return cruza #lista de quais medias cruzou boolean primeiro item mm10, segund item mm20, etc...

"""

def downup_limit(candle,medias_moveis): #retorna em uma lista a media movel imediatamente suprior e inferior ao fechamento
    fechamento = max(candle)
    valores_superiores = []
    valores_inferiores =[]
    superior = 0
    inferior = 0
    for i in range(len(medias_moveis)):
        if (medias_moveis[i]>fechamento):
            valores_superiores.append(medias_moveis[i])
        else:
            valores_inferiores.append(medias_moveis[i])           
    superior = min(valores_superiores, default = 2*fechamento)
    inferior = max(valores_inferiores, default = 0)
    valores_imediatos = [inferior,superior]
    return valores_imediatos

def compile_ma(collect,new_data):
    for i in range(len(new_data)):
        collect.append(new_data[i])
    return collect
    
#codigo main():

#import pandas as pd  
#ajuda = []
#resultado = pd.DataFrame(columns = ["Ativo","MM10","MM20","MM50","MM100","MM200","MM400","Limite Inferior","Limite Superior","Ultimo"])
#lista_tickers = get_tickers_from_csv()
#for i in range(len(lista_tickers)): #percorre todos os tickers da lista
#ticker=lista_tickers[i]
#def get_upside():

asset = Ticker("ES=F") #chama funcao Ticker do yahooquery entrada eh o ticker

hist_weekly = asset.history('max','1wk')#retorna dataframe pandas com o historico de cotacoes do ticker
close_weekly = hist_weekly["close"]
hist_daily = asset.history('max','1d')#retorna dataframe pandas com o historico de cotacoes do ticker
close_daily = hist_daily["close"] #pega historica de cotacao de fechamento do ticker e poe em outro dataframe
hist_hourly = asset.history('3mo','1h')#retorna dataframe pandas com o historico de cotacoes do ticker
close_hourly = hist_hourly["close"]
hist_15min = asset.history('1mo','15m')#retorna dataframe pandas com o historico de cotacoes do ticker
close_15min = hist_15min["close"] #pega historica de cotacao de fechamento do ticker e poe em outro dataframe
hist_1min = asset.history('1d','1m')#retorna dataframe pandas com o historico de cotacoes do ticker
close_1min = hist_15min["close"] #pega historica de cotacao de fechamento do ticker e poe em outro dataframe

aux_collect = []
collect_ma = []
aux_collect = get_ma(close_weekly)
collect_ma = compile_ma(collect_ma,aux_collect)
aux_collect = get_ma(close_daily)
collect_ma = compile_ma(collect_ma,aux_collect)
aux_collect = get_ma(close_hourly)
collect_ma = compile_ma(collect_ma,aux_collect)
aux_collect = get_ma(close_15min)
collect_ma = compile_ma(collect_ma,aux_collect)
last_quote = close_1min.tail(1)
trading_range = downup_limit(last_quote,collect_ma) 
upside= ((trading_range[1]-last_quote[0]))/last_quote[0]
downside = ((trading_range[0]-last_quote[0]))/last_quote[0]

"""
lista_mm = get_mm_from(fechamento) #chama funcao que lista medias moveis
    tres_candles = fusao_tres_candles(ticker) #funcao que funde os ultimos tres cndles em um
    cruzamento = cruza_mm(tres_candles,lista_mm) #verifica quais medias moveis cruza
    limites = limites_mm(tres_candles,lista_mm) #media movel imediatamente inferiro e superior ao fechamento
    ultimo = max(hist["close"].tail(1))
    ajuda =[ticker,cruzamento[0],cruzamento[1],cruzamento[2],cruzamento[3],cruzamento[4],cruzamento[5],limites[0],limites[1],ultimo]
    resultado.loc[i]=ajuda
resultado.to_csv('/home/am-user/Documents/py/analise_ativos.csv')
"""

