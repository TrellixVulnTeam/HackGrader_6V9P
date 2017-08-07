from rest_framework import serializers

from .models import TestRun
from .validators import validate_language, validate_test_type


class TestRunSerializer(serializers.ModelSerializer):
    extra_options = serializers.DictField(required=False)
    language = serializers.CharField(validators=[validate_language])
    test_type = serializers.CharField(validators=[validate_test_type])
    test = serializers.CharField(required=False)
    solution = serializers.CharField(required=False)

    def to_internal_value(self, data):
        extra_options = data.get('extra_options')
        if extra_options is not None and type(extra_options) is not dict:
            raise serializers.ValidationError(
                {"invalid_extra_options": "Extra options must be dict!, not {}".format(type(extra_options))}
            )

        return super().to_internal_value(data)

    class Meta:
        model = TestRun
        fields = ('language', 'test_type', 'created_at', 'status',
                  'extra_options', 'number_of_results', 'test', 'solution')
