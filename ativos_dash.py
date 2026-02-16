from time import sleep
import schedule
from dash import dash
from ativos import sub_categorias_e_roteadores



schedule.every(1).seconds.do(dash)
schedule.every(1).seconds.do(sub_categorias_e_roteadores)


while True:
    sleep(1)
    schedule.run_pending()





