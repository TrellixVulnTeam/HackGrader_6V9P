from rest_framework import serializers

from .models import Language, TestType


def validate_extra_options_dict(extra_options):
    if type(extra_options) is not dict:
        raise serializers.ValidationError("Extra options must be dict!")
    return extra_options


def validate_language(language):
    print("LANGUAGE IS: ", language)
    lang = Language.objects.filter(name=language).first()
    if lang is None:
        raise serializers.ValidationError(
            "Language {} not supported. Please check GET /supported_languages".format(language)
        )
    return language


def validate_test_type(test_type):
    print("TEST_TYPE IS: ", test_type)
    test = TestType.objects.filter(value=test_type).first()
    if test is None:
        raise serializers.ValidationError(
            "Test type {} not supported. Please check GET /supported_test_types".format(test_type)
        )
    return test_type
