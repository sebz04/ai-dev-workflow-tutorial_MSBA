import pandas as pd

from sales_data import load_sales_data


def test_load_sales_data_parses_columns_and_dtypes(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n"
        "2024-01-04,ORD-002,Phone Case,Accessories,South,3,24.99,74.97\n"
    )

    df = load_sales_data(str(csv_path))

    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert len(df) == 2
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
