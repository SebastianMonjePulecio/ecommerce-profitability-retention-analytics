from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "outputs" / "tables"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"
TEMPLATES_DIR = BASE_DIR / "templates"


app = FastAPI(
    title="API de Analitica E-commerce",
    description="Expone los principales resultados del proyecto de rentabilidad y retencion en e-commerce.",
    version="1.0.0",
)
app.mount("/charts", StaticFiles(directory=CHARTS_DIR), name="charts")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def load_table(filename: str) -> pd.DataFrame:
    path = TABLES_DIR / filename
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                f"No se encontro {filename}. Ejecuta primero "
                "src/generate_sample_data.py y src/analyze_ecommerce.py."
            ),
        )
    return pd.read_csv(path)


@app.get("/")
def home(request: Request):
    summary_df = load_table("executive_summary.csv")
    channel_df = load_table("channel_performance.csv")
    category_df = load_table("category_performance.csv")
    rfm_df = load_table("rfm_segments.csv")

    summary = dict(zip(summary_df["metric"], summary_df["value"]))
    top_channel = channel_df.sort_values("gross_profit", ascending=False).iloc[0].to_dict()
    top_category_risk = category_df.sort_values("return_rate_pct", ascending=False).iloc[0].to_dict()
    worst_roas_channel = channel_df.sort_values("roas", ascending=True).iloc[0].to_dict()
    best_margin_category = category_df.sort_values("gross_margin_pct", ascending=False).iloc[0].to_dict()
    segment_mix = (
        rfm_df["segment"]
        .value_counts()
        .rename_axis("segment")
        .reset_index(name="customers")
        .sort_values("customers", ascending=False)
        .to_dict(orient="records")
    )

    context = {
        "request": request,
        "summary": summary,
        "top_channel": top_channel,
        "top_category_risk": top_category_risk,
        "worst_roas_channel": worst_roas_channel,
        "best_margin_category": best_margin_category,
        "top_channels": channel_df.sort_values("gross_profit", ascending=False).head(5).to_dict(orient="records"),
        "category_table": category_df.sort_values("return_rate_pct", ascending=False).to_dict(orient="records"),
        "segment_mix": segment_mix,
        "charts": [
            "gross_profit_by_channel.png",
            "return_rate_by_category.png",
            "monthly_net_revenue.png",
        ],
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/summary")
def api_summary():
    df = load_table("executive_summary.csv")
    return df.to_dict(orient="records")


@app.get("/api/channels")
def api_channels():
    df = load_table("channel_performance.csv")
    return df.to_dict(orient="records")


@app.get("/api/categories")
def api_categories():
    df = load_table("category_performance.csv")
    return df.to_dict(orient="records")


@app.get("/api/rfm")
def api_rfm():
    df = load_table("rfm_segments.csv")
    return df.to_dict(orient="records")


@app.get("/download/{filename}")
def download_file(filename: str):
    path = TABLES_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")
    return FileResponse(path)
