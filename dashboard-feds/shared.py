from pathlib import Path
import json

import pandas as pd

app_dir = Path(__file__).parent
tips = pd.read_csv(app_dir / "tips.csv")

foia_df = pd.read_csv(app_dir / "feds.csv")

foia_collapsed_df = pd.read_csv(app_dir / "feds_collapsed.csv")

agency_abbreviations_raw = open(app_dir / '0agencies.json', 'r')
agency_abbreviations = json.load(agency_abbreviations_raw)

agency_abbreviations_reverse_raw = open(app_dir / '0agencies_reversed.json', 'r')
agency_abbreviations_reverse = json.load(agency_abbreviations_reverse_raw)