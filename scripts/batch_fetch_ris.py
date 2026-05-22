#!/usr/bin/env python3
import csv, re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True)

def curl_text(url, accept=None, timeout=25):
    hdr = f"-H 'Accept: {accept}'" if accept else ""
    cmd = f"curl -L -s --max-time {timeout} {hdr} '{url}'"
    r = sh(cmd)
    return r.stdout.decode('utf-8','ignore') if r.returncode == 0 else ''

def extract_doi(url):
    u = unquote(url)
    m = DOI_RE.search(u)
    if m:
        return m.group(0).rstrip(').,;')
    return ""

def fetch_ris_by_doi(doi):
    return curl_text(f"https://doi.org/{doi}", accept="application/x-research-info-systems")

def extract_doi_from_html(html):
    patterns = [
        r'citation_doi"\s*content="([^"]+)"',
        r"citation_doi'\s*content='([^']+)'",
        r'"doi"\s*:\s*"(10\\.[^"\\]+)"',
        r'"https?://doi.org/(10\\.[^"\\]+)"',
    ]
    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            return m.group(1).replace('\\/', '/')
    m = DOI_RE.search(html)
    return m.group(0) if m else ""

def normalize_ris(txt):
    if not txt.strip().startswith('TY  -'):
        return ""
    return txt if txt.endswith('\n') else txt + '\n'

def main():
    if len(sys.argv) < 2:
        print('usage: batch_fetch_ris.py input.tsv [outdir]')
        return 1
    inp = Path(sys.argv[1])
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('RIS')
    outdir.mkdir(parents=True, exist_ok=True)
    report = []
    seen = {}
    for raw in inp.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = re.split(r'\s+', line, maxsplit=1)
        if len(parts) < 2:
            continue
        idx, url = parts[0], parts[1].strip()
        if idx in seen:
            report.append((idx, url, seen[idx]['doi'], seen[idx]['status'], seen[idx]['note']))
            continue
        doi = extract_doi(url)
        source = 'url'
        if not doi:
            html = curl_text(url)
            doi = extract_doi_from_html(html) if html else ''
            source = 'html'
        ris = ''
        if doi:
            ris = normalize_ris(fetch_ris_by_doi(doi))
        if ris:
            (outdir / f"{idx}.ris").write_text(ris, encoding='utf-8')
            status, note = 'ok', f'from DOI ({source})'
        else:
            status, note = 'failed', 'doi_not_found_or_ris_unavailable'
        seen[idx] = {'doi': doi, 'status': status, 'note': note}
        report.append((idx, url, doi, status, note))
        print(idx, status, doi)
    with open(outdir / '_fetch_report.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id','url','doi','status','note'])
        w.writerows(report)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
