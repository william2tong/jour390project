from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
dph = pd.read_csv(app_dir / "DPH.csv")
bacp = pd.read_csv(app_dir / "BACP.csv")
dof = pd.read_csv(app_dir / "DOF.csv")
dps = pd.read_csv(app_dir / "DPS.csv")
case = pd.read_csv(app_dir / "CASE.csv")

dfs = {"None": "None", "Public Health Department": dph, "Business Affairs and Consumer Protection Department": bacp, "Finance Department": dof, "Procurement Services Department": dps, "Cultural Affairs and Special Events Department": case}

agency_status = pd.read_csv(app_dir / "AgencyStatus.csv")