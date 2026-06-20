from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'college_email', 'campus', 
                  'graduation_year', 'major', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            college_email=validated_data['college_email'],
            campus=validated_data.get('campus', ''),
            graduation_year=validated_data.get('graduation_year'),
            major=validated_data.get('major', ''),
            password=validated_data['password']
        )
        return user