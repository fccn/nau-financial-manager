# Util module

## Descripiton

This module is responsible to define high classes and defaults to be used on entire project compaing the SOLID concepts and good practices.

### Based Views

#### The ApiQuery class
Is a utility class for performing common API query operations. It provides two static methods: paginator and filter_queryset.

The paginator method paginates a query result using the Django Paginator class. It takes three arguments: result_query, which is the query result to paginate; total_results, which is the total number of results to paginate; and page, which is the page number to return. It returns a paginated query result.

The filter_queryset method filters a queryset using filter backends. It takes four arguments: filter_backends, which is a list of filter backends to apply; request, which is the request object; queryset, which is the queryset to filter; and view, which is the view object. It returns a filtered queryset.

#### The Format class
Is a utility class for formatting data. It provides static methods for formatting error messages, success responses, and dates.

The limit_string_size method limits the size of a string. It takes two arguments: string, which is the string to limit, and tam, which is the maximum length of the string. It returns a string with a maximum length of tam.

The format_error_limit_string method formats an error message. It takes three keyword arguments: codeError, which is the error code; nomeErro, which is the error name; and descricaoErro, which is the error description. It returns a dictionary containing the formatted error message.

The format_success method formats a success response. It takes two keyword arguments: codeError, which is the success code; and data, which is the success data. It returns a dictionary containing the formatted success response.

The format_success_paginated method formats a paginated success response. It takes three keyword arguments: codeError, which is the success code; data, which is the success data; and recordCount, which is the total number of records. It returns a dictionary containing the formatted paginated success response.

The format_date method formats a timestamp as a date. It takes one argument: timestamp, which is the timestamp to format. It returns a datetime object representing the formatted date.

The get_today method gets the current date as a timestamp. It returns a timestamp representing the current date.

The get_yesterday method gets yesterday's date as a timestamp. It returns a timestamp representing yesterday's date.


#### The CustomPageNumberPagination class

The CustomPageNumberPagination class is a custom pagination class that extends the PageNumberPagination class. It provides custom query parameters for pagination.

The page_query_param attribute is the query parameter for the current page number. The page_size_query_param attribute is the query parameter for the number of items per page. The page_size attribute is the default number of items per page.

#### The BaseAPIView class

Is a base class for API views.

The get_queryset method returns a queryset filtered by the given relations. It takes two arguments: _ (unused) and **relations, which are the relations to filter by.

The get_context method returns a dictionary of context data for the view. It takes one argument: request, which is the request object.

The get_serializer method returns the serializer instance for the view. It first sets the serializer name to "serializer". It then appends the custom_class_prefix_serializer attribute to the custom_prefixes_serializers list. It then iterates over the custom_prefixes_serializers list and checks if the expected serializer name exists. If it does, it sets the serializer name to the expected serializer name. Finally, it returns the serializer instance using the getattr function.
