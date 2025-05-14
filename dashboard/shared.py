from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
dph = pd.read_csv(app_dir / "DPH.csv")
bacp = pd.read_csv(app_dir / "BACP.csv")

dfs = {"None": "None", "Public Health Department": dph, "Business Affairs and Consumer Protection Department": bacp}

agency_status = pd.read_csv(app_dir / "agency_status.csv")