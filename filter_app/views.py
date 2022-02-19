from django.views.generic import View
from django.shortcuts import render

from .models import Transaction
from filter_datatable.views import DatatableFilterView


class MainView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class MainViewFilter(DatatableFilterView):
    queryset = Transaction.objects.all()
    columns = ('amount', 'customer', 'date', 'text', 'another_text', 'boolean_field', 'some_text', 'price', 'vendor',
               'boolean_field1', 'boolean_field2', 'number_customer')
    filter_columns = ('amount', )
    filter_range_columns = ['date']
    filter_property = ['number_customer']
