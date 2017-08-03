from rest_framework import serializers

from .validators import validate_language, validate_test_type


class TestRunSerializer(serializers.Serializer):
    extra_options = serializers.DictField(required=False)
    language = serializers.CharField(validators=[validate_language])
    test_type = serializers.CharField(validators=[validate_test_type])
    test = serializers.CharField(required=False)
    solution = serializers.CharField(required=False)
