from fastapi import APIRouter
from sqlalchemy import text
import pandas as pd
from db.database import SessionLocal

api_router = APIRouter(prefix="/api/v0")

# AR6 GWP
ch4_GWP_100yr = 29.8
ch4_GWP_20yr = 82.5
n2o_GWP_100yr = 273
n2o_GWP_20yr = 273

# GPC quality classification
gpc_quality_data = "TBD"
gpc_quality_EF = "TBD"


# Extract the data by locode, year and sector/subsector
def db_query(locode, year, reference_number):
    with SessionLocal() as session:
        query = text(
            """
            SELECT
                cco.cell_id,
                cg.area,
                cco.fraction_in_city,
                gce.emissions_quantity,
                gce.gas,
                gce.year,
                gce.reference_number
            FROM
                "CityCellOverlapEdgar" cco
            JOIN
                "GridCellEdgar" cg ON cco.cell_id = cg.id
            JOIN
                "GridCellEmissionsEdgar" gce ON cco.cell_id = gce.cell_id
            WHERE cco.locode = :locode
            AND gce.reference_number = :reference_number
            AND gce.year = :year;"""
        )

        params = {"locode": locode, "year": year, "reference_number": reference_number}
        result = session.execute(query, params).fetchall()

    return result


@api_router.get("/edgar/city/{locode}/{year}/{gpcReferenceNumber}")
def get_emissions_by_city_and_year(locode: str, year: int, gpcReferenceNumber: str):
    records = db_query(locode, year, gpcReferenceNumber)
    series = (
        pd.DataFrame(records)
        .assign(
            emissions_total=lambda row: row["area"]
            * row["fraction_in_city"]
            * row["emissions_quantity"]
        )
        .groupby("gas")
        .sum("emissions_total")
        .astype({"emissions_total": int})
        .loc[:, ["emissions_total"]]
        .squeeze()
    )

    totals = {
        "totals": {
            "emissions": {
                "co2_mass": str(series.get("CO2", 0)),
                "co2_co2eq": str(series.get("CO2", 0)),
                "ch4_mass": str(series.get("CH4", 0)),
                "ch4_co2eq_100yr": str(series.get("CH4", 0) * ch4_GWP_100yr),
                "ch4_co2eq_20yr": str(series.get("CH4", 0) * ch4_GWP_20yr),
                "n2o_mass": str(series.get("N2O", 0)),
                "n2o_co2eq_100yr": str(series.get("N2O", 0) * n2o_GWP_100yr),
                "n2o_co2eq_20yr": str(series.get("N2O", 0) * n2o_GWP_20yr),
                "gpc_quality": str(gpc_quality_data),
            }
        }
    }

    return totals