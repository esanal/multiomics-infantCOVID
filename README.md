# infantCOVID

Analysis workflow for the GEO series `GSE239799` from:

Wimmers F, Burrell AR, Feng Y, Zheng H et al. *Multi-omics analysis of mucosal and systemic immunity to SARS-CoV-2 after birth*. Cell. 2023 Oct 12;186(21):4632-4651.e23. PMID: 37776858.

This repository currently contains a minimal end-to-end pipeline to:

1. download the supplementary multi-omics data from GEO,
2. preprocess RNA-seq and ATAC-seq data for a small subset of samples,
3. train per-sample MOFA models, and
4. inspect factors in a downstream notebook.

The code is exploratory rather than packaged. The workflow is driven by one Python script and two notebooks.

## Repository layout

- `1.downloadData.py`: downloads GEO metadata and supplementary sample files into `./data`.
- `2.process.ipynb`: preprocesses RNA and ATAC modalities, writes per-sample `h5ad` files, and fits MOFA models.
- `3.downstream.ipynb`: loads metadata and MOFA outputs for exploratory downstream analysis.

## Data source

- GEO accession: `GSE239799`
- Study title: *Multi-omics analysis of mucosal and systemic immunity to SARS-CoV-2 after birth*

`1.downloadData.py` uses `GEOparse` to fetch the GEO record and download all sample-level supplementary files referenced in each GSM entry.

## Current workflow

### 1. Download data

Run:

```bash
python3 1.downloadData.py
```

This script:

- creates `./data` if needed,
- downloads the `GSE239799` series metadata,
- iterates through each GSM sample,
- collects `supplementary_file*` URLs from the GEO metadata,
- skips files that already exist locally,
- downloads missing supplementary files into `./data`.

### 2. Process RNA and ATAC data

Open `2.process.ipynb` and run the cells in order.

The notebook currently focuses on the first three matched RNA/ATAC sample directories found under `./data`, representing three timepoints for one individual (`pre`, `acute`, and `post/convalescent`, as described in the notebook text).

Main processing steps:

- query BioMart annotations to map Ensembl IDs and gene symbols,
- locate RNA directories matching `*_gex_*`,
- locate ATAC directories matching `*_atac_*`,
- preprocess RNA with Scanpy and Muon:
  - mitochondrial QC,
  - cell/gene filtering,
  - total-count normalization,
  - log transform,
  - highly variable gene selection,
  - scaling,
  - save per-sample RNA objects to `data/rna_samples_h5ad/*.h5ad`,
- preprocess ATAC with SnapATAC2, Scanpy, and Muon:
  - fragment import,
  - TSS enrichment QC,
  - cell/feature filtering,
  - gene activity matrix construction,
  - normalization and log transform,
  - highly variable feature selection,
  - LSI,
  - scaling,
  - harmonized feature naming,
  - save per-sample ATAC objects to `data/atac_samples_h5ad/*.h5ad`,
- build a `MuData` object per sample and train MOFA,
- write MOFA models to `data/*.hdf5`.

Important implementation detail: the notebook currently slices `rna_dirs[0:3]` and `atac_dirs[0:3]`, so it does not yet process the full cohort.

### 3. Downstream analysis

Open `3.downstream.ipynb` and run the cells in order.

This notebook currently:

- reloads GEO sample metadata,
- extracts subject, age, sex, and stage columns,
- loads MOFA models from `./data/*.hdf5`,
- inspects model dimensions, groups, and views,
- plots top weights per factor with `mofax`.

The first markdown cell explicitly notes two open items:

- gene set enrichment analysis for factors,
- extension of the workflow to all individuals.

## Expected outputs

After running the current workflow, you should expect artifacts under `./data/` similar to:

```text
data/
  GSE239799_family.soft.gz
  ... downloaded supplementary sample files ...
  rna_samples_h5ad/
    CC0022_pre.h5ad
    CC0022_acute.h5ad
    CC0022_conv.h5ad
  atac_samples_h5ad/
    CC0022_pre.h5ad
    CC0022_acute.h5ad
    CC0022_conv.h5ad
  CC0022_pre.hdf5
  CC0022_acute.hdf5
  CC0022_conv.hdf5
```

Exact filenames depend on the downloaded sample directory names.

## Python dependencies

The repository does not yet include a pinned environment file. Based on the current code, you will need at least:

- `GEOparse`
- `numpy`
- `pandas`
- `scanpy`
- `anndata`
- `muon`
- `snapatac2`
- `hdf5plugin`
- `mofax`
- `seaborn`
- `matplotlib`
- Jupyter support (`jupyterlab` or `notebook`)

The processing notebook also calls:

- `sc.queries.biomart_annotations(...)`, which requires network access to BioMart,
- `mu.tl.mofa(..., gpu_mode=True)`, so MOFA GPU support is assumed in the current notebook.

If GPU-backed MOFA is not available in your environment, that cell will need to be adapted.

## Notes and limitations

- This is an analysis prototype, not a reusable package.
- There is no lockfile or reproducible environment specification yet.
- The notebooks currently assume a specific downloaded directory naming convention from the GEO supplementary files.
- The sample-processing code is hard-coded to the first three matched RNA/ATAC directories.
- Downstream analysis is still incomplete.

## Suggested next steps

- add a `requirements.txt` or Conda environment file,
- parameterize sample selection instead of slicing the first three directories,
- convert notebook logic into reusable scripts/functions,
- document the expected raw GEO file layout after download,
- extend MOFA training and downstream analysis to the full cohort.
