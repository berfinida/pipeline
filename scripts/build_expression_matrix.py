import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: build_expression_matrix.py manifest.tsv expression_matrix.tsv", file=sys.stderr)
        sys.exit(1)
    manifest = sys.argv[1]
    out_tsv = sys.argv[2]

    # Read manifest: sample_id <tab> quant.sf
    sample_files = []
    with open(manifest) as f:
        for line in f:
            if not line.strip():
                continue
            sample, quant = line.rstrip("\n").split("\t")
            sample_files.append((sample, quant))

    transcripts = []
    transcript_seen = set()
    sample_tpms = {}

    for sample, quant_path in sample_files:
        sample_tpms[sample] = {}
        with open(quant_path) as quant_file:
            header = quant_file.readline().rstrip("\n").split("\t")
            name_idx = header.index("Name")
            tpm_idx = header.index("TPM")

            for line in quant_file:
                fields = line.rstrip("\n").split("\t")
                transcript = fields[name_idx]
                if transcript not in transcript_seen:
                    transcripts.append(transcript)
                    transcript_seen.add(transcript)
                sample_tpms[sample][transcript] = fields[tpm_idx]

    samples = [sample for sample, _ in sample_files]
    with open(out_tsv, "w") as out:
        out.write("Name\t" + "\t".join(samples) + "\n")
        for transcript in transcripts:
            values = [sample_tpms[sample].get(transcript, "0") for sample in samples]
            out.write(transcript + "\t" + "\t".join(values) + "\n")


if __name__ == "__main__":
    main()
