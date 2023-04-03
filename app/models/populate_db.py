import json
from random import choice

import requests

first_names_male = [
    'Manuel',
    'Bernardes',
    'Caetano',
    'Gabrielle',
    'Ribeiro',
    'Fernando',
    'Luís',
    'Altamira',
    'Diego',
    'Rodrigues',
    'Rodrigo',
    'José',
    'João',
    'Renan',
    'Marcelo',
    'Alan',
    'Denilson',
    'Guilherme',
    'Fabiano',
    'Fabiano',
]

first_names_female = [
    'Laura',
    'Aparecida',
    'Gabriella',
    'Bruna',
    'Ana',
    'Alice',
    'Fernanda',
    'Catarina',
    'Maria',
    'Sueli',
    'Jucilene',
    'Juliana',
    'Júlia',
    'Carol',
    'Amanda',
]

last_names = [
    'Azevedo',
    'Oliveira',
    'Bernardes',
    'Caetano',
    'Cavalcanti',
    'Ribeiro',
    'Sousa',
    'Castro',
    'Silva',
    'Barros',
    'Regueira',
    'Alves',
    'Altamira',
    'Rodrigues',
    'Goncalves',
    'Melo',
    'Fernandes',
    'Dias',
    'Souza',
    'Ferreira',
]

email_types = ['gmail', 'outlook', 'icloud', 'hotmail']


def first_name():

    if choice([True, False]):
        first_name_list = [choice(first_names_male)]
    else:
        first_name_list = [choice(first_names_female)]

    return first_name_list


def last_name():

    last_name_list = []

    len_last_name = choice([2, 3, 4])
    # len_last_name = 10
    for i in range(len_last_name):

        _last_name = choice(last_names)

        if _last_name not in last_name_list:
            last_name_list.append(_last_name)

    return last_name_list


def username(first_name_list, last_name_list):
    _username = first_name_list[0][0] + last_name_list[0][0] + last_name_list[choice([-1, -2])]
    return _username.lower()


def email(_username):
    email_type = choice(email_types)
    return f'{_username}@{email_type}.com'


def create_new_user():

    _first_name = first_name()
    _last_name = last_name()

    _username = username(_first_name, _last_name)

    _email = email(_username)
    # print(f'E-mail: {email}')

    new_user = {
        'first_name': _first_name[0],
        'last_name': ' '.join(_last_name),
        'username': _username,
        'email': _email,
        'password': 1234
    }
    json_body = json.dumps(new_user)
    requests.post('http://127.0.0.1:8000/api/v1/users', data=json_body)


if __name__ == '__main__':

    number_new_users = 5

    for _ in range(number_new_users):
        create_new_user()



