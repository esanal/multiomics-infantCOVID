'''
Downloads multi omics data from:
Multi-omics analysis of mucosal and systemic immunity to SARS-CoV-2 after birth. Cell 2023 Oct 12;186(21):4632-4651.e23. PMID: 37776858
'''

from pathlib import Path
from urllib.parse import unquote, urlparse

import GEOparse

data_dir = Path("./data")
data_dir.mkdir(parents=True, exist_ok=True)

gse = GEOparse.get_GEO(geo="GSE239799", destdir=str(data_dir))

print(gse.phenotype_data.columns)


def supplementary_urls(gsm):
    urls = []
    for key, values in gsm.metadata.items():
        if not key.startswith("supplementary_file"):
            continue
        if not isinstance(values, list):
            values = [values]
        for value in values:
            url = str(value).strip()
            if not url or url.lower() in {"none", "n/a", "na"}:
                continue
            urls.append(url)
    return urls


def filename_from_url(url):
    parsed = urlparse(url)
    return Path(unquote(parsed.path)).name


for sample in gse.phenotype_data.geo_accession:
    print(sample)
    gsm = gse.gsms[sample]
    urls = supplementary_urls(gsm)
    expected_names = [name for name in (filename_from_url(u) for u in urls) if name]

    if expected_names and all((data_dir / name).exists() for name in expected_names):
        print(f"Skipping {sample}: all supplementary files already downloaded")
        continue

    if not urls:
        print(f"Skipping {sample}: no supplementary_file entries in GEO record")
        continue

    print(gsm.download_supplementary_files(directory=str(data_dir)))
