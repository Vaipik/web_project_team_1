from django.db.models import Q


def get_filter_query_conditions(fields: list, query_string: str):
    filter_conditions = Q()
    query_list = query_string.split()

    if query_list:
        for query in query_list:
            for field in fields:
                filter_conditions = (
                    filter_conditions | Q(**{f"{field}__icontains": query})
                )

    return filter_conditions
