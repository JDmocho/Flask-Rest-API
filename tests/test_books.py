import pytest


def test_get_book_no_records(client):
    response = client.get('/api/v1/books')
    expected_result = {
        "data": [],
        "number_of_records": 0,
        "pagination": {
            "current_page": '/api/v1/books?page=1',
            "total_pages": 0,
            "total_records": 0
        },
        "success": True
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_books(client, sample_data):
    response = client.get('/api/v1/books')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 5
    assert len(response_data['data']) == 5
    assert response_data['pagination'] == {
        'total_pages': 3,
        'total_records': 14,
        'current_page': '/api/v1/books?page=1',
        'next_page': '/api/v1/books?page=2'
    }


def test_get_book_with_params(client, sample_data):
    response = client.get('/api/v1/books?page=1&fields=title&number_of_pages%5Bgte%5D=400&limit=5&sort=id')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 5
    assert len(response_data['data']) == 5
    assert response_data['pagination'] == {
        "current_page": "/api/v1/books?page=1&fields=title&number_of_pages%5Bgte%5D=400&limit=5&sort=id",
        "next_page": "/api/v1/books?page=2&fields=title&number_of_pages%5Bgte%5D=400&limit=5&sort=id",
        "total_pages": 2,
        "total_records": 7
    }

    assert response_data['data'] == [
        {
            "title": "It"
        },
        {
            "title": "Hunger Games"
        },
        {
            "title": "Catching Fire"
        },
        {
            "title": "Mockingjay"
        },
        {
            "title": "Origin"
        }
    ]


def test_get_single_book(client, sample_data):
    response = client.get('/api/v1/books/7')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['isbn'] == 9781407188935
    assert response_data['data']['number_of_pages'] == 448
    assert response_data['data']['title'] == 'Hunger Games'


def test_get_single_book_not_found(client):
    response = client.get('/api/v1/authors/15')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_get_all_author_books(client, sample_data):
    response = client.get('/api/v1/authors/6/books')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 3


def test_create_book(client, token, book, sample_data):
    response = client.post('/api/v1/authors/1/books',
                           json=book,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    expected_result = {
        "data": {
            "author": {
                "first_name": "George",
                "id": 1,
                "last_name": "Orwell"
            },
            **book,
            "id": 15,

        },
        "success": True,
    }

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result

    response = client.get('/api/v1/authors/1/books')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    expected_result2 = {
        "data": [
            {
                "description": "Mr Jones of Manor Farm is so lazy and drunken that one day he forgets to feed his livestock. The ensuing rebellion under the leadership of the pigs Napoleon and Snowball leads to the animals taking over the farm. Vowing to eliminate the terrible inequities of the farmyard, the renamed Animal Farm is organised to benefit all who walk on four legs.",
                "id": 1,
                "isbn": 9780141036137,
                "number_of_pages": 112,
                "title": "Animal Farm"
            },
            {
                "description": "One of the most celebrated classics of the twentieth century, Orwell's cautionary tale of a man trapped under the gaze of an authoritarian state feels more relevant now than ever before.",
                "id": 2,
                "isbn": 9780679417392,
                "number_of_pages": 325,
                "title": "1984"
            },
            {
                "description": "Some description",
                "id": 15,
                "isbn": 4444444444444,
                "number_of_pages": 478,
                "title": "New book"
            }
        ],
        "number_of_records": 3,
        "success": True
    }

    assert response_data == expected_result2


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({"number_of_pages": 478, "isbn": 4444444444444, "description": "Some description"}, "title"),
        ({"title": "New book", "isbn": 4444444444444, "description": "Some description"}, "number_of_pages"),
        ({"title": "New book", "number_of_pages": 478, "description": "Some description"}, "isbn"),
    ]
)
def test_create_book_invalid_data(client, token, data, missing_field, sample_data):
    response = client.post('/api/v1/authors/1/books',
                           json=data,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_create_book_invalid_content_type(client, token, book):
    response = client.post('/api/v1/authors/1/books',
                           data=book,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_book_missing_token(client, book):
    response = client.post('/api/v1/authors/1/books',
                           json=book)
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_book(client, token, update, sample_data):
    response = client.put('/api/v1/books/5',
                           json=update,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    expected_result = {
        "data": {
            "author": {
                "first_name": "Olga",
                "id": 10,
                "last_name": "Tokarczuk"
            },
            "description": "some description",
                "id": 5,
                "isbn": 1234567890123,
                "number_of_pages": 741,
                "title": "some book"
        },
        "success": True
    }

    assert response_data == expected_result


def test_delete_books(client, token,  sample_data):
    response = client.delete('/api/v1/books/10',
                          headers={
                              'Authorization': f'Bearer {token}'
                          })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['data'] == 'Book with id 10 has been deleted'
    assert response_data['success'] is True

    response = client.get('/api/v1/books/10')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['message'] == 'Book with id 10 not found'
    assert response_data['success'] is False
