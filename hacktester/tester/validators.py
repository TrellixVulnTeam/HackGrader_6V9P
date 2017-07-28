from rest_framework import serializers

from .models import Language, TestType


def validate_extra_options_dict(extra_options):
    if type(extra_options) is not dict:
        raise serializers.ValidationError("Extra options must be dict!")


def validate_language(language):
    language = Language.objects.filter(name=language).first()
    if language is None:
        raise serializers.ValidationError(
            "Language {} not supported. Please check GET /supported_languages".format(language)
        )


def validate_test_type(test_type):
    test_type = Language.objects.filter(value=test_type).first()
    if test_type is None:
        raise serializers.ValidationError(
            "Test type {} not supported. Please check GET /supported_test_types".format(test_type)
        )
