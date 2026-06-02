#!/usr/bin/env python3

import os
import subprocess
import sys
import multiprocessing as mp
from pathlib import Path


def report(root: Path):
    domains = sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith("."))

    if not domains:
        print("No domain directories found.")
        return

    print(f"{'Domain':<30} {'PDFs':>6} {'Done':>6} {'HTMLs':>6}")
    print("-" * 50)

    total_pdf = total_done = total_html = 0

    for dom in domains:
        pdfs = sorted(dom.rglob("*.pdf"))
        done = sum(1 for p in pdfs if p.with_suffix(".cnt.md").exists())
        htmls = sorted(dom.rglob("*.html")) + sorted(dom.rglob("*.htm"))

        n_pdf = len(pdfs)
        n_html = len(htmls)

        total_pdf += n_pdf
        total_done += done
        total_html += n_html

        print(f"{dom.name:<30} {n_pdf:>6} {done:>6} {n_html:>6}")

    print("-" * 50)
    print(f"{'Total':<30} {total_pdf:>6} {total_done:>6} {total_html:>6}")


def gpu_count() -> int:
    try:
        result = subprocess.run(
            ["nvidia-smi", "-L"],
            capture_output=True,
            text=True,
            timeout=5
        )

        return len([l for l in result.stdout.split("\n") if l.strip()])

    except Exception:
        return 0


def convert_worker(gpu_id: int, files: list[Path]):
    """
    One worker process bound to one GPU.
    """

    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    print(f"[GPU {gpu_id}] Starting worker with {len(files)} files")

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    models = create_model_dict()

    # IMPORTANT:
    # create converter ONCE
    converter = PdfConverter(
        artifact_dict=models
    )

    for pdf_path in files:
        try:
            target = pdf_path.with_suffix(".cnt.md")

            if target.exists():
                print(f"[GPU {gpu_id}] Skipping existing: {pdf_path}")
                continue

            print(f"[GPU {gpu_id}] Converting: {pdf_path}")

            rendered = converter(str(pdf_path))

            target.write_text(
                rendered.markdown,
                encoding="utf-8"
            )

            print(f"[GPU {gpu_id}] Created: {target}")
            import time

            time.sleep(10)
        except Exception as e:
            print(f"[GPU {gpu_id}] ERROR {pdf_path}: {e}")

    print(f"[GPU {gpu_id}] Finished")


def convert_cpu(root: Path, limit: int | None = None):
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    pdf_files = sorted(root.rglob("*.pdf"))
    pending = [p for p in pdf_files if not p.with_suffix(".cnt.md").exists()]

    if limit is not None:
        pending = pending[:limit]

    if not pending:
        print("No pending PDFs.")
        return

    models = create_model_dict()

    converter = PdfConverter(
        artifact_dict=models
    )

    for pdf_path in pending:
        try:
            print(f"[CPU] Converting: {pdf_path}")

            rendered = converter(str(pdf_path))

            target = pdf_path.with_suffix(".cnt.md")

            target.write_text(
                rendered.markdown,
                encoding="utf-8"
            )

            print(f"[CPU] Created: {target}")

        except Exception as e:
            print(f"[CPU] ERROR {pdf_path}: {e}")


def convert_multi_gpu(root: Path, limit: int | None = None):
    pdf_files = sorted(root.rglob("*.pdf"))

    pending = [
        p for p in pdf_files
        if not p.with_suffix(".cnt.md").exists()
    ]

    if limit is not None:
        pending = pending[:limit]

    if not pending:
        print("No pending PDFs.")
        return

    ngpus = gpu_count()

    if ngpus < 2:
        print("Less than 2 GPUs detected.")
        return

    print(f"Using {ngpus} GPUs")

    # split files between GPUs
    chunks = [[] for _ in range(ngpus)]

    for idx, pdf in enumerate(pending):
        chunks[idx % ngpus].append(pdf)

    mp.set_start_method("spawn", force=True)

    processes = []

    for gpu_id in range(ngpus):
        if not chunks[gpu_id]:
            continue

        p = mp.Process(
            target=convert_worker,
            args=(gpu_id, chunks[gpu_id])
        )

        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("All workers completed.")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    ngpus = gpu_count()

    print()
    print("1) Multi GPU")
    print("2) Single GPU")
    print("3) CPU")
    print("4) Report")
    print()

    choice = input("Choose option (default: 1): ").strip() or "1"

    if choice == "4":
        report(root)
        return

    n_input = input("Number of files to convert (default: all): ").strip()

    limit = int(n_input) if n_input.isdigit() else None

    if choice == "1":
        if ngpus < 2:
            print("Need at least 2 GPUs.")
            return

        convert_multi_gpu(root, limit)

    elif choice == "2":
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        convert_worker(0, sorted(root.rglob("*.pdf"))[:limit])

    elif choice == "3":
        convert_cpu(root, limit)

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
