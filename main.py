from prettytable import PrettyTable
import json



db = {}
db_update = {}
FLAG = ''

def get_valid_input(prompt, type_):
    '''Валідація введення кількості.Працює так щоб користувач вводив тількі цілі числа типу даних int'''
    while True:
        try:
            return type_(input(prompt))
        except ValueError:
            print(f"Wprowadź prawidłową wartość typu! Proszę wpisać numer")



def create():
    '''Створення бази даних'''
    # flag = ''
    while True:
        delivery_name = input('Wpisz nazwę kartonu.......>>> ').lower()
        # delivery_total = int(input('Podaj ilość kartonu........>>> '))
        delivery_total = get_valid_input('Podaj ilość kartonu........>>> ', int)
        if delivery_name in db:
            print(f"Produkt << {delivery_name} >> już istnieje!")
            continue
        db[delivery_name] = dict(
            [("total", delivery_total), 
             ("stock_quantity", delivery_total), 
             ('order', None), ('total_order', 0)
             ])
        with open('json_db_1.json', 'w') as file_json:
            json.dump(db, file_json, indent=4)
            print(f'Produkt {delivery_name} o ilości {delivery_total} został dodany do Bazy Danych!')
        FLAG = input("Naciśnij < Q > lub < q >, aby wyjść. Aby kontynuować Naciśnij < ENTER >.....>>> ").lower()
        if FLAG == 'q':
            break

def read():
    table = PrettyTable()
    table.field_names = ["Dostawa(nazwa kartonu)", "Ilość", "Ilość w magazynie", "Nazwa zamówienia", "Ilość zamówienia", "Saldo w magazynie"]
    with open("json_db.json", 'r') as file_json:
        json_db = json.load(file_json)
        for i in json_db:
            table.add_row([i, json_db[i]['total'],json_db[i]['stock_quantity'], json_db[i]['order'], json_db[i]['total_order'], json_db[i]['stock_quantity'] - 0 ])
    return print(table)


def update():
    '''Оновлення бази даних(доставка)'''
    while True:
        name_deliv =input('Wpisz nazwę kartonu, lub producenta  kartonu / dostawy.......>>> ') #'6kg n'  ввід користувача 
        # total = int(input('Podaj ilość kartonu dostawu......>>> ')) #40  ввід користувача 
        total = get_valid_input('Podaj ilość kartonu dostawu......>>> ', int)
        
        # json_db = None
        with open("json_db.json", 'r+') as file_json:
            json_db = json.load(file_json)

            if name_deliv in json_db:
                up_total, up_stock_quantity = json_db[name_deliv]['total'], json_db[name_deliv]['stock_quantity'] + total
                up_total = total
                json_db[name_deliv]['total'] = up_total
                json_db[name_deliv]['stock_quantity'] = up_stock_quantity
                file_json.seek(0)
                json.dump(json_db, file_json, indent=4)
                # print(up_total, up_stock_quantity)

            else:
                print('Produkt nie znaleziony! Czy chcesz tworzyć?')
                FLAG = input("Naciśnij < Y >, aby tworzyć. Naciśnij < N > aby wyjść.....>>>  ").lower()
                if FLAG == 'y':
                    json_db[name_deliv] = dict([("total",total ), ("stock_quantity", total), ('order', None), ('total_order', 0)])
                    file_json.seek(0)
                    json.dump(json_db, file_json, indent=4)
                    print(f'Produkt << {name_deliv} >> został dodany do magazynu')
                elif FLAG == 'n':
                    break
            return None
            


def order():
    '''створення замовлення'''
    while True:
        search = input('Wpisz nazwę kartonu....>>> ').lower()
        with open("json_db.json", 'r+') as file_json:
            json_db = json.load(file_json)
            if search not in json_db:
                print("Produkt jest niedostępny na magazynie!")
            elif search in json_db and json_db[search]['stock_quantity'] > 0:
                stock_quantity = json_db[search]['stock_quantity']
                total_order_product = json_db[search]['total_order'] # total order product
                print(f'Produkt jest na magazynie w Ilości << {stock_quantity} szt >>')

                order_name = input('Wpisz nazwę zamówienia....>>> ').lower()
                order_total = get_valid_input('Podaj ilość zamawianego kartonu...>>> ', int)
                # json_db[search]['order'] = order_name
                # json_db[search]['total_order'] = order_tolal
                # stock_quantity = json_db[search]['stock_quantity']
                if stock_quantity < order_total: # перевіврка кількості продукта на складі з замовленням
                    print(
                        f"Ilość - << {stock_quantity} szt. >> kartonów jest za mała do zamówienia - << {order_total} szt. >>."
                    )
                    FLAG = input(" Naciśnij < Q > aby wyjść. Aby kontynuować Naciśnij < ENTER >.....>>> ").lower()
                    if FLAG == 'q':
                        break
                elif stock_quantity >= order_total: # якщо кількість на складі > або = замовленю то робимо ордер
                    json_db[search]['order'] = order_name
                    json_db[search]['total_order'] = order_total
                    up_stock_quantity_order = stock_quantity - order_total
                    up_order_total_sum = total_order_product + order_total
                    json_db[search]['stock_quantity'] = up_stock_quantity_order
                    json_db[search]['total_order'] = up_order_total_sum
                    file_json.seek(0)
                    json.dump(json_db, file_json, indent=4)
                    file_json.truncate()
                    print(f'Zamówienie dodane! Ilość na magazynie - << {stock_quantity - order_total} szt.>>')
                    FLAG = input('Czy Chcesz dodać kolejne zamówienie? Naciśnij < Q > lub < q >, aby wyjść. Aby kontynuować Naciśnij < ENTER >....>>> ').lower()
                    if FLAG == 'q':
                        break
            else:
                if json_db[search]['stock_quantity']== 0:
                    print(f'Produkt jest niedostępny na magazynie! Ilość produktu równia się -- << {json_db[search]['stock_quantity']} >>')



        # order = input('Wpisz nazwę zamówienia........ ')
        # order_total = int(input('Podaj ilość zamawianego kartonu......... '))


def delete():
    pass

def list_info():
    pass


# with open("json_db.json", 'r') as file_json:
#     json_db = json.load(file_json)

# for i in json_db:
#     print(json_db[i]['total'])
if __name__ == '__main__':
    create()
    # read()
    # update()
    # order()