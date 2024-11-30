from rest_framework import serializers
from ..models import Month, Overview


# Entry Serializer
class EntrySerializer(serializers.Serializer):
    text = serializers.CharField()
    amount = serializers.FloatField()


# Overview Serializer
class OverviewSerializer(serializers.Serializer):
    income = EntrySerializer(many=True)
    fixed_expenses = EntrySerializer(many=True)
    savings_goal = EntrySerializer()
    spending_goal = EntrySerializer()


# Month Serializer
class MonthSerializer(serializers.ModelSerializer):
    overview = OverviewSerializer()
    class Meta:
        model = Month
        fields = ['id', 'user_id', 'year', 'month', 'overview']
    def create(self, validated_data):
        try:
            month = Month.objects.create(**validated_data)
            month.save()
            return month
        except Exception as ex:
            raise f'Something went wrong creating month record. More info: {ex}'