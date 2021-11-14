import django_tables2 as tables

from .models import AbbreviatedLink, Transition


class AbbreviatedLinkTable(tables.Table):
    created_time_and_date = tables.columns.DateTimeColumn(format="Y-m-d H:i")
    my_column = tables.TemplateColumn(verbose_name='',
                                      template_name='tables/buttons.html',
                                      orderable=False)

    class Meta:
        model = AbbreviatedLink
        template_name = 'django_tables2/semantic.html'
        exclude = ('owner', 'id')
        row_attrs = {
            "data-id": lambda record: record.pk
        }


class TransitionTable(tables.Table):
    class Meta:
        model = Transition
        attrs = {'class': 'paleblue'}
