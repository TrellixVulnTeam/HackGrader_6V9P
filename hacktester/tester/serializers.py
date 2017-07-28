from rest_framework import serializers

from .models import TestRun, Language, TestType
from .validators import validate_extra_options_dict, validate_language, validate_test_type


class TestRunSerializer(serializers.ModelSerializer):
    extra_options = serializers.CharField(allow_blank=True, required=False, validators=[validate_extra_options_dict])
    language = serializers.PrimaryKeyRelatedField(
        validators=[validate_language],
    )
    test_type = serializers.PrimaryKeyRelatedField(validators=[validate_test_type])

    class Meta:
        model = TestRun
        fields = ('language', 'test_type', 'created_at', 'status',
                  'extra_options', 'number_of_results', 'test', 'solution')
