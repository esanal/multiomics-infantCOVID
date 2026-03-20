# infantCOVID

This repository analyzes the GEO series `GSE239799`:

Wimmers F, Burrell AR, Feng Y, Zheng H et al. *Multi-omics analysis of mucosal and systemic immunity to SARS-CoV-2 after birth*. Cell. 2023 Oct 12;186(21):4632-4651.e23. PMID: 37776858.

The data used here are supplementary single-cell RNA-seq and ATAC-seq files downloaded from GEO and processed into per-sample MOFA models.

## Repository structure

- `1.downloadData.py`: downloads the `GSE239799` GEO record and sample supplementary files into `data/`.
- `2.process.ipynb`: preprocesses RNA-seq and ATAC-seq data and trains MOFA models for the selected samples.
- `3.downstream.ipynb`: loads metadata and MOFA outputs for exploratory downstream analysis.
- `requirements.txt`: Python dependencies used by the script and notebooks.
