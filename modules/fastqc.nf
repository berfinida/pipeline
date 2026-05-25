// FastQC module for DMD RNA-seq pipeline (DSL2)
// Runs FastQC on a single FASTQ file (R1 or R2)
process FASTQC {
    tag "${sample_id}"
    publishDir "${params.outdir}/fastqc", mode: 'copy'
    conda "bioconda::fastqc=0.12.1"

    input:
    tuple val(sample_id), path(reads)

    output:
        tuple val(sample_id), \
              path("*_fastqc.zip"), \
              path("*_fastqc.html")

    script:
    """
    fastqc --outdir . $reads
    """
}
