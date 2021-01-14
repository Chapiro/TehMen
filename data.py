import datetime
import time
import json
import csv


#Открываем CSV файл
with open('data_task.csv') as data_csv:
    reader = csv.DictReader(data_csv, delimiter='\t')
    rows = list(reader)

#Записываем в JSON для удобства
with open('data.json', 'w') as data_json:
    json.dump(rows, data_json)

#Открывает в режиме чтения JSON
with open("data.json", "r") as data_json:
    data = json.load(data_json)

count = 0
execution_all = 0
data_average_ts_list = []

#Открываем новый CSV. Да, перевёл в JSON, чтобы снова записать в CSV ¯ \ _ (ツ) _ / ¯
with open('data_average_ts6.csv', "w") as data_average_ts_csv:
    writer = csv.writer(data_average_ts_csv, lineterminator='\n')
    for i in data: #Идём по файлу
        closed_ts = int(time.mktime(datetime.datetime.strptime(data[count]['closed_ts'], '%Y-%m-%d %H:%M:%S').timetuple())) #Время окончания выполнения задания в секундах. timestamp выглядит более надежным при операциях с временем.
        assigned_ts = int(time.mktime(datetime.datetime.strptime(data[count]['assigned_ts'], '%Y-%m-%d %H:%M:%S').timetuple())) #Время резервирования задания в секундах.
        execution_ts = (closed_ts - assigned_ts) / float(data[count]['Microtasks']) #Тут считается время в секундах на один микротаск.
        if (execution_ts >= 0): #Смотрим нет ли отрицательного времени. Было только одно, в тестовом задании не страшно, но при реальной работе баг.
            data_average_ts_list = ['{:.2f}'.format(execution_ts)] #Оставляем два знака после запятой
            writer.writerows([data_average_ts_list]) #Записываем время в секундах на один микротаск в CSV для дальнейшего анализа.
        else:
            print(data[count]) #интересно, что попался один случай, когда assigned_ts: 2017-05-24 16:13:06, а closed_ts: 2017-05-24 16:00:57. Отрицательного времени не может быть, поэтому исключаем из статистики.
            print(count)
        count += 1  #Считаем количество выполненных заданий

print(count) #701826 — 1 задание исключили, где было отрицательное время.



