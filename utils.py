import re
from datetime import datetime

PHONE_CODE_NUMBER_BY_DEFAULT = '+38'
PHONE_CODE_NUMBER_BY_DEFAULT_WITHOUT_PLUS = '38'

def normalize_phone(phone_number: str) -> str:
    cleaned_phone_number = re.sub(r'[^\d+]', '', phone_number)
    
    if cleaned_phone_number.startswith('+'):
        if cleaned_phone_number.startswith(PHONE_CODE_NUMBER_BY_DEFAULT):
            return cleaned_phone_number
        else:
            return PHONE_CODE_NUMBER_BY_DEFAULT + cleaned_phone_number[1:]
    elif cleaned_phone_number.startswith(PHONE_CODE_NUMBER_BY_DEFAULT_WITHOUT_PLUS):
        return PHONE_CODE_NUMBER_BY_DEFAULT + cleaned_phone_number[2:]
    else:
        return PHONE_CODE_NUMBER_BY_DEFAULT + cleaned_phone_number
    
from datetime import datetime, timedelta
from typing import List, Dict

def get_upcoming_birthdays(records):
    current_date = datetime.today().date()
    next_week_date = current_date + timedelta(days=7)
    results = []

    for record in records.values():
        if record.birthday:
            birthday_date = record.birthday.value.date()
            
            birthday_this_year = birthday_date.replace(year=current_date.year)

            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)
            
            if current_date <= birthday_this_year <= next_week_date:
                results.append(record)
    
    return results