from rest_framework import serializers

from .models import Language, TestType


def validate_language(language):
    lang = Language.objects.filter(name=language).first()
    if lang is None:
        raise serializers.ValidationError(
            "Language {} not supported. Please check GET /supported_languages".format(language)
        )
    return language


def validate_test_type(test_type):
    test = TestType.objects.filter(value=test_type).first()
    if test is None:
        raise serializers.ValidationError(
            "Test type {} not supported. Please check GET /supported_test_types".format(test_type)
        )
    return test_type
