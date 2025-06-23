import re
from collections import Counter

class Order:
    def __init__(self):
        
        self.wrong_orders_address = []
        self.wrong_orders_phone = []
        self.true_orders_other_country = []
        self.true_orders_russian = []

    def check_num(self, mas):
        """
        Проверям корректность id заказа
        """
        if len(mas) == 5:
            return True
        else:
            return False

    def check_ord(self, mas):
        """
        Проверяет, что заказ не пуст
        """
        if len(mas) > 1:
            return True
        else:
            return False
        
    def check_name(self, mas):
        """
        Проверяет корректность ФИО
        """
        if len(mas) > 0 and not any(char.isdigit() for char in mas):
            return True
        else:
            return False
        
    def check_address(self, address, id):
        """
        Проверяет корректность адреса и распределяет непрпвильные
        """
        pattern = r'^[^\.]+\. [^\.]+\. [^\.]+\. .+$'
        parts = address.split('. ')
        if not address or address.strip() == '':
            self.wrong_orders_address.append([id, 1, address, 1])
            return False
        elif not re.match(pattern, address):
            self.wrong_orders_address.append([id, 1, address, 2])
            return False
        elif len(parts) != 4 or any(not part.strip() for part in parts):
            self.wrong_orders_address.append([id, 1, address, 2])
            return False
        else:
            return True
        
    def check_phone(self, mas, id):
        """
        Проверят корректность номера и выявляет не правильные
        """
        if not mas or mas.strip() == '':
            self.wrong_orders_phone.append([id, 2, mas])
            return False
        pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
        if not re.fullmatch(pattern, mas):
            self.wrong_orders_phone.append([id, 2, mas])
            return False
        else:
            return True
        
    def write_wrong_ord(self):
        """
        Записывает в файл non_valid_orders.txt сначала неправильные заказы по номеру, потом по адресу
        """
        f = open("non_valid_orders.txt", 'w')
        for el in self.wrong_orders_phone:
            f.write(f"{el[0]}; {el[1]}, {el[2]}\n")
        for el in self.wrong_orders_address:
            if el[3] == 1:
                f.write(f"{el[0]};{el[1]};no data\n")
            else:
                f.write(f"{el[0]};{el[1]}; {el[2]}\n")

    def check_prior(self, mas):
        """
        Проверяет корректность приоритета
        """
        prior = {'MAX', 'MIDDLE', 'LOW'}
        if not mas or mas.strip() == '':
            return False
        if mas not in prior:
            return False
        return True
    
    def check_country_order(self, order):
        """
        Сортирует на Российские заказы и иностранные
        """
        if "Россия" in order[3] or "Российская Федерация" in order[3]:
            self.true_orders_russian.append(order)
        else:
            self.true_orders_other_country.append(order)

    def true_address(self, address):
        """
        Функция для вывода правильного адреса в файл order_country.txt
        """
        t_address = [part.strip() for part in address.split(".")[1:4]]
        return ". ".join(t_address)

    def true_format_for_order(self, ord):
        """
        Функция для вывода правильного набора продуктовв файл order_country
        """
        items = ord.split(", ")
        counts = Counter(items)
        result = []

        for item, count in counts.items():
            if count > 1:
                result.append(f"{item} x{count}")
            else:
                result.append(item)
        return ",".join(result)

    
    def write_sorted_orders(self):
        """
        Сортировка и вывод заказов в файл order_country.txt
        """
        f = open("order_country.txt", 'w')
        priority_map = {'MAX': 3, 'MIDDLE': 2, 'LOW': 1}
        sorted_orders_r = sorted(self.true_orders_russian, key=lambda order: -priority_map[order[5].strip()])
        sorted_orders_o = sorted(self.true_orders_other_country, key=lambda order: -priority_map[order[5].strip()])
        for el in sorted_orders_r:
            f.write(f"{el[0]};{self.true_format_for_order(el[1])};{el[2]};{self.true_address(el[3])};{el[4]};{el[5]}")
        for el in sorted_orders_o:
            f.write(f"{el[0]};{self.true_format_for_order(el[1])};{el[2]};{self.true_address(el[3])};{el[4]};{el[5]}")

    def checking_true_order(self, mas):
        """
        Парсинг одного заказа из файла order.txt с последующими функциями
        """
        check = [True,True,True,True,True,True]
        check[0] = self.check_num(mas[0])
        check[1] = self.check_ord(mas[1])
        check[2] = self.check_name(mas[2])
        check[3] = self.check_address(mas[3], mas[0])
        check[4] = self.check_phone(mas[4], mas[0])
        check[5] = self.check_prior(mas[5])
        print(check)
        if check[3] and check[4]:
            self.check_country_order(mas)
            

    def pars_file(self, namefile):
        """
        Парсинг файла order.txt с последующими функциями, 
        а также вывод значений в файлы order_country.txt и non_valid_order.txt
        """
        f = open(namefile, encoding="utf-8")
        m = []
        for line in f:
            m = line.split(";")
            self.checking_true_order(m)
        self.write_wrong_ord()
        self.write_sorted_orders()



m = Order()
m.pars_file("order.txt")
