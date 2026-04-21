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
        .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 1rem;
            margin-top: 1.2rem;
        }
        .hero-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.82), rgba(247,244,237,0.92));
            border: 1px solid #d6cfbf;
            border-radius: 18px;
            padding: 1rem 1.1rem;
        }
        .hero-panel h4 {
            color: #18230f;
            margin: 0 0 0.6rem 0;
            font-size: 1rem;
        }
        .hero-panel p, .hero-panel li {
            color: #4d5845;
            line-height: 1.6;
            margin: 0;
        }
        .hero-panel ul {
            padding-left: 1.1rem;
            margin: 0;
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
        .story-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 1rem 0 1.2rem 0;
        }
        .story-chip {
            background: #fffaf2;
            border: 1px solid #d6cfbf;
            border-radius: 18px;
            padding: 0.9rem 1rem;
        }
        .story-chip strong {
            color: #18230f;
            display: block;
            margin-bottom: 0.35rem;
        }
        .story-chip span {
            color: #5a6650;
            line-height: 1.5;
            font-size: 0.93rem;
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
        @media (max-width: 960px) {
            .hero-grid, .story-strip {
                grid-template-columns: 1fr;
            }
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


def impact_card(title: str, body: str) -> str:
    return f"""
    <div class="insight-card">
        <strong>{title}</strong><br><br>
        {body}
    </div>
    """


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
        <div class="hero-grid">
            <div class="hero-panel">
                <h4>Qué estoy tratando de responder</h4>
                <p>
                    Si el negocio ya vende, pero no captura todo el valor que podría, entonces el foco deja de ser
                    solo adquisición. La conversación pasa a calidad de ingresos, eficiencia comercial y retención.
                </p>
            </div>
            <div class="hero-panel">
                <h4>Lo que quiero que se vea aquí</h4>
                <ul>
                    <li>qué canal deja mejor negocio</li>
                    <li>dónde las devoluciones castigan el margen</li>
                    <li>qué clientes conviene proteger o reactivar</li>
                </ul>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="story-strip">
        <div class="story-chip">
            <strong>Problema</strong>
            <span>El volumen crece, pero no toda venta deja el mismo valor para el negocio.</span>
        </div>
        <div class="story-chip">
            <strong>Lectura</strong>
            <span>Canales, categorias y segmentos tienen pesos muy distintos en margen y recurrencia.</span>
        </div>
        <div class="story-chip">
            <strong>Riesgo</strong>
            <span>Seguir empujando ventas sin depurar mezcla comercial puede inflar ingreso y debilitar utilidad.</span>
        </div>
        <div class="story-chip">
            <strong>Decision</strong>
            <span>La mejor palanca no siempre es vender mas, sino vender mejor y retener con criterio.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Foco del dashboard")
    available_views = ["Resumen ejecutivo", "Canales y categorías", "Clientes y retención"]
    query_view = st.query_params.get("view", "Resumen ejecutivo")
    if query_view not in available_views:
        query_view = "Resumen ejecutivo"
    view = st.radio(
        "Selecciona la vista",
        available_views,
        index=available_views.index(query_view),
    )
    st.query_params["view"] = view
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

    st.markdown('<div class="section-title">Key takeaways</div>', unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    k1.markdown(
        f"""
        <div class="insight-card">
            <strong>Qué está pasando</strong><br><br>
            El negocio muestra un ingreso neto de <strong>{fmt_currency(summary['net_revenue'])}</strong> con una utilidad bruta de
            <strong>{fmt_currency(summary['gross_profit'])}</strong>. La lectura no es de crisis comercial, sino de
            eficiencia: hay crecimiento, pero parte del valor se erosiona por mezcla de canales, descuentos y devoluciones.
        </div>
        """,
        unsafe_allow_html=True,
    )
    k2.markdown(
        f"""
        <div class="insight-card">
            <strong>Qué merece atención inmediata</strong><br><br>
            La tasa de devoluciones de <strong>{fmt_pct(summary['return_rate_pct'])}</strong> y el desempeño desigual por canal
            sugieren que el siguiente salto no vendrá solo por invertir más, sino por depurar qué ventas realmente dejan margen
            y cuáles están generando costo operativo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)
    q1.markdown(
        """
        <div class="insight-card">
            <strong>Quick win</strong><br><br>
            Reasignar inversión hacia los canales con mejor equilibrio entre utilidad y ROAS puede generar mejora relativamente
            rápida sin necesidad de cambiar el modelo comercial completo.
        </div>
        """,
        unsafe_allow_html=True,
    )
    q2.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo principal</strong><br><br>
            Seguir premiando volumen sin revisar rentabilidad puede inflar ventas mientras deteriora margen y hace más cara la operación.
        </div>
        """,
        unsafe_allow_html=True,
    )
    q3.markdown(
        """
        <div class="insight-card">
            <strong>Decisión sugerida</strong><br><br>
            La prioridad ejecutiva debería ser ordenar el mix de canales y categorías antes de escalar presupuesto o descuentos.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendación ejecutiva</div>
            <div class="hero-text">
                La foto general del negocio sugiere una oportunidad clara de mejora en calidad de ingresos. La mejor lectura no es
                “vender más”, sino “vender mejor”: proteger canales con mejor utilidad, revisar categorías con alta fricción
                operativa y usar la retención como palanca de rentabilidad, no solo de volumen.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    estimated_margin_gain = summary["net_revenue"] * 0.02
    estimated_returns_recovery = summary["net_revenue"] * 0.015
    st.markdown('<div class="section-title">Impacto estimado</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    e1.markdown(
        impact_card(
            "Escenario 1: mejora de margen",
            f"Si una revision de mix comercial y descuentos ayudara a mejorar el margen bruto en 2 puntos sobre el ingreso actual, el negocio podria capturar alrededor de <strong>{fmt_currency(estimated_margin_gain)}</strong> adicionales."
        ),
        unsafe_allow_html=True,
    )
    e2.markdown(
        impact_card(
            "Escenario 2: menor friccion operativa",
            f"Si una parte de las devoluciones se redujera via mejoras en categorias criticas, la recuperacion potencial podria rondar <strong>{fmt_currency(estimated_returns_recovery)}</strong> entre ingreso preservado y menor presion operativa."
        ),
        unsafe_allow_html=True,
    )

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

    best_channel = channels_df.sort_values("gross_margin_pct", ascending=False).iloc[0]
    weakest_channel = channels_df.sort_values("gross_margin_pct", ascending=True).iloc[0]
    highest_return_category = categories_df.sort_values("return_rate_pct", ascending=False).iloc[0]
    highest_discount_category = categories_df.sort_values("avg_discount_rate_pct", ascending=False).iloc[0]

    st.markdown('<div class="section-title">Insights comerciales</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    i1.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 1: no todos los canales valen lo mismo</strong><br><br>
            <strong>{best_channel['acquisition_channel']}</strong> lidera en margen bruto con
            <strong>{fmt_pct(best_channel['gross_margin_pct'])}</strong>, mientras que
            <strong>{weakest_channel['acquisition_channel']}</strong> queda más expuesto en eficiencia.
            Esto sugiere que la mezcla de adquisición debe optimizarse con criterio de utilidad, no solo de volumen.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i2.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 2: las categorías también están presionando el negocio</strong><br><br>
            <strong>{highest_return_category['category']}</strong> registra la mayor tasa de devolución con
            <strong>{fmt_pct(highest_return_category['return_rate_pct'])}</strong>, y
            <strong>{highest_discount_category['category']}</strong> muestra el mayor descuento promedio.
            Cuando estas dos señales se combinan, suele haber destrucción de margen incluso si la categoría vende bien.
        </div>
        """,
        unsafe_allow_html=True,
    )

    i3, i4, i5 = st.columns(3)
    i3.markdown(
        """
        <div class="insight-card">
            <strong>Quick win</strong><br><br>
            Revisar el presupuesto del canal menos eficiente y mover una parte hacia canales con mejor ROAS y margen puede tener impacto rápido.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i4.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo operativo</strong><br><br>
            Categorías con devoluciones altas pueden esconder problemas de calidad, promesa comercial o experiencia postventa.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i5.markdown(
        """
        <div class="insight-card">
            <strong>Decisión sugerida</strong><br><br>
            Antes de escalar inversión, conviene definir un criterio de priorización que combine utilidad, ROAS, devolución y descuento.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendación ejecutiva</div>
            <div class="hero-text">
                La conversación comercial debería cambiar de “qué canal vende más” a “qué canal y qué categoría dejan mejor negocio”.
                La mejor decisión aquí es construir una gestión integrada de adquisición y rentabilidad, donde descuentos, devoluciones
                y margen sean parte del mismo tablero de control.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    spend_shift_impact = worst_channel["spend"] * 0.10 if "spend" in worst_channel else 0
    category_efficiency_impact = highest_return_category["net_revenue"] * 0.03
    st.markdown('<div class="section-title">Impacto estimado</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    p1.markdown(
        impact_card(
            "Escenario 1: reasignacion de inversion",
            f"Si el negocio moviera solo 10% del presupuesto del canal menos eficiente hacia canales con mejor retorno, ya habria espacio para reordenar aproximadamente <strong>{fmt_currency(spend_shift_impact)}</strong> con mejor criterio de rentabilidad."
        ),
        unsafe_allow_html=True,
    )
    p2.markdown(
        impact_card(
            "Escenario 2: correccion en categoria critica",
            f"Si se atacara la categoria con mayor devolucion y se mejorara su eficiencia en torno a 3% de su ingreso neto, el impacto defensivo podria acercarse a <strong>{fmt_currency(category_efficiency_impact)}</strong>."
        ),
        unsafe_allow_html=True,
    )

if view == "Clientes y retención":
    st.markdown('<div class="section-title">Segmentación y retención</div>', unsafe_allow_html=True)
    segment_mix = (
        rfm_df["segment"]
        .value_counts()
        .rename_axis("segment")
        .reset_index(name="customers")
    )
    segment_summary = (
        rfm_df.groupby("segment", as_index=False)
        .agg(
            customers=("customer_id", "count"),
            avg_monetary=("monetary", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_recency=("recency", "mean"),
        )
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
    potential = int((rfm_df["segment"] == "Potential Loyalist").sum())

    champions_row = segment_summary[segment_summary["segment"] == "Champions"].iloc[0]
    at_risk_row = segment_summary[segment_summary["segment"] == "At Risk"].iloc[0]
    loyal_row = segment_summary[segment_summary["segment"] == "Loyal"].iloc[0]
    potential_row = segment_summary[segment_summary["segment"] == "Potential Loyalist"].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes Champions", f"{champions:,}")
    c2.metric("Clientes Loyal", f"{loyal:,}")
    c3.metric("Clientes At Risk", f"{at_risk:,}")

    st.markdown('<div class="section-title">Insights y recomendaciones</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    i1.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 1: el valor está concentrado en los segmentos altos</strong><br><br>
            Los clientes <strong>Champions</strong> tienen un valor monetario promedio de
            <strong>{fmt_currency(champions_row['avg_monetary'])}</strong> y una frecuencia media de
            <strong>{champions_row['avg_frequency']:.1f}</strong> compras. Este grupo debería protegerse con
            beneficios de fidelización, acceso anticipado o campañas de cross-sell, porque perderlos tendría un impacto
            desproporcionado en ingreso y recurrencia.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i2.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 2: hay una bolsa relevante de clientes en riesgo</strong><br><br>
            El segmento <strong>At Risk</strong> reúne <strong>{at_risk:,}</strong> clientes con una recencia promedio de
            <strong>{at_risk_row['avg_recency']:.0f}</strong> días. No todos justifican el mismo esfuerzo, así que la
            recomendación es reactivar primero a quienes todavía muestran valor histórico razonable y evitar campañas masivas
            sobre clientes de baja contribución.
        </div>
        """,
        unsafe_allow_html=True,
    )

    i3, i4 = st.columns(2)
    i3.markdown(
        f"""
        <div class="insight-card">
            <strong>Oportunidad 1: convertir potenciales en clientes leales</strong><br><br>
            Hay <strong>{potential:,}</strong> clientes en <strong>Potential Loyalist</strong>. Este grupo suele ser el más rentable
            para trabajar porque todavía no está perdido y ya mostró señales de interés. Aquí sirven campañas de segunda y tercera compra,
            bundles, recomendaciones personalizadas y recordatorios post-compra.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i4.markdown(
        f"""
        <div class="insight-card">
            <strong>Oportunidad 2: fidelizar sin sobreinvertir</strong><br><br>
            El segmento <strong>Loyal</strong> ya muestra una frecuencia media de <strong>{loyal_row['avg_frequency']:.1f}</strong> compras.
            En vez de empujar descuentos agresivos, la mejor estrategia suele ser aumentar ticket y recompra con beneficios no monetarios,
            programas VIP o promociones exclusivas por categoría.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendación ejecutiva</div>
            <div class="hero-text">
                La estrategia de retención no debería ejecutarse de forma uniforme. Una versión más madura sería dividir la inversión en tres frentes:
                <strong>proteger Champions</strong>, <strong>escalar Potential Loyalists</strong> y <strong>reactivar At Risk con criterios de valor</strong>.
                Con esta lógica, el negocio evita gastar de más en segmentos de baja probabilidad de retorno y concentra esfuerzo donde la mejora en ingreso
                incremental es más defendible.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    p1, p2, p3 = st.columns(3)
    p1.markdown(
        """
        <div class="insight-card">
            <strong>Quick win</strong><br><br>
            Activar journeys de segunda y tercera compra sobre clientes con señal de potencial puede mejorar retención sin elevar demasiado CAC.
        </div>
        """,
        unsafe_allow_html=True,
    )
    p2.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo principal</strong><br><br>
            Tratar a toda la base de clientes igual genera desperdicio comercial y normalmente termina sobreincentivando a quienes menos lo necesitan.
        </div>
        """,
        unsafe_allow_html=True,
    )
    p3.markdown(
        """
        <div class="insight-card">
            <strong>Decisión sugerida</strong><br><br>
            La retención debería medirse por uplift incremental por segmento, no solo por aperturas, clics o volumen de campaña.
        </div>
        """,
        unsafe_allow_html=True,
    )

    protected_champions_impact = champions_row["avg_monetary"] * max(champions * 0.05, 1)
    recovered_at_risk_impact = at_risk_row["avg_monetary"] * max(at_risk * 0.03, 1)
    st.markdown('<div class="section-title">Impacto estimado</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    r1.markdown(
        impact_card(
            "Escenario 1: proteger clientes top",
            f"Si una estrategia de fidelizacion evitara la perdida de solo 5% de los clientes Champions, el ingreso protegido podria rondar <strong>{fmt_currency(protected_champions_impact)}</strong>."
        ),
        unsafe_allow_html=True,
    )
    r2.markdown(
        impact_card(
            "Escenario 2: reactivar parte del riesgo",
            f"Si una campaña bien segmentada lograra recuperar 3% del valor potencial de clientes At Risk, el efecto estimado podria estar cerca de <strong>{fmt_currency(recovered_at_risk_impact)}</strong>."
        ),
        unsafe_allow_html=True,
    )
