import pytest
from app.internal.models.user import User
from app.internal.models.checking_account import CheckingAccount
from app.internal.models.card import Card
import decimal


@pytest.fixture(scope="function")
def create_first_user(name="test_name1", phone_number="+71231231230"):
    return User.objects.create(id=3, name=name, phone_number=phone_number)


@pytest.fixture(scope="function")
def create_second_user(name="test_name2", phone_number="+71231231231"):
    return User.objects.create(id=4, name=name, phone_number=phone_number)


@pytest.fixture(scope="function")
def create_user_without_phone(name="test_name3"):
    return User.objects.create(id=5, name=name)


@pytest.fixture(scope="function")
def create_first_account(create_first_user, acccount_number="12345123451234512345", balance=decimal.Decimal("100.00").quantize(decimal.Decimal("0.01"))):
    return CheckingAccount.objects.create(id=5, account_number=acccount_number, owner=create_first_user, balance=balance)


@pytest.fixture(scope="function")
def create_second_account(create_second_user, account_number="02345123451234512345", balance=decimal.Decimal("100.00").quantize(decimal.Decimal("0.01"))):
    return CheckingAccount.objects.create(id=6, account_number=account_number, owner=create_second_user, balance=balance)


@pytest.fixture(scope="function")
def create_first_card(create_first_account, card_number="1234512345123451",
                      expiration_date="2024-04-05", cvv_code="123"):
    return Card.objects.create(id=6, card_number=card_number, expiration_date=expiration_date,
                               cvv_code=cvv_code, checking_account=create_first_account)


@pytest.fixture(scope="function")
def create_second_card(create_second_account, card_number="0234512345123451",
                       expiration_date="2024-04-05", cvv_code="123"):
    return Card.objects.create(id=7, card_number=card_number, expiration_date=expiration_date,
                               cvv_code=cvv_code, checking_account=create_second_account)
