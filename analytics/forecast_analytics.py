from .db_utils import execute_query
import pandas as pd


class ForecastAnalytics:
    """Forecasting revenue menggunakan SARIMA."""

    # -------------------------------------------------------
    # Get historical monthly revenue
    # -------------------------------------------------------

    def _get_monthly_data(self, province: str = None) -> pd.DataFrame:
        """Ambil data revenue bulanan untuk training."""
        from .product_analytics import _build_filters

        filters, params = _build_filters(province=province)

        sql = f"""
            SELECT
                d.year,
                d.month,
                d.month_name,
                SUM(f.revenue) AS total_revenue
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY d.year, d.month, d.month_name
            ORDER BY d.year, d.month
        """
        result = execute_query(sql, tuple(params))
        if result["status"] != "success" or not result["data"]:
            return pd.DataFrame()

        df = pd.DataFrame(result["data"])
        df["total_revenue"] = pd.to_numeric(df["total_revenue"])
        df["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"
        )
        df = df.sort_values("date").reset_index(drop=True)
        return df

    # -------------------------------------------------------
    # SARIMA forecast
    # -------------------------------------------------------

    def forecast_next_months(
        self,
        n_months: int = 3,
        province: str = None
    ) -> dict:
        """
        Forecast revenue n bulan ke depan menggunakan SARIMA.

        Returns dict dengan keys:
        - forecasts: list of {month_name, year, predicted_revenue, lower, upper}
        - model_info: string info model
        - status: 'success' | 'error'
        """
        try:
            from statsmodels.tsa.statespace.sarimax import SARIMAX
            import warnings
            warnings.filterwarnings("ignore")

            df = self._get_monthly_data(province=province)

            if df.empty or len(df) < 12:
                return {
                    "status": "error",
                    "message": "Data tidak cukup untuk forecasting (minimum 12 bulan)",
                    "forecasts": []
                }

            # Set datetime index
            ts = df.set_index("date")["total_revenue"]
            ts.index = pd.DatetimeIndex(ts.index).to_period("M")

            # SARIMA(1,1,1)(1,1,0,12) — cocok untuk data retail bulanan
            model = SARIMAX(
                ts,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 0, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            fit = model.fit(disp=False)

            # Forecast
            forecast = fit.get_forecast(steps=n_months)
            mean = forecast.predicted_mean
            ci   = forecast.conf_int(alpha=0.2)  # 80% confidence interval

            month_names_id = {
                1: "Januari", 2: "Februari", 3: "Maret",
                4: "April",   5: "Mei",      6: "Juni",
                7: "Juli",    8: "Agustus",  9: "September",
                10: "Oktober",11: "November",12: "Desember"
            }

            forecasts = []
            for period, pred in mean.items():
                mo = period.month
                yr = period.year
                lo = float(ci.loc[period].iloc[0])
                hi = float(ci.loc[period].iloc[1])

                forecasts.append({
                    "month":            mo,
                    "year":             yr,
                    "month_name":       month_names_id.get(mo, str(mo)),
                    "predicted_revenue": max(0, float(pred)),
                    "lower":            max(0, lo),
                    "upper":            max(0, hi),
                    "label":            f"{month_names_id.get(mo, str(mo))} {yr}"
                })

            return {
                "status":     "success",
                "forecasts":  forecasts,
                "model_info": f"SARIMA(1,1,1)(1,1,0,12) · {len(df)} bulan data training",
                "aic":        round(fit.aic, 2)
            }

        except ImportError:
            return {
                "status": "error",
                "message": "statsmodels tidak terinstall. Jalankan: pip install statsmodels",
                "forecasts": []
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "forecasts": []
            }

    # -------------------------------------------------------
    # Simple trend forecast (fallback)
    # -------------------------------------------------------

    def forecast_simple(self, n_months: int = 3, province: str = None) -> dict:
        """Linear regression fallback kalau SARIMA gagal."""
        try:
            from sklearn.linear_model import LinearRegression
            import numpy as np

            df = self._get_monthly_data(province=province)
            if df.empty or len(df) < 6:
                return {"status": "error", "forecasts": []}

            X = np.arange(len(df)).reshape(-1, 1)
            y = df["total_revenue"].values

            model = LinearRegression()
            model.fit(X, y)

            month_names_id = {
                1: "Januari", 2: "Februari", 3: "Maret",
                4: "April",   5: "Mei",      6: "Juni",
                7: "Juli",    8: "Agustus",  9: "September",
                10: "Oktober",11: "November",12: "Desember"
            }

            last_date = df["date"].iloc[-1]
            forecasts = []
            for i in range(1, n_months + 1):
                next_date = last_date + pd.DateOffset(months=i)
                pred = float(model.predict([[len(df) + i - 1]])[0])
                mo, yr = next_date.month, next_date.year
                forecasts.append({
                    "month":             mo,
                    "year":              yr,
                    "month_name":        month_names_id.get(mo, str(mo)),
                    "predicted_revenue": max(0, pred),
                    "lower":             max(0, pred * 0.85),
                    "upper":             pred * 1.15,
                    "label":             f"{month_names_id.get(mo, str(mo))} {yr}"
                })

            return {
                "status":     "success",
                "forecasts":  forecasts,
                "model_info": "Linear Regression (fallback)"
            }
        except Exception as e:
            return {"status": "error", "message": str(e), "forecasts": []}