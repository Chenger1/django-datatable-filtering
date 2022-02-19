from collections import namedtuple

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

from .utils import get_none_attr


order_dict = {'asc': '', 'desc': '-'}


class DatatableFilter:
    """Class with filtering logic for response in DatatableFilterView."""


    def __init__(self,
                 request,
                 columns,
                 queryset,
                 filter_columns,
                 filter_range_columns,
                 filter_property,
                 actions_fields,
                 default_order="-pk"):
        self.columns = columns
        self.request_values = request.GET
        self.result_data = None
        self.cardinality_filtered = 0
        # total in the table unfiltered
        self.cardinality = 0
        self.queryset = queryset
        self.filter_columns = filter_columns
        self.filter_property = filter_property
        self.filter_range_columns = filter_range_columns
        self.actions_fields = actions_fields
        self.default_order = default_order

    def output_result(self):
        output = {}
        output['sEcho'] = int(self.request_values['sEcho'])
        output['iTotalRecords'] = self.queryset.count()
        output['iTotalDisplayRecords'] = self.cardinality_filtered
        output['aaData'] = list(self.result_data)
        return output

    def paging(self):
        pages = namedtuple('pages', ('start', 'length', 'total_length'))
        pages.start = int(self.request_values.get('iDisplayStart', 0))
        pages.length = int(self.request_values.get('iDisplayLength', 10))
        pages.total_length = pages.start + pages.length
        return pages

    def filtering(self):
        filter_fields = {}
        for filter_column in get_none_attr(self, 'filter_columns', []):
            filter_value = self.request_values.get(f'filter_{filter_column}')
            if filter_value:
                filter_fields[f'{filter_column}__icontains'] = filter_value

        for filter_range_column in get_none_attr(self, 'filter_range_columns', []):
            column_range = self.request_values.get(f'filter_{filter_range_column}', '').split(' to ')
            if len(column_range) == 2:
                filter_fields[f'{filter_range_column}__range'] = (column_range[0], column_range[1])
            if len(column_range) == 1 and column_range[0] != '':
                filter_fields[f'{filter_range_column}__range'] = (column_range[0], column_range[0])

        return filter_fields

    def sorting(self):
        order = self.default_order
        datatable_sort_col = self.request_values.get('iSortCol_0', '')
        datatable_sorting_cols = int(self.request_values.get('iSortingCols', 0))

        if datatable_sort_col and datatable_sorting_cols > 0:
            for index in range(datatable_sorting_cols):
                column_number = int(self.request_values[f'iSortCol_{index}'])
                sort_direction = self.request_values[f'sSortDir_{index}']

                order = (
                        ("" if order == "" else ",") +
                        order_dict[sort_direction] +
                        self.columns[column_number]
                )
        return order

    def has_property_filter(self):
        for filter_property in self.filter_property:
            if self.request_values.get(f'filter_{filter_property}'):
                return True
        return False

    def get_structure_column(self, field, instance):
        field_path = field.split('__')
        attr = instance
        for elem in field_path:
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                return None
        return attr

    def get_data_list(self, data):
        for row in data:
            query_row = {}
            for column in self.columns:
                if '__' in column:
                    query_row[column] = str(self.get_structure_column(column, row))
                else:
                    query_row[column] = str(getattr(row, column))
                if self.actions_fields:
                    _actions_fields = {}
                    for action_field in self.actions_fields:
                        _actions_fields[action_field] = str(getattr(row, action_field))
                    query_row['actions'] = _actions_fields
            yield query_row

    def pagination(self, data, pages):
        paginator = Paginator(data, pages.length)
        current_page = int(pages.total_length / pages.length)
        try:
            paginated_data = paginator.page(current_page)
        except (InvalidPage, PageNotAnInteger):
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        return paginated_data

    def filtering_property(self, data):
        data_filtered = []

        for obj in data:
            valid = False

            for prop in self.filter_property:
                property_value = self.request_values.get(f'filter_{prop}', '').lower()
                if property_value:
                    obj_property = getattr(obj, prop, '').lower()
                    if property_value in obj_property:
                        valid = True
            if valid:
                data_filtered.append(obj)
        return data_filtered

    def run_queries(self):
        pages = self.paging()
        _filter = self.filtering()
        sorting = self.sorting()

        qs = self.queryset
        if _filter:
            data = qs.filter(**_filter).order_by('%s' % sorting)
        else:
            data = qs.order_by('%s' % sorting)

        if self.has_property_filter():
            data = self.filtering_property(data)
        paginated_data = self.pagination(data, pages)
        serialized_data = self.get_data_list(paginated_data)
        self.result_data = serialized_data
        self.cardinality_filtered = paginated_data.paginator.num_pages
        self.cardinality = pages.total_length - pages.start
