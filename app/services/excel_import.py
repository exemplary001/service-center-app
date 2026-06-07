import pandas as pd

from app.models import Customer


def import_sample_data(db):

    existing_records = db.query(Customer).count()

    if existing_records > 0:
        return

    df = pd.read_excel(
        "HANIF.xlsx",
        sheet_name="FILE 1"
    )

    for _, row in df.iterrows():

        customer = Customer(
            customer_name=str(row["NAME"]),
            address=str(row["ADDRESS"]),
            phone_number=str(row["MOBILE NUMBER"]),
            call_date=row["DATE"].date(),
            total_calls=int(row["OVERALL CALL"]),
            closed_calls=int(row["CLOSED CALL"])
        )

        db.add(customer)

    db.commit()