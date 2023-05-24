from django import VERSION
from faker import Faker


def test_django_version_4():
    assert VERSION[0] >= 4


def test_faker_fixture_pressence(faker):
    assert isinstance(faker, Faker)
