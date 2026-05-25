// Salmon module for DMD RNA-seq pipeline (DSL2)
// Quantifies transcript abundance using Salmon
process SALMON {
    tag "${sample_id}"
    publishDir "${params.outdir}/salmon", mode: 'copy'
    conda "bioconda::salmon"

    input:
        tuple val(sample_id), path(trimmed_reads)

    output:
        tuple val(sample_id), path("${sample_id}.quant.sf")

    script:
    """
    salmon quant -i ${params.salmon_index} -l A \
        -r ${trimmed_reads} \
        -p ${task.cpus} \
        --validateMappings \
        -o salmon_out
    cp salmon_out/quant.sf ${sample_id}.quant.sf
    """
}
