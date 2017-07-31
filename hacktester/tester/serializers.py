from rest_framework import serializers

from .models import TestRun, Language, TestType
from .validators import validate_language, validate_test_type


class TestRunSerializer(serializers.ModelSerializer):
    extra_options = serializers.DictField(required=False)
    language = serializers.CharField()
    test_type = serializers.CharField()
    test = serializers.CharField(required=False)
    solution = serializers.CharField(required=False)

    def validate(self, attrs):
        language_name = self.initial_data.get('language')
        test_type = self.initial_data.get('test_type')
        language = Language.objects.filter(name=language_name).first()
        if language is None:
            raise serializers.ValidationError(
                "Language {} not supported. Please check GET /supported_languages".format(language_name)
            )
        test = TestType.objects.filter(value=test_type).first()
        if test is None:
            raise serializers.ValidationError(
                "Test type {} not supported. Please check GET /supported_test_types".format(test_type)
            )
        return attrs

    class Meta:
        model = TestRun
        fields = ('language', 'test_type', 'created_at', 'status',
                  'extra_options', 'number_of_results', 'test', 'solution')
