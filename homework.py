import datetime as dt


class Calculator:
    """ 
    Общий класс калькулятора
    """
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """
        Сохраняем записи
        """
        self.records.append(record) 

    def get_today_stats(self):
        """
        Считаем потраченные/съеденые сегодня деньги/калории
        """
        now = dt.datetime.now().date()
        return sum([rec.amount for rec in self.records if rec.date == now])

    def get_week_stats(self):
        """
        Считаем сколько денег/калорий потрачено/получено за последние 7 дней
        """
        sum_week = 0
        now = dt.datetime.now().date()
        week = dt.datetime.now() - dt.timedelta(days=6)
        sum_week = (sum([record.amount for record in self.records 
            if now >= record.date >= week.date()]))
        return sum_week

    def get_today_remained(self):
        """
        Считаем остаток денег/калорий на сегодня
        """
        return self.limit - self.get_today_stats()    

class Record:
    """
    Класс для записи расходов или каллорий
    """
    def __init__(self, amount, comment, date=None):

        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, date_format).date()

class CashCalculator(Calculator):
    """
    Класс для калькулятора денег
    """    
    USD_RATE = 72.54
    EURO_RATE = 88.35
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit) 
    
    def get_today_cash_remained(self, currency):
        """ 
        Считаем сколько ещё денег можно потратить сегодня
        """
        cash_for_today = self.get_today_stats()
        cash_residual = self.get_today_remained()
        
        dict_currency = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
            }

        for value in dict_currency:
            if value == currency:
                valuta, rate = dict_currency.get(value)      

        if cash_for_today == self.limit:
            return 'Денег нет, держись'
        elif cash_for_today < self.limit:
            return f'На сегодня осталось {round(cash_residual/rate, 2)} {valuta}'
        return f'Денег нет, держись: твой долг - {round(abs(cash_residual/rate),2)} {valuta}'

class CaloriesCalculator(Calculator):
    """
    Класс для калькулятора калорий
    """
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """
        Считаем сколько ещё калорий можно/нужно получить сегодня
        """
        calories_residual = self.get_today_remained()

        if calories_residual > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
            f'но с общей калорийностью не более {calories_residual} кКал')
        return 'Хватит есть!' 

def main():
    cash = CashCalculator(300)
    cash.add_record(Record(amount=750, date='17.12.2020', comment='Пицца в Додо'))

    calories = CaloriesCalculator(500)
    calories.add_record(Record(amount=330, date='17.12.2020', comment='Пицца'))

    print(cash.get_today_cash_remained('eur'))
    print(calories.get_calories_remained())
    
if __name__ == "__main__":
    main()