import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title('Конвертер валют')
        self.root.geometry('400x300')

        self.rates = {}
        self.last_update = ''

        self.crete_widgets()
        self.fetch_currency_rates()

    def crete_widgets(self):
        self.update_label = ttk.Label(self.root, text='Курсы не загружены')
        self.update_label.pack(pady=10)

        convert_frame = ttk.Frame(self.root)
        convert_frame.pack(pady=10)

        ttk.Label(convert_frame, text='Сумма:').grid(row=0, column=0, padx=5)
        self.amount_entry = ttk.Entry(convert_frame, width=10)
        self.amount_entry.grid(row=0, column=1, padx=5)
        self.amount_entry.insert(0, '1')


        ttk.Label(convert_frame, text='Из:').grid(row=1, column=0, padx=5)

        self.from_currency = ttk.Combobox(convert_frame, values=[], state='readonly', width=7)
        self.from_currency.grid(row=1, column=1, padx=5)

        ttk.Label(convert_frame, text='В:').grid(row=2, column=0, padx=5)

        self.to_currency = ttk.Combobox(convert_frame, values=[], state='readonly', width=7)
        self.to_currency.grid(row=2, column=1, padx=5)


        self.convert_button = ttk.Button(convert_frame, text='Конвертировать', command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.root, text='', font=('Arial', 12, 'bold'))
        self.result_label.pack(pady=10)

        ttk.Button(self.root, text='Обновить курсы', command=self.fetch_currency_rates).pack(pady=10)

    def fetch_currency_rates(self):
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        self.rates = data['Valute']
        self.last_update = datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')
        self.rates['RUB'] = {
            "ID": "R00000",
            "NumCode": "643",
            "CharCode": "RUB",
            "Nominal": 1,
            "Name": "Российский рубль",
            "Value": 1,
            "Previous": 1
        }

        currencies = sorted(self.rates.keys())
        self.from_currency['values'] = currencies
        self.to_currency['values'] = currencies

        if 'USD' in currencies:
            self.from_currency.set('USD')

        if 'RUB' in currencies:
            self.to_currency.set('RUB')

        self.update_label.config(text=f'Курсы обновлены: {self.last_update}')


    def convert(self):
        amount = float(self.amount_entry.get())
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        if not from_curr or not to_curr:
            messagebox.showwarning('Предупреждение', 'Выберите валюты ждя конвертации')
            return
        from_rate = self.rates[from_curr]['Value'] / self.rates[from_curr]['Nominal']
        to_rate = self.rates[to_curr]['Value'] / self.rates[to_curr]['Nominal']

        result = amount * from_rate / to_rate

        self.result_label.config(
            text=f'{amount:.2f} {from_curr} = {result:.2f} {to_curr}\n'
                 f'1 {from_curr} = {from_rate / to_rate:.4f} {to_curr}\n'
                 f'1 {to_curr} = {to_rate / from_rate:.4f} {from_curr}'
        )













root = tk.Tk()
c = CurrencyConverter(root)

root.mainloop()