from django.views.generic import View
from django.http import JsonResponse

from .filter import DatatableFilter


class DatatableFilterView(View):
    """
       Filter view base class that returns filtering data to datatable.

       To use, need to inherit and override next fields:
       columns: all display columns in datatable,
       filter_columns: colums for filtering (default: simple text using searching with icontains)
       filter_range_columns: columns for filtering date in range [from; to]
       actions_fields: fields that will return as dict (F.e. {"id": 1, is_active: true})
           using in specified url generation for every row in datatable
       default_order: field for ordering queryset
       """

    queryset = None
    columns = None
    filter_columns = None
    filter_range_columns = None
    actions_fields = None
    filter_property = None
    default_order = '-pk'

    def get(self, request, *args, **kwargs):
        datatable_filter = DatatableFilter(
            request,
            self.columns,
            self.queryset,
            self.filter_columns,
            self.filter_range_columns,
            self.filter_property,
            self.actions_fields,
            self.default_order
        )
        datatable_filter.run_queries()
        return JsonResponse(datatable_filter.output_result(), safe=False)

    def post(self, request, *args, **kwargs):
        datatable_filter = DatatableFilter(
            request,
            self.columns,
            self.queryset,
            self.filter_columns,
            self.filter_property,
            self.filter_range_columns,
            self.actions_fields,
            self.default_order
        )
        datatable_filter.run_queries()
        return JsonResponse(datatable_filter.output_result(), safe=False)
