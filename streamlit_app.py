from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
TABLES_DIR = BASE_DIR / "outputs" / "tables"


st.set_page_config(
    page_title="Dashboard Ejecutivo E-commerce",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(107,138,58,0.10), transparent 28%),
                linear-gradient(180deg, #f9f5ee 0%, #f4efe7 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero-card {
            background: rgba(255, 250, 242, 0.92);
            border: 1px solid #d6cfbf;
            border-radius: 22px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 18px 35px rgba(24, 35, 15, 0.06);
            margin-bottom: 1rem;
        }
        .hero-eyebrow {
            display: inline-block;
            background: #dfe8c8;
            color: #6b8a3a;
            border-radius: 999px;
            padding: 0.3rem 0.7rem;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            font-weight: 700;
        }
        .hero-title {
            font-size: 2.5rem;
            color: #18230f;
            line-height: 1.02;
            margin: 0.9rem 0 0.5rem 0;
            font-weight: 700;
        }
        .hero-text {
            color: #5a6650;
            font-size: 1rem;
            line-height: 1.65;
            max-width: 780px;
        }
        .insight-card {
            background: #fffaf2;
            border: 1px solid #d6cfbf;
            border-left: 5px solid #6b8a3a;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            color: #4d5845;
            min-height: 145px;
        }
        .section-title {
            color: #18230f;
            font-size: 1.2rem;
            font-weight: 700;
            margin-top: 0.3rem;
            margin-bottom: 0.3rem;
        }
        div[data-testid="stMetric"] {
            background: #fffaf2;
            border: 1px solid #d6cfbf;
            border-radius: 18px;
            padding: 0.75rem 0.9rem;
        }
        div[data-testid="stMetricLabel"] {
            color: #5a6650;
        }
        div[data-testid="stMetricValue"] {
            color: #18230f;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_table(filename: str) -> pd.DataFrame:
    path = TABLES_DIR / filename
    if not path.exists():
        st.error(
            f"No se encontró {filename}. Ejecuta primero `python src/generate_sample_data.py` y `python src/analyze_ecommerce.py`."
        )
        st.stop()
    return pd.read_csv(path)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = load_table("executive_summary.csv")
    channels = load_table("channel_performance.csv")
    categories = load_table("category_performance.csv")
    rfm = load_table("rfm_segments.csv")
    monthly = load_table("monthly_sales.csv")
    return summary, channels, categories, rfm, monthly


def metric_lookup(summary_df: pd.DataFrame) -> dict[str, float]:
    return dict(zip(summary_df["metric"], summary_df["value"]))


def fmt_currency(value: float) -> str:
    return f"${value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


inject_styles()
summary_df, channels_df, categories_df, rfm_df, monthly_df = load_data()
summary = metric_lookup(summary_df)

top_channel = channels_df.sort_values("gross_profit", ascending=False).iloc[0]
worst_channel = channels_df.sort_values("roas", ascending=True).iloc[0]
top_category = categories_df.sort_values("return_rate_pct", ascending=False).iloc[0]

st.markdown(
    f"""
    <div class="hero-card">
        <span class="hero-eyebrow">Portafolio de Data Analytics</span>
        <div class="hero-title">Rentabilidad y retención en e-commerce</div>
        <div class="hero-text">
            Este dashboard traduce un problema comercial en una lectura ejecutiva: qué canales,
            categorías y segmentos ayudan a crecer con rentabilidad y cuáles están generando
            fricción en margen, devoluciones y eficiencia de inversión.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Foco del dashboard")
    view = st.radio(
        "Selecciona la vista",
        ["Resumen ejecutivo", "Canales y categorías", "Clientes y retención"],
    )
    st.markdown("## KPIs rápidos")
    st.write(f"Ingreso neto: {fmt_currency(summary['net_revenue'])}")
    st.write(f"Utilidad bruta: {fmt_currency(summary['gross_profit'])}")
    st.write(f"Margen bruto: {fmt_pct(summary['gross_margin_pct'])}")
    st.write(f"ROAS: {summary['roas']:.2f}")


col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingreso neto", fmt_currency(summary["net_revenue"]))
col2.metric("Utilidad bruta", fmt_currency(summary["gross_profit"]))
col3.metric("Margen bruto", fmt_pct(summary["gross_margin_pct"]))
col4.metric("ROAS", f"{summary['roas']:.2f}")

col5, col6, col7 = st.columns(3)
col5.metric("Ticket promedio", fmt_currency(summary["average_order_value"]))
col6.metric("Tasa de recompra", fmt_pct(summary["repeat_purchase_rate_pct"]))
col7.metric("Tasa de devoluciones", fmt_pct(summary["return_rate_pct"]))


if view == "Resumen ejecutivo":
    st.markdown('<div class="section-title">Lectura ejecutiva</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.markdown(
        f"""
        <div class="insight-card">
            <strong>Canal más rentable</strong><br><br>
            {top_channel['acquisition_channel']} lidera en utilidad bruta con {fmt_currency(top_channel['gross_profit'])}.
            Eso sugiere que la calidad del ingreso pesa más que el simple volumen.
        </div>
        """,
        unsafe_allow_html=True,
    )
    b.markdown(
        f"""
        <div class="insight-card">
            <strong>Canal con peor eficiencia</strong><br><br>
            {worst_channel['acquisition_channel']} muestra el ROAS más bajo con {worst_channel['roas']:.2f},
            lo que abre espacio para revisar inversión y descuento.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c.markdown(
        f"""
        <div class="insight-card">
            <strong>Mayor alerta operativa</strong><br><br>
            {top_category['category']} tiene la tasa de devolución más alta con {fmt_pct(top_category['return_rate_pct'])}.
            Allí puede haber problemas de producto, surtido o experiencia.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns((1.1, 0.9))

    monthly_chart = px.line(
        monthly_df,
        x="order_month",
        y="net_revenue",
        markers=True,
        color_discrete_sequence=["#6B8A3A"],
    )
    monthly_chart.update_layout(
        title="Tendencia mensual del ingreso neto",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    left.plotly_chart(monthly_chart, use_container_width=True)

    channel_chart = px.bar(
        channels_df.sort_values("gross_profit", ascending=True),
        x="gross_profit",
        y="acquisition_channel",
        orientation="h",
        color="gross_profit",
        color_continuous_scale=["#DDE7C5", "#6B8A3A"],
    )
    channel_chart.update_layout(
        title="Utilidad bruta por canal",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    right.plotly_chart(channel_chart, use_container_width=True)

    return_chart = px.bar(
        categories_df.sort_values("return_rate_pct", ascending=True),
        x="return_rate_pct",
        y="category",
        orientation="h",
        color="return_rate_pct",
        color_continuous_scale=["#F2D2C8", "#A64032"],
    )
    return_chart.update_layout(
        title="Tasa de devolución por categoría",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(return_chart, use_container_width=True)

if view == "Canales y categorías":
    st.markdown('<div class="section-title">Desempeño comercial</div>', unsafe_allow_html=True)
    left, right = st.columns((1, 1))

    scatter = px.scatter(
        channels_df,
        x="roas",
        y="gross_margin_pct",
        size="net_revenue",
        color="acquisition_channel",
        hover_name="acquisition_channel",
        color_discrete_sequence=["#6B8A3A", "#C97C2C", "#1F4E5F", "#A64032", "#9D8C5A"],
    )
    scatter.update_layout(
        title="Trade-off entre ROAS y margen bruto",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    left.plotly_chart(scatter, use_container_width=True)

    discount_chart = px.bar(
        categories_df.sort_values("avg_discount_rate_pct", ascending=False),
        x="category",
        y="avg_discount_rate_pct",
        color="avg_discount_rate_pct",
        color_continuous_scale=["#E8DDB6", "#C97C2C"],
    )
    discount_chart.update_layout(
        title="Descuento promedio por categoría",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    right.plotly_chart(discount_chart, use_container_width=True)

    st.dataframe(
        channels_df.sort_values("gross_profit", ascending=False).style.format(
            {
                "net_revenue": "${:,.0f}",
                "gross_profit": "${:,.0f}",
                "return_rate_pct": "{:.1f}%",
                "avg_discount_rate_pct": "{:.1f}%",
                "roas": "{:.2f}",
                "gross_margin_pct": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.dataframe(
        categories_df.sort_values("return_rate_pct", ascending=False).style.format(
            {
                "net_revenue": "${:,.0f}",
                "gross_profit": "${:,.0f}",
                "return_rate_pct": "{:.1f}%",
                "avg_discount_rate_pct": "{:.1f}%",
                "gross_margin_pct": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

if view == "Clientes y retención":
    st.markdown('<div class="section-title">Segmentación y retención</div>', unsafe_allow_html=True)
    segment_mix = (
        rfm_df["segment"]
        .value_counts()
        .rename_axis("segment")
        .reset_index(name="customers")
    )

    left, right = st.columns((0.85, 1.15))
    segment_chart = px.bar(
        segment_mix.sort_values("customers", ascending=False),
        x="segment",
        y="customers",
        color="segment",
        color_discrete_sequence=["#6B8A3A", "#1F4E5F", "#C97C2C", "#A64032"],
    )
    segment_chart.update_layout(
        title="Mix de segmentos RFM",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    left.plotly_chart(segment_chart, use_container_width=True)

    top_customers = rfm_df.sort_values(["monetary", "frequency"], ascending=False).head(15)
    right.dataframe(
        top_customers.style.format(
            {
                "monetary": "${:,.0f}",
                "recency": "{:.0f}",
                "frequency": "{:.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    champions = int((rfm_df["segment"] == "Champions").sum())
    at_risk = int((rfm_df["segment"] == "At Risk").sum())
    loyal = int((rfm_df["segment"] == "Loyal").sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes Champions", f"{champions:,}")
    c2.metric("Clientes Loyal", f"{loyal:,}")
    c3.metric("Clientes At Risk", f"{at_risk:,}")

    st.markdown(
        """
        <div class="insight-card">
            <strong>Cómo leer esta página</strong><br><br>
            La retención no debería tratar a todos los clientes igual. Los segmentos con mayor valor y mejor frecuencia
            merecen acciones de fidelización, mientras que los segmentos en riesgo requieren campañas más tácticas de reactivación.
        </div>
        """,
        unsafe_allow_html=True,
    )
