import random
from datetime import datetime, timedelta

statuses = ['live', 'draft', 'approved']
types = ['fixed', 'ranged']
services = ['kylie', 'jason']
jurisdictions1 = ['bonnie', 'clyde']
jurisdictions2 = ['tom', 'jerry']

base_date = datetime(2024, 1, 1)
insert_statements = []

for i in range(1, 101):
    code = f"FEE{i:03}"
    value = round(random.uniform(10, 300), 2)
    description = "Lorem ipsum dolor sit amet"
    status = random.choice(statuses)
    type_ = random.choice(types)
    service = random.choice(services)
    jurisdiction1 = random.choice(jurisdictions1)
    jurisdiction2 = random.choice(jurisdictions2)

    start_date = base_date + timedelta(days=random.randint(0, 365))
    end_date = start_date + timedelta(days=random.randint(1, 365))

    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    insert = (
        f"INSERT INTO fees (code, value, description, status, start_date, end_date, type, service, jurisdiction1, jurisdiction2) "
        f"VALUES ('{code}', {value}, '{description}', '{status}', '{start_date_str}', '{end_date_str}', "
        f"'{type_}', '{service}', '{jurisdiction1}', '{jurisdiction2}');"
    )
    insert_statements.append(insert)

with open("02-data.sql", "w") as f:
    f.write("\n".join(insert_statements))
