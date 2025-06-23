import pytest
from main import Order

@pytest.fixture
def order():
    return Order()

def test_check_num(order):
    """
    Проверяет, что check_num возвращает True для списка из 5 элементов и 
    False для меньшего количества.
    """
    assert order.check_num(['1','2','3','4','5'])
    assert not order.check_num(['1','2','3'])

def test_check_ord(order):
    """
    Проверяет, что check_ord возвращает True для списка из более чем одного элемента и 
    False для одного элемента.
    """
    assert order.check_ord(['item1','item2'])
    assert not order.check_ord(['item1'])

def test_check_name(order):
    """
    Проверяет, что check_name возвращает True для имени без цифр и False для имени с цифрами.
    """
    assert order.check_name('Иванов Иван')
    assert not order.check_name('Иванов 123')

def test_check_address(order):
    """
    Проверяет, что check_address возвращает True для валидного адреса и 
    False для пустого, некорректного или неполного адреса.
    """
    assert order.check_address('Россия. Москва. Москва. Арбат', '12345')
    assert not order.check_address('', '12345')
    assert not order.check_address('Россия. Москва. Арбат', '12345')
    assert not order.check_address('Россия. . Москва. Арбат', '12345')

def test_check_phone(order):
    """
    Проверяет, что check_phone возвращает True для валидного номера и 
    False для пустого или некорректного номера.
    """
    assert order.check_phone('+7-123-456-78-90', '12345')
    assert not order.check_phone('', '12345')
    assert not order.check_phone('+7-123-456-7890', '12345')
    assert not order.check_phone('1234567890', '12345')

def test_check_prior(order):
    """
    Проверяет, что check_prior возвращает True для допустимых приоритетов и 
    False для пустого или некорректного значения.
    """
    assert order.check_prior('MAX')
    assert order.check_prior('MIDDLE')
    assert order.check_prior('LOW')
    assert not order.check_prior('')
    assert not order.check_prior('HIGH')

def test_true_format_for_order(order):
    """
    Проверяет, что true_format_for_order корректно группирует одинаковые товары и считает их количество.
    """
    s = 'Яблоко, Яблоко, Груша, Груша, Груша, Банан'
    formatted = order.true_format_for_order(s)
    assert 'Яблоко x2' in formatted
    assert 'Груша x3' in formatted
    assert 'Банан' in formatted

def test_true_address(order):
    """
    Проверяет, что true_address возвращает строку с нужными частями адреса и пробелами после точки.
    """
    addr = 'Россия. Москва. Москва. Арбат'
    assert order.true_address(addr) == 'Москва. Москва. Арбат'

def test_check_country_order(order):
    """
    Проверяет, что check_country_order относит российский заказ к true_orders_russian, 
    а иностранный — к true_orders_other_country.
    """
    order_ru = ['1', 'товар', 'ФИО', 'Россия. Москва. Москва. Арбат', '+7-123-456-78-90', 'MAX']
    order_fr = ['2', 'товар', 'ФИО', 'Франция. Иль-де-Франс. Париж. Шанз-Элизе', '+3-123-456-78-90', 'LOW']
    order.check_country_order(order_ru)
    order.check_country_order(order_fr)
    assert order_ru in order.true_orders_russian
    assert order_fr in order.true_orders_other_country
