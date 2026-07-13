"""Download the selected BLS Average Price series from FRED's public CSV mirror."""

from pathlib import Path
from urllib.request import urlretrieve


SERIES_IDS = (
    "APU0000701312",
    "APU0000701111",
    "APU0000701322",
    "APU0000702111",
    "APU0000702212",
    "APU0000703112",
    "APU0000704111",
    "APU0000706111",
    "APU0000FF1101",
    "APU0000708111",
    "APU0000709112",
    "APU0000710212",
    "APU0000711211",
    "APU0000711311",
    "APU0000712211",
    "APU0000712112",
    "APU0000712311",
    "APU0000714233",
)
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "fred"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for series_id in SERIES_IDS:
        destination = RAW_DIR / f"{series_id}.csv"
        urlretrieve(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}", destination)
        print(f"Downloaded {series_id} to {destination}")


if __name__ == "__main__":
    main()
