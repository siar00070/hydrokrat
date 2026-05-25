import csv


def save_lead(
    name,
    company,
    phone,
    email,
    application,
    flow,
    head
):

    with open(
        "leads.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            company,
            phone,
            email,
            application,
            flow,
            head
        ])