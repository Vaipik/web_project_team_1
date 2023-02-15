from datetime import date
from dateutil.relativedelta import relativedelta


def happens_in(birthday, days):
    """
    Calculates if person's birthday falls in the range.
    :param birthday: date
    :param days: days from today
    :return: True if birthday is within the period False otherwise
    """
    today = date.today()
    birthday = date(today.year, birthday.month, birthday.day)
    difference = birthday - today
    if difference.days >= 0:
        return difference.days <= relativedelta(days=days).days
    else:
        abs_difference = today + relativedelta(days=difference.days) + relativedelta(years=1)
        return abs_difference <= relativedelta(days=days) + today


def get_birthday_list(list_of_contacts, days):
    """
    Returns a list of contacts who have birthdays from today up to the number of given days.
    """
    contacts = []
    num_days = int(days)
    for cont in list_of_contacts:
        if happens_in(cont.birthday, num_days):
            contacts.append(cont)
    return contacts
