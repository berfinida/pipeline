// fastp module for DMD RNA-seq pipeline (DSL2)
// Performs adapter and quality trimming on single-end FASTQ files
process FASTP {
    tag "${sample_id}"
    publishDir "${params.outdir}/fastp", mode: 'copy'
    conda "bioconda::fastp=0.23.4"

    input:
    tuple val(sample_id), path(reads)

    output:
        tuple val(sample_id),
              path("${sample_id}.trimmed.fastq.gz"),
              path("${sample_id}_fastp.json"),
              path("${sample_id}_fastp.html")

    script:
    """
    fastp -i ${reads} \
          -o ${sample_id}.trimmed.fastq.gz \
          --json ${sample_id}_fastp.json \
          --html ${sample_id}_fastp.html
    """
}
