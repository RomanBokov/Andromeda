# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import allure
import pytest

from test_cases import TestCases


@allure.title('Тревога. Объект есть в БД. Нет карточки КК в статусе «Открыта»')
@pytest.mark.parametrize('type_number',list(range(1,11)))
def test_with_new(type_number):
    case = TestCases()
    case.case_all(type_number,2)

@pytest.mark.parametrize('type_number_open_card',list(range(1,11)))
def test_double_messeges(type_number_open_card):
    case = TestCases()
    case.case_all(type_number_open_card,1)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
