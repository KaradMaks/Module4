import datetime

from django.contrib import admin
from django.db.models import DateField, DateTimeField
from django.utils import timezone

from .models import Advertisement


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'description', 'price',
        'created_date', 'auction', 'updated_date', 'get_html_image',
    ]

    list_filter = ['auction', 'created_at']
    actions = ['make_auction_as_false', 'make_auction_as_true']

    fieldsets = (
        ('Общее', {
            'fields': ('title', 'description', 'image', 'user'),
        }),
        ('Финансы', {
            'fields': ('price', 'auction'),
            'classes': ['collapse']
        })
    )

    @staticmethod
    def update_with_last_modified_time(qs, **kwargs):
        # This function adds any auto_now field to the update call because QuerySet.update() doesn't do it :X
        model_fields = qs.model._meta.get_fields()
        fields_and_value_map = {}
        for field in model_fields:
            try:
                auto_now = field.auto_now
            except AttributeError:
                auto_now = False

            if auto_now:
                if type(field) == DateField:
                    fields_and_value_map[field.name] = datetime.date.today()
                elif type(field) == DateTimeField:
                    fields_and_value_map[field.name] = timezone.now()

        fields_and_value_map.update(kwargs)
        return qs.update(**fields_and_value_map)

    @admin.action(description='Убрать возможность торга')
    def make_auction_as_false(self, request, queryset):
        queryset.update(auction=False)
        self.update_with_last_modified_time(queryset)

    @admin.action(description='Добавить возможность торга')
    def make_auction_as_true(self, request, queryset):
        queryset.update(auction=True)
        self.update_with_last_modified_time(queryset)


admin.site.register(Advertisement, AdvertisementAdmin)
