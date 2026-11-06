"""Gera o ZIP da skill para enviar ao Claude App / claude.ai.

A pasta `gerar-telas/` fica na raiz do ZIP (exigência do upload) e nada de
`__pycache__`/`.pyc` entra. Saída: dist/gerar-telas-<versão>.zip

    py tools/gerar_zip.py 0.3.0          (Linux: python3 tools/gerar_zip.py 0.3.0)
    py tools/gerar_zip.py                (sem versão: gerar-telas-dev.zip)
"""
import argparse
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / ".claude" / "skills" / "gerar-telas"
DIST = RAIZ / "dist"
IGNORAR_PASTAS = {"__pycache__"}
IGNORAR_SUFIXOS = {".pyc", ".pyo"}
DATA_FIXA = (2020, 1, 1, 0, 0, 0)  # ZIP reproduzível: mesmo conteúdo, mesmo arquivo


def arquivos_da_skill(skill: Path = SKILL) -> list[Path]:
    return sorted(
        p for p in skill.rglob("*")
        if p.is_file()
        and not (set(p.relative_to(skill).parts) & IGNORAR_PASTAS)
        and p.suffix not in IGNORAR_SUFIXOS
    )


def gerar_zip(destino: Path, skill: Path = SKILL) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arq in arquivos_da_skill(skill):
            nome = (Path(skill.name) / arq.relative_to(skill)).as_posix()
            info = zipfile.ZipInfo(nome, DATA_FIXA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, arq.read_bytes())
    return destino


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("versao", nargs="?", default="dev", help="ex.: 0.3.0")
    args = ap.parse_args()
    if not (SKILL / "SKILL.md").is_file():
        sys.exit(f"SKILL.md não encontrado em {SKILL}")
    destino = gerar_zip(DIST / f"{SKILL.name}-{args.versao}.zip")
    print(f"{destino}  ({destino.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
