from datetime import datetime

def clean_currency(item: str) -> float:
    stripped = item.replace("$", "").replace(",", "")
    return float(stripped)

def extract_year_mdy(timestamp):

    datetime_yr = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S').year
    return datetime_yr

def clean_country_usa(item: str) ->str:

    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    if item.strip().lower() in possibilities:
        return 'United States'
    else:
        return item
    


if __name__=='__main__':
    print(

        clean_currency('$1,000,000.00'),
        extract_year_mdy('12/31/2021 23:59:59'),
        clean_country_usa('United States of America')
        )

