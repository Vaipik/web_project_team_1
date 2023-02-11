from django.contrib.auth import get_user_model
import factory.fuzzy

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    username = "test_username_test"  # if new username required call factory as UserFactory(username="new_username")
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User
        django_get_or_create = ('username', )
