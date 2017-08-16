from rest_framework import serializers

from .models import Language, TestType


def validate_language(language):
    language_name = language
    language = Language.objects.filter(name=language_name).first()
    if language is None:
        raise serializers.ValidationError(
            {"invalid_language": "Language {} not supported. Please check GET /supported_languages"
             .format(language_name)}
        )


def validate_test_type(test_type):
    test = TestType.objects.filter(value=test_type).first()
    if test is None:
        raise serializers.ValidationError(
            {"invalid_test_type": "Test type {} not supported. Please check GET /supported_test_types"
             .format(test_type)}
        )
