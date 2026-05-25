from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib import colors

OUT = "/Users/berfinnidaozturk/Desktop/kemal_sanli_odev/dmd-rnaseq-nextflow/report/DMD_vs_WT_SingleEnd_RNAseq_Assignment_Report.pdf"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title2", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=16)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, leading=19, spaceBefore=10, spaceAfter=8)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, leading=15, spaceBefore=8, spaceAfter=6)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=11, leading=15)

    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=2.2*cm, bottomMargin=2.2*cm)
    story = []

    # Cover
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("DMD vs WT Single-End RNA-seq Analysis Pipeline Using Nextflow DSL2", title))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Molecular Biology and Biotechnology Master’s Programme", body))
    story.append(Paragraph("Assignment Report", body))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Student: Berfin Nida Öztürk", body))
    story.append(Paragraph("Date: 25 May 2026", body))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("Contents", h1))
    toc_lines = [
        "1. Introduction",
        "2. Methods",
        "3. Results",
        "4. Supplementary Items (SI)",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body)) for x in toc_lines], bulletType='1'))
    story.append(PageBreak())

    story.append(Paragraph("1. Introduction", h1))
    story.append(Paragraph("Duchenne muscular dystrophy (DMD) is a progressive neuromuscular disorder caused by mutations in the dystrophin gene. RNA-seq provides a robust approach to investigate transcriptomic differences between DMD and wild-type (WT) muscle samples. In this study, a modular and reproducible single-end RNA-seq workflow was implemented with Nextflow DSL2.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("The selected public dataset was GSE156496 / SRP278118, including two WT and two DMD (Delta 51) samples. The aim was to generate a reproducible end-to-end pipeline from raw FASTQ files to a transcript-level expression matrix.", body))

    story.append(Paragraph("2. Methods", h1))
    story.append(Paragraph("2.1 Dataset and sample selection", h2))
    samples = [
        "WT1 = SRR12478073 = GSM4732625 = TA_WT_1 RNA-seq",
        "WT2 = SRR12478074 = GSM4732626 = TA_WT_2 RNA-seq",
        "DMD1 = SRR12478076 = GSM4732628 = TA_D51_4 RNA-seq (Delta 51)",
        "DMD2 = SRR12478077 = GSM4732629 = TA_D51_5 RNA-seq (Delta 51)",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body)) for x in samples], bulletType='bullet'))

    story.append(Paragraph("2.2 Reference preparation", h2))
    story.append(Paragraph("Mus musculus GRCm39 Ensembl cDNA transcriptome FASTA was used as reference. Salmon index was built with k=31.", body))

    story.append(Paragraph("2.3 Pipeline steps", h2))
    steps = [
        "FastQC raw read quality control",
        "fastp single-end read trimming and filtering",
        "Salmon transcript quantification",
        "MultiQC report generation",
        "Custom Python/pandas expression matrix generation",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body)) for x in steps], bulletType='1'))

    story.append(Paragraph("2.4 Outputs", h2))
    outputs = [
        "results/fastqc/",
        "results/fastp/",
        "results/salmon/",
        "results/multiqc/multiqc_report.html",
        "results/matrix/expression_matrix.tsv",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body)) for x in outputs], bulletType='bullet'))

    story.append(Paragraph("3. Results", h1))
    story.append(Paragraph("The pipeline completed successfully with exit code 0. All workflow processes, including MultiQC and EXPR_MATRIX, completed without unresolved errors.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("The expression matrix was generated successfully at results/matrix/expression_matrix.tsv. The first columns are: Name, DMD1, DMD2, WT1, WT2.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A descriptive TPM-based comparison was added to compute DMD mean TPM, WT mean TPM, and log2FC using pseudocount 1. This is a descriptive summary and not a formal statistical differential expression test.", body))

    story.append(Paragraph("4. Supplementary Items (SI)", h1))
    si = [
        "GitHub repository: https://github.com/berfinida/pipeline",
        "Dataset IDs: GSE156496 / SRP278118; SRR12478073, SRR12478074, SRR12478076, SRR12478077",
        "Run command: nextflow run main.nf -profile conda --samplesheet samplesheet.csv --outdir results --salmon_index \"$PWD/refs/salmon_index\" -resume",
        "Software: Nextflow DSL2, FastQC, fastp, Salmon, MultiQC, Python (pandas)",
        "Raw FASTQ files and Salmon index are excluded from GitHub due to file size",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body)) for x in si], bulletType='bullet'))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main()
