# DMD vs WT Single-End RNA-seq Analysis Pipeline Using Nextflow DSL2

## 1. Introduction
Duchenne muscular dystrophy (DMD) is a progressive neuromuscular disorder caused by mutations in the dystrophin gene. RNA-seq provides a robust strategy for investigating transcriptomic differences between DMD and wild-type (WT) muscle samples. In this study, a reproducible and modular analysis workflow was implemented using Nextflow DSL2 for single-end RNA-seq data.

The selected public dataset was GSE156496 / SRP278118, with two WT and two DMD (Delta 51) samples. The objective was to establish a reproducible end-to-end pipeline from raw reads to a comparable transcript-level expression matrix.

## 2. Methods
### 2.1 Dataset and sample selection
- WT1 = SRR12478073 = GSM4732625 = TA_WT_1 RNA-seq
- WT2 = SRR12478074 = GSM4732626 = TA_WT_2 RNA-seq
- DMD1 = SRR12478076 = GSM4732628 = TA_D51_4 RNA-seq (Delta 51)
- DMD2 = SRR12478077 = GSM4732629 = TA_D51_5 RNA-seq (Delta 51)

### 2.2 Reference and index
- Reference: Mus musculus GRCm39 Ensembl cDNA transcriptome FASTA
- Indexing: Salmon index built with k=31

### 2.3 Pipeline architecture and steps
The Nextflow DSL2 workflow consists of modular processes:
1. FastQC raw read quality control
2. fastp single-end read trimming and filtering
3. Salmon transcript quantification
4. MultiQC report generation
5. Custom Python/pandas expression matrix generation

### 2.4 Output directories
- `results/fastqc/`
- `results/fastp/`
- `results/salmon/`
- `results/multiqc/multiqc_report.html`
- `results/matrix/expression_matrix.tsv`

## 3. Results
The workflow completed successfully (exit code 0) and all planned processes finished without unresolved runtime errors. The expression matrix was generated successfully at `results/matrix/expression_matrix.tsv`.

The matrix structure confirms correct grouping of samples for downstream interpretation. The first columns are:
- `Name`
- `DMD1`
- `DMD2`
- `WT1`
- `WT2`

In addition, a descriptive TPM-based comparison step was added to summarize mean TPM differences between DMD and WT samples using log2 fold change with pseudocount 1.

## 4. Supplementary Items (SI)
### SI-1. GitHub repository
- https://github.com/berfinida/pipeline

### SI-2. Dataset accession IDs
- Study IDs: GSE156496 / SRP278118
- Runs: SRR12478073, SRR12478074, SRR12478076, SRR12478077
- GSM IDs: GSM4732625, GSM4732626, GSM4732628, GSM4732629
- GEO link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE156496
- SRA project link: https://www.ncbi.nlm.nih.gov/sra?term=SRP278118
- Run links:
  - https://www.ncbi.nlm.nih.gov/sra/SRR12478073
  - https://www.ncbi.nlm.nih.gov/sra/SRR12478074
  - https://www.ncbi.nlm.nih.gov/sra/SRR12478076
  - https://www.ncbi.nlm.nih.gov/sra/SRR12478077

### SI-3. Run command
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

### SI-4. Software/tools used
- Nextflow DSL2
- FastQC
- fastp
- Salmon
- MultiQC
- Python (pandas)

### SI-5. Data availability note
Raw FASTQ files and Salmon index files are excluded from GitHub due to file-size constraints. The repository contains workflow code, configuration, and lightweight reproducibility materials.
