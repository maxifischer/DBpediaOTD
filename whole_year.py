import DBPedia_On_This_Day
def start(year):
    last = False
    month_day = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    for i in range(1, 13):
       month = i
       for j in range(1, month_day[i] + 1):
           day = j
           date = year,month,day
           if month == 1 and day == 1:
               last = True
           if last == True:
               DBPedia_On_This_Day.main(date)
