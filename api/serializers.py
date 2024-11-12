from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'birth_date',
                  'can_be_contacted', 'can_data_be_shared', 'password']
        # write_only permet de ne pas afficher le password dans les reponses
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        The create method is used to customize the creation of a user in the serializer.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance