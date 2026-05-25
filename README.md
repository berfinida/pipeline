# DMD RNA-seq Nextflow Pipeline

A custom, modular Nextflow DSL2 pipeline for processing Duchenne Muscular Dystrophy (DMD) RNA-seq data.

## Features
- FastQC quality control
- fastp read trimming/filtering
- Salmon transcript quantification
- MultiQC summary reporting
- Gene expression matrix output

## Project Structure
```
dmd-rnaseq-nextflow/
├── main.nf
├── nextflow.config
├── samplesheet.csv
├── README.md
├── modules/
│   ├── fastqc.nf
│   ├── fastp.nf
│   ├── salmon.nf
│   └── multiqc.nf
├── data/
├── refs/
├── results/
└── scripts/
```

## Requirements
- Nextflow >=22.10.0
- Conda or Docker/Singularity

## Usage
1. Edit `samplesheet.csv` with your sample information.
2. Set reference paths in `nextflow.config`.
3. Run the pipeline:

```bash
nextflow run main.nf -profile conda --samplesheet samplesheet.csv --outdir results --salmon_index refs/salmon_index
```

## Example `samplesheet.csv`
```
sample,fastq_1,fastq_2
DMD1,data/DMD1_R1.fastq.gz,data/DMD1_R2.fastq.gz
DMD2,data/DMD2_R1.fastq.gz,data/DMD2_R2.fastq.gz
```

## Reference preparation
Before running the real analysis, download a transcriptome FASTA file. For example, for mouse data you can use the Ensembl GRCm39 cDNA/transcript FASTA file and place it under `refs/`.

Then build the Salmon index:

```bash
mkdir -p refs
salmon index \
  -t refs/Mus_musculus.GRCm39.cdna.all.fa.gz \
  -i refs/salmon_index \
  -k 31
```

Notes:
- The current tiny TEST FASTQ files are only for pipeline testing.
- Real DMD FASTQ files must be downloaded from GEO/SRA.
- Once the Salmon index and real FASTQ files exist, run the pipeline normally.

## Output
- Quality reports, trimmed FASTQs, quantification, MultiQC, and expression matrix in `results/`.

## Notes
- All processes are modular and use clean DSL2 syntax.
- See comments in each file for details.
