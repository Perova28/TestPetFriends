import os

from api import PetFriends
from settings import valid_password, valid_email
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()

def test_get_api_key_for_valid_user(email: str = valid_email, password: str = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Борис', anymal_type='кот', age='13', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet( auth_key, name, anymal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
def test_successful_delete_self_pet():
    """ Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боб", "Голубой кот", "4", "images/Dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Рон', animal_type='Барбос', age=5):
    """ Проверка возможности обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцев нет")

def test_add_pets_with_valid_data_without_photo(name = 'Кто я', animal_tipe = 'Жираф', age = '25'):
    """ Проверка добавление питомца без фото"""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_tipe, age)
    assert status == 200
    assert result['name'] == name

def test_get_api_key_for_no_valid_email(email = 'New@rambler.ru', password = valid_password):
    """ Проверка, негативное тестирование, ввод неверного e-mail """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_no_valid_password(email=valid_email, password='159753'):
    """ Проверка, негативное тестирование, ввод неверного пароля """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_no_valid_age_str(name = 'Кэмел', animal_type = 'верблюд', age = 'вот это чушь', pet_photo = 'images/Dog1.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с вводом нечисловой переменной в поле возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert age not in result['age']

def test_add_new_pet_with_four_age_number(name = 'Рой', animal_type = 'Барсук', age = '1234', pet_photo = 'images/Dog1.jpg'):
    """ Проверка, негативное тестирование, добавление питомца с четырехзначным числом в поле возраст """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert len(result['age']) < 4, 'Питомец добавлен на сайт с четырехзначным числом в поле возраст!'

def test_add_pet_with_value_in_variable_name(name='', animal_type='кот', age='2', pet_photo='images/Dog1.jpg'):
    """ Проверка, негативное тестирование,  возможности добавления питомца без имени """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'

def test_add_pet_with_a_lot_of_variable_name(animal_type='терьер', age='6', pet_photo='images/Dog1.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с именем состоящим более 5 слов """

    name = 'Просто очееень длинное имя которое никогда не существовало'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    assert status == 200
    assert len(list_name) < 5, 'Питомец добавлен с именем более 5 слов'

def test_add_new_pet_with_no_valid_tipe_int(name = 'Боря', animal_type = '849256', age = '12', pet_photo = 'images/Dog1.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с вводом числа в поле порода"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо породы!'

def test_add_pet_with_a_lot_of_variable_tipe(name ='Афоня', age='41', pet_photo='images/Dog1.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с названием породы состоящим более 5 слов """

    animal_type = 'Такой породы просто не может существовать на этом свете'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['animal_type'].split()
    assert status == 200
    assert len(list_name) < 5, 'Питомец добавлен с названием породы более 5 слов'

