from faker import Faker
#https://pypi.org/project/Faker/

fake = Faker()

def generate_user():
    return {
        "email": fake.unique.email(),
        "telephone": fake.msisdn()[:10],
        "password": fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    }

def generate_shipping_address():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "city": fake.city(),
        "post_code": fake.postcode()
    }