import math
import os
import sys
import pandas as pd


def main():
    if len(sys.argv) != 2:
        print("Usage: differential_summary.py results/matrix/expression_matrix.tsv", file=sys.stderr)
        sys.exit(1)

    input_tsv = sys.argv[1]
    out_dir = os.path.dirname(input_tsv)
    summary_tsv = os.path.join(out_dir, "dmd_vs_wt_summary.tsv")
    up_tsv = os.path.join(out_dir, "top10_upregulated.tsv")
    down_tsv = os.path.join(out_dir, "top10_downregulated.tsv")

    df = pd.read_csv(input_tsv, sep="\t")

    required_cols = ["Name", "DMD1", "DMD2", "WT1", "WT2"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    dmd_cols = ["DMD1", "DMD2"]
    wt_cols = ["WT1", "WT2"]

    for col in dmd_cols + wt_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    df["DMD_mean_TPM"] = df[dmd_cols].mean(axis=1)
    df["WT_mean_TPM"] = df[wt_cols].mean(axis=1)
    df["log2FC"] = ((df["DMD_mean_TPM"] + 1.0) / (df["WT_mean_TPM"] + 1.0)).apply(math.log2)

    summary_cols = ["Name", "DMD_mean_TPM", "WT_mean_TPM", "log2FC"]
    summary_df = df[summary_cols].copy()
    summary_df.to_csv(summary_tsv, sep="\t", index=False, float_format="%.6f")

    up_df = summary_df.sort_values("log2FC", ascending=False).head(10)
    down_df = summary_df.sort_values("log2FC", ascending=True).head(10)

    up_df.to_csv(up_tsv, sep="\t", index=False, float_format="%.6f")
    down_df.to_csv(down_tsv, sep="\t", index=False, float_format="%.6f")


if __name__ == "__main__":
    main()
