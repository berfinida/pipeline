// main.nf - DMD RNA-seq Nextflow Pipeline (DSL2)
// Author: Custom pipeline for DMD transcriptome analysis
// See README.md for usage instructions

nextflow.enable.dsl=2

// =========================
// Import process modules
// =========================
include { FASTQC } from './modules/fastqc.nf'
include { FASTP } from './modules/fastp.nf'
include { SALMON } from './modules/salmon.nf'
include { MULTIQC } from './modules/multiqc.nf'

// =========================
// Workflow definition
// =========================
workflow {
    // 1. Load sample sheet and create channel of tuples: (sample_id, fastq_1)
    samples_ch = Channel.fromPath(params.samplesheet)
        .splitCsv(header:true)
        .map { row -> tuple(row.sample, file(row.fastq_1)) }

    // 2. Run FastQC on raw reads (single-end)
    fastqc_raw_ch = samples_ch | FASTQC

    // 3. Run fastp for adapter/quality trimming
    fastp_ch = samples_ch | FASTP

    // 4. Run FastQC on trimmed reads (optional, not included for brevity)
    // fastqc_trimmed_ch = fastp_ch.flatMap { sample_id, r1, r2, ... ->
    //     [ tuple(sample_id, r1), tuple(sample_id, r2) ]
    // } | FASTQC

    // 5. Quantify transcripts with Salmon (single-end)
    salmon_ch = fastp_ch
        .map { sample_id, trimmed_reads, fastp_json, fastp_html -> tuple(sample_id, trimmed_reads) }
        | SALMON

    // 6. Run MultiQC on all QC and quantification outputs
    multiqc_input_ch = fastqc_raw_ch
        .map { sample_id, zip, html -> [zip, html] }
        .mix(fastp_ch.map { sample_id, trimmed_reads, fastp_json, fastp_html -> [fastp_json, fastp_html] })
        .mix(salmon_ch.map { sample_id, quant -> quant })
        .flatten()
        .collect()
    multiqc_ch = multiqc_input_ch | MULTIQC

    // 7. Prepare gene expression matrix from Salmon quant.sf files
    salmon_ch
        .collect()
        .map { quant_list ->
            def sample_ids = quant_list.collect { it[0] }
            def quant_files = quant_list.collect { it[1] }
            def manifest = [sample_ids, quant_files].transpose().collect { sample, quant -> "${sample}\t${quant.name}" }.join('\n')
            tuple(file("scripts/build_expression_matrix.py"), manifest, quant_files)
        }
        | EXPR_MATRIX
}

// =========================
// Expression matrix process
// =========================
process EXPR_MATRIX {
    tag "expression_matrix"
    publishDir "${params.outdir}/matrix", mode: 'copy'
    input:
        tuple path(matrix_script), val(manifest), path(quant_files)
    output:
        path("expression_matrix.tsv")
    script:
"""
cat > manifest.tsv <<'EOF'
${manifest}
EOF
python3 ${matrix_script} manifest.tsv expression_matrix.tsv
"""
}
// End of main.nf
