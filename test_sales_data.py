import pandas as pd

from sales_data import (
    get_category_breakdown,
    get_monthly_sales_trend,
    get_region_breakdown,
    get_total_orders,
    get_total_sales,
    load_sales_data,
)


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


def _sample_df():
    return pd.DataFrame({
        "total_amount": [159.98, 74.97, 299.99],
    })


def test_get_total_sales_sums_total_amount():
    assert get_total_sales(_sample_df()) == 534.94


def test_get_total_orders_counts_rows():
    assert get_total_orders(_sample_df()) == 3


def test_get_monthly_sales_trend_groups_and_sorts_by_month():
    df = pd.DataFrame({
        "date": pd.to_datetime([
            "2024-02-10", "2024-01-05", "2024-01-20",
        ]),
        "total_amount": [5.0, 10.0, 20.0],
    })

    trend = get_monthly_sales_trend(df)

    assert list(trend["month"]) == [
        pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01"),
    ]
    assert list(trend["total_amount"]) == [30.0, 5.0]


def test_get_category_breakdown_sums_and_sorts_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Accessories", "Audio", "Wearables"],
        "total_amount": [10.0, 50.0, 20.0, 25.0],
    })

    breakdown = get_category_breakdown(df)

    assert list(breakdown["category"]) == ["Accessories", "Audio", "Wearables"]
    assert list(breakdown["total_amount"]) == [50.0, 30.0, 25.0]


def test_get_region_breakdown_sums_and_sorts_descending():
    df = pd.DataFrame({
        "region": ["North", "South", "North"],
        "total_amount": [40.0, 60.0, 10.0],
    })

    breakdown = get_region_breakdown(df)

    assert list(breakdown["region"]) == ["South", "North"]
    assert list(breakdown["total_amount"]) == [60.0, 50.0]
