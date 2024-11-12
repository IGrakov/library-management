from django.contrib import admin

from reader_card.models import ReaderCard


@admin.register(ReaderCard)
class ReaderCardAdmin(admin.ModelAdmin):
    @admin.display(description='Allowed Halls')
    def halls(self, reader_card):
        halls = []
        for hall_ in reader_card.hall_access.all():
            halls.append(hall_.name)
        return ', '.join(halls)

    list_select_related = ('reader',)
    list_display = ('reader__last_name', 'reader__first_name', 'is_suspended', 'photo', 'halls')
    list_filter = ('is_suspended', 'hall_access')

    ordering = (
        'reader__last_name',
    )

    list_per_page = 20

    @staticmethod
    def reader__last_name(obj):
        return obj.reader.last_name

    @staticmethod
    def reader__first_name(obj):
        return obj.reader.first_name
