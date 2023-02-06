from django.contrib.auth import get_user_model
import factory.fuzzy

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda n: f"test_username_{n}")
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User
