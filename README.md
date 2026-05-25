# DMD vs WT Single-End RNA-seq Pipeline (Nextflow DSL2)

This project is a modular Nextflow pipeline for transcriptome-level comparison of WT vs DMD ΔEx51 mouse tibialis anterior muscle RNA-seq data (single-end).

## Dataset Accession IDs
Source: NCBI GEO/SRA

- GEO series: `GSE156496`  
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE156496
- SRA project: `SRP278118`  
  https://www.ncbi.nlm.nih.gov/sra?term=SRP278118
- Run accessions mapped in this project:
  - `WT1` -> `SRR12478073`  
    https://www.ncbi.nlm.nih.gov/sra/SRR12478073
  - `WT2` -> `SRR12478074`  
    https://www.ncbi.nlm.nih.gov/sra/SRR12478074
  - `DMD1` -> `SRR12478076`  
    https://www.ncbi.nlm.nih.gov/sra/SRR12478076
  - `DMD2` -> `SRR12478077`  
    https://www.ncbi.nlm.nih.gov/sra/SRR12478077

Current `samplesheet.csv` expects:

```csv
sample,fastq_1
WT1,data/WT1_R1.fastq.gz
WT2,data/WT2_R1.fastq.gz
DMD1,data/DMD1_R1.fastq.gz
DMD2,data/DMD2_R1.fastq.gz
```

## Pipeline Steps
1. Read sample sheet (single-end FASTQ input)
2. Run FastQC on raw reads
3. Trim reads with fastp
4. Quantify transcripts with Salmon
5. Aggregate QC with MultiQC
6. Build expression matrix from `quant.sf` files

## Requirements
- macOS/Linux
- Java 17+
- Nextflow (DSL2)
- Conda (Miniforge/Anaconda) for `-profile conda`

## Reference Preparation
Download transcriptome FASTA (example: Ensembl GRCm39 cDNA) and build Salmon index:

```bash
mkdir -p refs
salmon index \
  -t refs/Mus_musculus.GRCm39.cdna.all.fa.gz \
  -i refs/salmon_index \
  -k 31
```

## Run Command
From project directory:

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$HOME/miniforge3/bin:$PATH"

nextflow run main.nf \
  -profile conda \
  --samplesheet samplesheet.csv \
  --outdir results \
  --salmon_index "$PWD/refs/salmon_index" \
  -resume
```

## Output
- `results/fastqc/`: FastQC reports
- `results/fastp/`: trimmed FASTQ + fastp reports
- `results/salmon/`: sample-level `*.quant.sf`
- `results/multiqc/`: MultiQC report
- `results/matrix/expression_matrix.tsv`: merged expression table

## GitHub Repository Note
Large raw data and generated artifacts are intentionally excluded from GitHub, including:
- raw FASTQ files
- Salmon index files
- Nextflow `work/` directory
- large intermediate result directories
