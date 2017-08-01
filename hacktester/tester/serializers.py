from rest_framework import serializers

from .models import TestRun, Language, TestType
from .validators import validate_language, validate_test_type


class TestRunSerializer(serializers.ModelSerializer):
    extra_options = serializers.DictField(required=False)
    language = serializers.CharField(validators=[validate_language])
    test_type = serializers.CharField(validators=[validate_test_type])
    test = serializers.CharField(required=False)
    solution = serializers.CharField(required=False)

    class Meta:
        model = TestRun
        fields = ('language', 'test_type', 'created_at', 'status',
                  'extra_options', 'number_of_results', 'test', 'solution')
