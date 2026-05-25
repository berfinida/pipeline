// MultiQC module for DMD RNA-seq pipeline (DSL2)
// Aggregates QC and quantification results into a single report
process MULTIQC {
    tag "multiqc"
    publishDir "${params.outdir}/multiqc", mode: 'copy'
    conda "bioconda::multiqc=1.17"

    input:
    path(qc_files)

    output:
    path("multiqc_report.html")

    script:
    """
    multiqc $qc_files -o .
    """
}
