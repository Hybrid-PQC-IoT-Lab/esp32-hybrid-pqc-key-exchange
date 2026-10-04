#!/usr/bin/env python3
"""Export one Git commit, compile its manuscript, and hash every package member.

The source commit cannot contain its own hash. The exported artifact_identity.tex
is therefore a declared generated file, like the compiled PDF and manifest.
Historical raw observations are exported directly from immutable Git objects.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
BASE='467bbe7a3c5a718d4eec7c882bc00f042487304d'


def git(*args):
    # Export canonical object bytes even on Windows checkouts using autocrlf.
    return subprocess.check_output(['git','-c','core.autocrlf=false',*args],cwd=ROOT)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--commit',required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--repository',required=True)
    ap.add_argument('--tag',required=True)
    ap.add_argument('--tectonic',default=os.environ.get('CODEX_TECTONIC_PATH','tectonic'))
    ap.add_argument('--validation-dir',type=Path)
    args=ap.parse_args()
    commit=git('rev-parse',args.commit+'^{commit}').decode().strip()
    out=args.output.resolve()
    if out.exists():
        raise SystemExit('Output already exists; choose a new directory to preserve earlier artifacts.')
    out.mkdir(parents=True)
    source=out/'source'
    source.mkdir()
    data=git('archive','--format=zip',commit)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for member in z.infolist():
            target=(source/member.filename).resolve()
            if not target.is_relative_to(source.resolve()):
                raise ValueError('Unsafe archive member')
        z.extractall(source)
    subprocess.run([sys.executable,str(source/'tools/analyze_submission.py'),'--check'],check=True)
    preserved=[]
    for entry in git('ls-tree','-r','--name-only',BASE).decode().splitlines():
        if (entry.startswith(('docs/evidence/','data/')) and Path(entry).suffix.lower() in ('.log','.csv','.txt','.pcap','.pv')):
            original=git('show',BASE+':'+entry)
            candidate=source/entry
            if not candidate.exists() or candidate.read_bytes()!=original:
                raise ValueError('Historical evidence changed: '+entry)
            preserved.append(entry)
    identity=source/'docs/artifact_identity.tex'
    identity.write_text('% Generated from immutable Git metadata.\n'
        +'\\newcommand{\\ArtifactCommit}{'+commit+'}\n'
        +'\\newcommand{\\ArtifactRepository}{'+args.repository+'/tree/'+commit+'}\n'
        +'\\newcommand{\\ArtifactRelease}{'+args.repository+'/releases/tag/'+args.tag+'}\n',encoding='utf-8')
    pdf_dir=out/'manuscript'
    pdf_dir.mkdir()
    validation=out/'validation'
    validation.mkdir()
    env=os.environ.copy()
    env['SOURCE_DATE_EPOCH']=git('show','-s','--format=%ct',commit).decode().strip()
    command=[args.tectonic,'-X','compile','--untrusted','--keep-logs','--outdir',str(pdf_dir),'research_paper.tex']
    result=subprocess.run(command,cwd=source/'docs',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (validation/'latex-build.log').write_bytes(result.stdout)
    if result.returncode:
        raise RuntimeError('LaTeX build failed; see validation/latex-build.log')
    if not (pdf_dir/'research_paper.pdf').exists():
        raise RuntimeError('Compiler returned without a PDF')
    if args.validation_dir:
        for p in sorted(args.validation_dir.resolve().iterdir()):
            if p.is_file() and p.name!='latex.log':
                (validation/p.name).write_bytes(p.read_bytes())
    provenance={
        'source_commit':commit,'measurement_source_commit':BASE,
        'repository':args.repository,'candidate_release_tag':args.tag,
        'release_url':args.repository+'/releases/tag/'+args.tag,
        'status':'NO-GO for journal submission until documented blockers are resolved',
        'build_epoch':env['SOURCE_DATE_EPOCH'],
        'preserved_evidence_files':preserved,
        'source_export':'git archive of source_commit; generated artifact_identity.tex is the only added source-directory file',
        'derived_outputs':['source/docs/artifact_identity.tex','manuscript/research_paper.pdf','validation/','BUILD_PROVENANCE.json','MANIFEST_SHA256.json'],
        'original_release_pdf_sha256':'3a95ae9c4feca696084fd67a78eee4cf13c287bd2dd8212e9b1381f5bb104b58',
        'original_release_zip_sha256':'c9f2d65f04ee89d3cbc2feb5a3e3308967ed40dffc4b93f11a8fe1281b6ccfdb',
        'upstream_reviewed_commit':'670448651276740e0d58931f388ca32035cb6245',
        'latest_primary_release_pdf_sha256':'794cc1f743971680f4a046e3a56bc76d11066a62a5e04d5e1eb0409bf064355a',
        'latest_primary_release_zip_sha256':'a84d636bbd1c92a6f3f627ec58e4cc9f705be2abf818a8e27206e3c036e87557',
        'hardware_execution':'None performed for corrected commit; archived data remain historical',
    }
    (out/'BUILD_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    (out/'README.md').write_text('# Journal audit candidate\n\nStart with `source/docs/submission/GO_NO_GO.md`.\n'
        +'The corrected manuscript is `manuscript/research_paper.pdf`.\n'
        +'Editable source and figures are under `source/docs` and `source/figures`.\n'
        +'Historical PDF is clearly marked under `source/docs/archive/`.\n'
        +'No new ESP32 measurements were created. Author placeholders and hardware-evidence gaps remain.\n'
        +'`BUILD_PROVENANCE.json` gives the exact source commit and preserved evidence list.\n',encoding='utf-8')
    records=[]
    for p in sorted(out.rglob('*')):
        if p.is_file():
            records.append({'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)})
    manifest=out/'MANIFEST_SHA256.json'
    manifest.write_text(json.dumps({'source_commit':commit,'files':records},indent=2)+'\n',encoding='utf-8')
    for record in records:
        if digest(out/record['path'])!=record['sha256']:
            raise RuntimeError('Post-build digest mismatch')
    zip_path=out.with_suffix('.zip')
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():
                stamp=datetime.fromtimestamp(int(env['SOURCE_DATE_EPOCH']),timezone.utc)
                info=zipfile.ZipInfo(p.relative_to(out).as_posix(),date_time=stamp.timetuple()[:6])
                info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(zip_path) as z:
        for record in records:
            if hashlib.sha256(z.read(record['path'])).hexdigest()!=record['sha256']:
                raise RuntimeError('ZIP member hash mismatch')
    zip_path.with_suffix('.zip.sha256').write_text(digest(zip_path)+'  '+zip_path.name+'\n',encoding='ascii')
    print(json.dumps({'commit':commit,'pdf':str(pdf_dir/'research_paper.pdf'),'zip':str(zip_path),
                      'sha256':digest(zip_path),'verified_files':len(records),
                      'preserved_historical_files':len(preserved)},indent=2))


if __name__=='__main__':
    main()
