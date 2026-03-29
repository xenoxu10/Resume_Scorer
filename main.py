import argparse
from pathlib import Path

from src.config import settings
from src.loader import load_documents_from_dir
from src.scorer import llm_score_resumes_against_jd


def main() -> None:
    parser = argparse.ArgumentParser(description="Score resumes against a job description using OpenAI embeddings.")
    parser.add_argument(
        "--jd",
        type=str,
        required=False,
        help="Path to a specific JD file (.txt or .pdf). If not provided, the first file in the JD directory is used.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of top resumes to display.",
    )
    args = parser.parse_args()

    resumes_dir = Path(settings.resumes_dir)
    jds_dir = Path(settings.jds_dir)

    resumes = load_documents_from_dir(str(resumes_dir))
    if not resumes:
        print(f"No resumes found in {resumes_dir} (supported: .txt, .pdf)")
        return

    if args.jd:
        jd_path = Path(args.jd)
        if not jd_path.exists():
            print(f"JD file not found: {jd_path}")
            return
        from src.loader import read_text_file, read_pdf_file

        if jd_path.suffix.lower() == ".txt":
            jd_text = read_text_file(jd_path)
        elif jd_path.suffix.lower() == ".pdf":
            jd_text = read_pdf_file(jd_path)
        else:
            print("JD file must be .txt or .pdf")
            return
        jd_name = jd_path.name
    else:
        jds = load_documents_from_dir(str(jds_dir))
        if not jds:
            print(f"No JD files found in {jds_dir} (supported: .txt, .pdf)")
            return
        jd_name, jd_text = jds[0]

    results = llm_score_resumes_against_jd(resumes, jd_text)
    if not results:
        print("No results to display.")
        return

    print(f"Job description used: {jd_name}")
    print("\nTop resumes:")
    for name, score in results[: args.top_k]:
        print(f"- {name}: {score:.2f}/100")


if __name__ == "__main__":
    main()
