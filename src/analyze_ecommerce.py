from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
TABLES_DIR = BASE_DIR / "outputs" / "tables"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv(RAW_DIR / "customers.csv", parse_dates=["signup_date"])
    products = pd.read_csv(RAW_DIR / "products.csv")
    orders = pd.read_csv(RAW_DIR / "orders.csv", parse_dates=["order_date"])
    marketing = pd.read_csv(RAW_DIR / "marketing_spend.csv", parse_dates=["spend_date"])
    return customers, products, orders, marketing


def prepare_dataset(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    df = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .drop_duplicates()
    )

    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]
    df["product_cost"] = df["quantity"] * df["unit_cost"]
    df["net_realized_revenue"] = df["net_revenue"].where(df["returned_flag"] == 0, 0)
    df["gross_profit"] = df["net_realized_revenue"] - df["product_cost"] - df["shipping_cost"]
    df["discount_rate"] = (df["discount_amount"] / df["gross_revenue"]).fillna(0)
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def build_executive_summary(df: pd.DataFrame, marketing: pd.DataFrame) -> pd.DataFrame:
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    repeat_customers = (
        df.groupby("customer_id")["order_id"].nunique().gt(1).sum()
    )

    total_marketing = marketing["spend"].sum()
    total_net_revenue = df["net_realized_revenue"].sum()
    total_profit = df["gross_profit"].sum()

    summary = pd.DataFrame(
        {
            "metric": [
                "total_customers",
                "total_orders",
                "net_revenue",
                "gross_profit",
                "gross_margin_pct",
                "average_order_value",
                "repeat_purchase_rate_pct",
                "return_rate_pct",
                "avg_discount_rate_pct",
                "marketing_spend",
                "roas",
            ],
            "value": [
                total_customers,
                total_orders,
                round(total_net_revenue, 2),
                round(total_profit, 2),
                round((total_profit / total_net_revenue) * 100, 2),
                round(total_net_revenue / total_orders, 2),
                round((repeat_customers / total_customers) * 100, 2),
                round(df["returned_flag"].mean() * 100, 2),
                round(df["discount_rate"].mean() * 100, 2),
                round(total_marketing, 2),
                round(total_net_revenue / total_marketing, 2),
            ],
        }
    )
    return summary


def build_channel_performance(df: pd.DataFrame, marketing: pd.DataFrame) -> pd.DataFrame:
    channel_metrics = (
        df.groupby("acquisition_channel", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            customers=("customer_id", "nunique"),
            net_revenue=("net_realized_revenue", "sum"),
            gross_profit=("gross_profit", "sum"),
            return_rate_pct=("returned_flag", lambda x: x.mean() * 100),
            avg_discount_rate_pct=("discount_rate", lambda x: x.mean() * 100),
        )
    )

    spend_by_channel = marketing.groupby("acquisition_channel", as_index=False)["spend"].sum()
    channel_metrics = channel_metrics.merge(spend_by_channel, on="acquisition_channel", how="left")
    channel_metrics["roas"] = channel_metrics["net_revenue"] / channel_metrics["spend"]
    channel_metrics["gross_margin_pct"] = (
        channel_metrics["gross_profit"] / channel_metrics["net_revenue"]
    ) * 100
    return channel_metrics.sort_values("gross_profit", ascending=False)


def build_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    category_metrics = (
        df.groupby("category", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            net_revenue=("net_realized_revenue", "sum"),
            gross_profit=("gross_profit", "sum"),
            return_rate_pct=("returned_flag", lambda x: x.mean() * 100),
            avg_discount_rate_pct=("discount_rate", lambda x: x.mean() * 100),
        )
    )
    category_metrics["gross_margin_pct"] = (
        category_metrics["gross_profit"] / category_metrics["net_revenue"]
    ) * 100
    return category_metrics.sort_values("return_rate_pct", ascending=False)


def build_rfm_segments(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)
    rfm = (
        df.groupby("customer_id", as_index=False)
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("net_realized_revenue", "sum"),
            acquisition_channel=("acquisition_channel", "first"),
            region=("region", "first"),
        )
    )

    rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1], duplicates="drop").astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

    def segment(score: int) -> str:
        if score >= 10:
            return "Champions"
        if score >= 8:
            return "Loyal"
        if score >= 6:
            return "Potential Loyalist"
        return "At Risk"

    rfm["segment"] = rfm["rfm_score"].apply(segment)
    return rfm.sort_values(["rfm_score", "monetary"], ascending=[False, False])


def export_charts(channel_metrics: pd.DataFrame, category_metrics: pd.DataFrame, monthly_sales: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=channel_metrics,
        x="gross_profit",
        y="acquisition_channel",
        hue="acquisition_channel",
        palette="Blues_r",
        legend=False,
    )
    plt.title("Gross Profit by Acquisition Channel")
    plt.xlabel("Gross Profit")
    plt.ylabel("Acquisition Channel")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "gross_profit_by_channel.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=category_metrics,
        x="return_rate_pct",
        y="category",
        hue="category",
        palette="Reds_r",
        legend=False,
    )
    plt.title("Return Rate by Category")
    plt.xlabel("Return Rate (%)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "return_rate_by_category.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=monthly_sales, x="order_month", y="net_revenue", marker="o")
    plt.title("Monthly Net Revenue Trend")
    plt.xlabel("Order Month")
    plt.ylabel("Net Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "monthly_net_revenue.png", dpi=150)
    plt.close()


def main() -> None:
    ensure_directories()
    customers, products, orders, marketing = load_data()
    df = prepare_dataset(customers, products, orders)

    summary = build_executive_summary(df, marketing)
    channel_metrics = build_channel_performance(df, marketing)
    category_metrics = build_category_performance(df)
    rfm_segments = build_rfm_segments(df)
    monthly_sales = df.groupby("order_month", as_index=False)["net_realized_revenue"].sum()
    monthly_sales = monthly_sales.rename(columns={"net_realized_revenue": "net_revenue"})

    df.to_csv(PROCESSED_DIR / "ecommerce_clean.csv", index=False)
    summary.to_csv(TABLES_DIR / "executive_summary.csv", index=False)
    channel_metrics.to_csv(TABLES_DIR / "channel_performance.csv", index=False)
    category_metrics.to_csv(TABLES_DIR / "category_performance.csv", index=False)
    rfm_segments.to_csv(TABLES_DIR / "rfm_segments.csv", index=False)
    monthly_sales.to_csv(TABLES_DIR / "monthly_sales.csv", index=False)

    export_charts(channel_metrics, category_metrics, monthly_sales)

    print("Analysis complete. Results exported to outputs/tables and outputs/charts")


if __name__ == "__main__":
    main()
