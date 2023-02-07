from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginator(request, scrape_list, count):
    """
    Function returns paginator object
    :param request: request
    :param scrape_list: list of scraped data
    :param count: count of items per page
    :return: paginator object
    """
    paginator = Paginator(scrape_list, count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
