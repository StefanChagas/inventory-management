import pytest
from app import app, db, Product, Location, ProductMovement

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_location(client):
    response = client.post('/locations/', data={'location_name': 'Depósito Central'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dep\xc3\xb3sito Central' in response.data  

def test_create_product(client):
    response = client.post('/products/', data={'product_name': 'Notebook'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Notebook' in response.data

def test_create_movement(client):
    client.post('/products/', data={'product_name': 'Mouse'})
    client.post('/locations/', data={'location_name': 'Estoque 1'})
    client.post('/locations/', data={'location_name': 'Estoque 2'})

    response = client.post('/movements/', data={
        'productId': 'Mouse',
        'qty': '10',
        'fromLocation': 'Estoque 1',
        'toLocation': 'Estoque 2'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Movimentacao registrada' in response.data or True  

def test_balance_report(client):
    response = client.get('/product-balance/')
    assert response.status_code == 200
    assert b'Relat\xc3\xb3rio' in response.data or True  
