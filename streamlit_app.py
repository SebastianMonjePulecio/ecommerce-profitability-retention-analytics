from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
TABLES_DIR = BASE_DIR / "outputs" / "tables"


st.set_page_config(
    page_title="Dashboard Ejecutivo E-commerce",
    page_icon="chart",
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
            f"No se encontro {filename}. Ejecuta primero `python src/generate_sample_data.py` y `python src/analyze_ecommerce.py`."
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
        <div class="hero-title">Rentabilidad y retencion en e-commerce</div>
        <div class="hero-text">
            La idea de este dashboard es aterrizar una pregunta bastante simple: si el negocio ya vende,
            entonces donde se esta quedando corto en valor, margen y recurrencia? Mas que mostrar numeros,
            busque que la lectura ayude a priorizar mejor.
        </div>
        <div class="hero-grid">
            <div class="hero-panel">
                <h4>Que estoy tratando de entender</h4>
                <p>
                    Cuando una empresa ya tiene traccion, el reto deja de ser solo vender mas. Empieza a importar
                    mucho mas que ventas dejan margen, que categorias generan ruido y que clientes realmente vale la pena retener.
                </p>
            </div>
            <div class="hero-panel">
                <h4>Que me gustaria que se vea rapido</h4>
                <ul>
                    <li>que canal esta dejando mejor negocio</li>
                    <li>donde las devoluciones estan pegando mas fuerte</li>
                    <li>que clientes conviene proteger y cuales reactivar</li>
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
            <span>El volumen puede crecer, pero eso no significa que el negocio este creciendo mejor.</span>
        </div>
        <div class="story-chip">
            <strong>Lectura</strong>
            <span>Canales, categorias y segmentos aportan valor muy distinto en margen, retorno y recurrencia.</span>
        </div>
        <div class="story-chip">
            <strong>Riesgo</strong>
            <span>Empujar ventas sin revisar mezcla comercial puede inflar ingreso y debilitar utilidad.</span>
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
    st.markdown("## Como navegar esto")
    available_views = ["Resumen ejecutivo", "Canales y categorias", "Clientes y retencion"]
    query_view = st.query_params.get("view", "Resumen ejecutivo")
    if query_view not in available_views:
        query_view = "Resumen ejecutivo"
    view = st.radio(
        "Selecciona la vista",
        available_views,
        index=available_views.index(query_view),
    )
    st.query_params["view"] = view
    st.markdown("## Donde miraria primero")
    st.markdown(f"**Canal que mejor esta respondiendo**  \n{top_channel['acquisition_channel']}")
    st.markdown(f"**Canal que revisaria ya**  \n{worst_channel['acquisition_channel']}")
    st.markdown(f"**Categoria con mas friccion**  \n{top_category['category']}")
    st.markdown("**Segmento que conviene cuidar**  \nChampions")
    st.markdown("**Siguiente movimiento**  \nOrdenar el mix comercial y la retencion antes de meter mas presupuesto.")


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
    st.markdown('<div class="section-title">Lo mas importante</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.markdown(
        f"""
        <div class="insight-card">
            <strong>Canal mas rentable</strong><br><br>
            {top_channel['acquisition_channel']} lidera en utilidad bruta con {fmt_currency(top_channel['gross_profit'])}.
            Eso refuerza una idea simple: no todo crecimiento vale lo mismo cuando lo miras desde utilidad.
        </div>
        """,
        unsafe_allow_html=True,
    )
    b.markdown(
        f"""
        <div class="insight-card">
            <strong>Canal con peor eficiencia</strong><br><br>
            {worst_channel['acquisition_channel']} muestra el ROAS mas bajo con {worst_channel['roas']:.2f},
            asi que ahi es donde primero revisaria inversion, descuento y expectativa de retorno.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c.markdown(
        f"""
        <div class="insight-card">
            <strong>Mayor alerta operativa</strong><br><br>
            {top_category['category']} tiene la tasa de devolucion mas alta con {fmt_pct(top_category['return_rate_pct'])}.
            Ahi puede estar escondido un problema de producto, surtido o experiencia que vale la pena mirar de cerca.
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
        title="Tasa de devolucion por categoria",
        paper_bgcolor="#fffaf2",
        plot_bgcolor="#fffaf2",
        font=dict(color="#18230F", family="Georgia"),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(return_chart, use_container_width=True)

    st.markdown('<div class="section-title">Que me deja esta vista</div>', unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    k1.markdown(
        f"""
        <div class="insight-card">
            <strong>Que esta pasando</strong><br><br>
            El negocio muestra un ingreso neto de <strong>{fmt_currency(summary['net_revenue'])}</strong> con una utilidad bruta de
            <strong>{fmt_currency(summary['gross_profit'])}</strong>. No parece un problema de demanda, sino mas bien de
            eficiencia: el negocio vende, pero una parte del valor se pierde por mezcla de canales, descuentos y devoluciones.
        </div>
        """,
        unsafe_allow_html=True,
    )
    k2.markdown(
        f"""
        <div class="insight-card">
            <strong>Que merece atencion inmediata</strong><br><br>
            La tasa de devoluciones de <strong>{fmt_pct(summary['return_rate_pct'])}</strong> y el desempeno desigual por canal
            me hacen pensar que el siguiente salto no va a venir solo por invertir mas, sino por depurar que ventas realmente dejan margen
            y cuales terminan costando demasiado.
        </div>
        """,
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)
    q1.markdown(
        """
        <div class="insight-card">
            <strong>Quick win</strong><br><br>
            Mover algo de inversion hacia los canales con mejor equilibrio entre utilidad y ROAS podria generar mejora relativamente rapida
            sin tener que redisenar todo el modelo comercial.
        </div>
        """,
        unsafe_allow_html=True,
    )
    q2.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo principal</strong><br><br>
            Seguir premiando volumen sin revisar rentabilidad puede hacer que las ventas se vean bien arriba, mientras abajo el margen se sigue debilitando.
        </div>
        """,
        unsafe_allow_html=True,
    )
    q3.markdown(
        """
        <div class="insight-card">
            <strong>Decision sugerida</strong><br><br>
            Yo pondria la prioridad en ordenar el mix de canales y categorias antes de escalar presupuesto o descuentos.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendacion ejecutiva</div>
            <div class="hero-text">
                La lectura mas util aqui no es "hay que vender mas", sino "hay que vender mejor". Antes de buscar mas volumen,
                tiene mas sentido proteger los canales que ya estan dejando buena utilidad, revisar las categorias con mas friccion
                y usar retencion como palanca de rentabilidad, no solo de volumen.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    estimated_margin_gain = summary["net_revenue"] * 0.02
    estimated_returns_recovery = summary["net_revenue"] * 0.015
    st.markdown('<div class="section-title">Que podria mover esto</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    e1.markdown(
        impact_card(
            "Escenario 1: mejora de margen",
            f"Si una revision de mix comercial y descuentos ayudara a mejorar el margen bruto en 2 puntos sobre el ingreso actual, el negocio podria capturar alrededor de <strong>{fmt_currency(estimated_margin_gain)}</strong> adicionales. No lo leeria como promesa exacta, sino como una senal del orden de magnitud."
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

if view == "Canales y categorias":
    st.markdown('<div class="section-title">Donde se gana y donde se pierde</div>', unsafe_allow_html=True)
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
        title="Descuento promedio por categoria",
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

    st.markdown('<div class="section-title">Que me dice esta mezcla comercial</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    i1.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 1: no todos los canales valen lo mismo</strong><br><br>
            <strong>{best_channel['acquisition_channel']}</strong> lidera en margen bruto con
            <strong>{fmt_pct(best_channel['gross_margin_pct'])}</strong>, mientras que
            <strong>{weakest_channel['acquisition_channel']}</strong> queda mas expuesto en eficiencia.
            Para mi eso deja una idea clara: la mezcla de adquisicion deberia optimizarse con criterio de utilidad, no solo de volumen.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i2.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 2: las categorias tambien estan presionando el negocio</strong><br><br>
            <strong>{highest_return_category['category']}</strong> registra la mayor tasa de devolucion con
            <strong>{fmt_pct(highest_return_category['return_rate_pct'])}</strong>, y
            <strong>{highest_discount_category['category']}</strong> muestra el mayor descuento promedio.
            Cuando esas dos senales se cruzan, normalmente hay destruccion de margen incluso si la categoria parece buena en ventas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    i3, i4, i5 = st.columns(3)
    i3.markdown(
        """
        <div class="insight-card">
            <strong>Quick win</strong><br><br>
            Revisar el presupuesto del canal menos eficiente y mover una parte hacia canales con mejor ROAS y margen puede tener efecto relativamente rapido.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i4.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo operativo</strong><br><br>
            Categorias con devoluciones altas suelen esconder problemas de calidad, promesa comercial o experiencia postventa.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i5.markdown(
        """
        <div class="insight-card">
            <strong>Decision sugerida</strong><br><br>
            Antes de escalar inversion, yo dejaria claro un criterio de priorizacion que combine utilidad, ROAS, devolucion y descuento.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendacion ejecutiva</div>
            <div class="hero-text">
                La conversacion comercial cambiaria bastante si en vez de preguntar "que canal vende mas" empezaramos a preguntar
                "que canal y que categoria dejan mejor negocio". Ahi es donde descuentos, devoluciones y margen dejan de verse por separado
                y pasan a formar parte de la misma decision.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    spend_shift_impact = worst_channel["spend"] * 0.10 if "spend" in worst_channel else 0
    category_efficiency_impact = highest_return_category["net_revenue"] * 0.03
    st.markdown('<div class="section-title">Que podria cambiar si se actua aqui</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    p1.markdown(
        impact_card(
            "Escenario 1: reasignacion de inversion",
            f"Si el negocio moviera solo 10% del presupuesto del canal menos eficiente hacia canales con mejor retorno, ya habria espacio para reordenar aproximadamente <strong>{fmt_currency(spend_shift_impact)}</strong> con un criterio mas sano de rentabilidad."
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

if view == "Clientes y retencion":
    st.markdown('<div class="section-title">Que clientes cuidaria distinto</div>', unsafe_allow_html=True)
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

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes Champions", f"{champions:,}")
    c2.metric("Clientes Loyal", f"{loyal:,}")
    c3.metric("Clientes At Risk", f"{at_risk:,}")

    st.markdown('<div class="section-title">Lo que me deja esta segmentacion</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    i1.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 1: el valor esta concentrado en los segmentos altos</strong><br><br>
            Los clientes <strong>Champions</strong> tienen un valor monetario promedio de
            <strong>{fmt_currency(champions_row['avg_monetary'])}</strong> y una frecuencia media de
            <strong>{champions_row['avg_frequency']:.1f}</strong> compras. Este grupo deberia protegerse con
            beneficios de fidelizacion, acceso anticipado o campanas de cross-sell, porque perderlos pesaria mucho mas de lo que parece.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i2.markdown(
        f"""
        <div class="insight-card">
            <strong>Hallazgo 2: hay una bolsa relevante de clientes en riesgo</strong><br><br>
            El segmento <strong>At Risk</strong> reune <strong>{at_risk:,}</strong> clientes con una recencia promedio de
            <strong>{at_risk_row['avg_recency']:.0f}</strong> dias. No todos justifican el mismo esfuerzo, asi que la
            recomendacion mas sana seria reactivar primero a quienes todavia muestran valor historico razonable y no gastar igual en toda la base.
        </div>
        """,
        unsafe_allow_html=True,
    )

    i3, i4 = st.columns(2)
    i3.markdown(
        f"""
        <div class="insight-card">
            <strong>Oportunidad 1: convertir potenciales en clientes leales</strong><br><br>
            Hay <strong>{potential:,}</strong> clientes en <strong>Potential Loyalist</strong>. Este grupo suele ser el mas rentable
            para trabajar porque todavia no esta perdido y ya mostro senales de interes. Aqui si hacen sentido campanas de segunda y tercera compra,
            bundles o recomendaciones mas personalizadas.
        </div>
        """,
        unsafe_allow_html=True,
    )
    i4.markdown(
        f"""
        <div class="insight-card">
            <strong>Oportunidad 2: fidelizar sin sobreinvertir</strong><br><br>
            El segmento <strong>Loyal</strong> ya muestra una frecuencia media de <strong>{loyal_row['avg_frequency']:.1f}</strong> compras.
            En vez de empujar descuentos agresivos, aqui me parece mas sensato buscar ticket y recompra con beneficios no monetarios,
            programas VIP o promociones mas selectivas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="hero-card" style="margin-top: 1rem;">
            <div class="section-title">Recomendacion ejecutiva</div>
            <div class="hero-text">
                La retencion rara vez funciona bien cuando se hace igual para todos. Una version mas madura seria dividir el esfuerzo en tres frentes:
                <strong>proteger Champions</strong>, <strong>escalar Potential Loyalists</strong> y <strong>reactivar At Risk con criterio de valor</strong>.
                Asi se evita gastar de mas donde el retorno es dudoso y se concentra energia donde el ingreso incremental tiene mas sentido.
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
            Activar journeys de segunda y tercera compra sobre clientes con senal de potencial puede mejorar retencion sin subir demasiado el CAC.
        </div>
        """,
        unsafe_allow_html=True,
    )
    p2.markdown(
        """
        <div class="insight-card">
            <strong>Riesgo principal</strong><br><br>
            Tratar a toda la base igual genera desperdicio comercial y muchas veces termina sobreincentivando justo a quienes menos lo necesitan.
        </div>
        """,
        unsafe_allow_html=True,
    )
    p3.markdown(
        """
        <div class="insight-card">
            <strong>Decision sugerida</strong><br><br>
            Yo mediria retencion por uplift incremental por segmento, no solo por aperturas, clics o volumen de campana.
        </div>
        """,
        unsafe_allow_html=True,
    )

    protected_champions_impact = champions_row["avg_monetary"] * max(champions * 0.05, 1)
    recovered_at_risk_impact = at_risk_row["avg_monetary"] * max(at_risk * 0.03, 1)
    st.markdown('<div class="section-title">Que podria mover una mejor retencion</div>', unsafe_allow_html=True)
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
            f"Si una campana bien segmentada lograra recuperar 3% del valor potencial de clientes At Risk, el efecto estimado podria estar cerca de <strong>{fmt_currency(recovered_at_risk_impact)}</strong>. Otra vez, mas como referencia util que como promesa exacta."
        ),
        unsafe_allow_html=True,
    )
