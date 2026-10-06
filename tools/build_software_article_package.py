#!/usr/bin/env python3
"""Build the software article and supplementary analysis from one Git commit.

No board execution or new scientific measurements are performed here. Preserve
historical evidence bytes and generate archive identity only after source freeze.
"""
import argparse, hashlib, io, json, os, subprocess, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='467bbe7a3c5a718d4eec7c882bc00f042487304d'
def git(*args):
    return subprocess.check_output(['git','-c','core.autocrlf=false',*args],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--commit',required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--repository',required=True)
    ap.add_argument('--tag',required=True)
    ap.add_argument('--compiler-evidence',type=Path)
    args=ap.parse_args()
    commit=git('rev-parse',args.commit+'^{commit}').decode().strip()
    out=args.output.resolve()
    if out.exists():raise SystemExit('Use a new output directory; preserve earlier packages.')
    source=out/'source';source.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',commit))) as z:
        for m in z.infolist():
            if not (source/m.filename).resolve().is_relative_to(source.resolve()):raise ValueError('Unsafe archive path')
        z.extractall(source)
    preserved=[]
    for path in git('ls-tree','-r','--name-only',BASE).decode().splitlines():
        if path.startswith(('docs/evidence/','data/')) and Path(path).suffix.lower() in ('.log','.csv','.txt','.pcap','.pv'):
            old=git('show',BASE+':'+path)
            if (source/path).read_bytes()!=old:raise ValueError('Historical evidence changed: '+path)
            preserved.append({'path':path,'sha256':sha(old)})
    identity='% Generated from the frozen source commit; this is not a hardware build identity.\n'
    identity+=r'\newcommand{\ArtifactCommit}{'+commit+'}\n'
    identity+=r'\newcommand{\ArtifactRepository}{'+args.repository+'/tree/'+commit+'}\n'
    identity+=r'\newcommand{\ArtifactRelease}{'+args.repository+'/releases/tag/'+args.tag+'}\n'
    (source/'docs/artifact_identity.tex').write_text(identity,encoding='utf8')
    validation=out/'validation';validation.mkdir()
    check=subprocess.run([os.sys.executable,str(source/'tools/analyze_submission.py'),'--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (validation/'historical_statistics_check.txt').write_bytes(check.stdout)
    if check.returncode:raise RuntimeError('Historical statistics check failed')
    for script,input_name,result_name in [('tools/summarize_endurance_csv.py','endurance_summary.csv','endurance_recount.json'),('benchmarks/energy_calculation.py','power_energy_calculations.csv','electrical_window_estimates.json')]:
        generated=json.loads(subprocess.check_output([os.sys.executable,str(source/script),'--input',str(source/'docs/evidence'/input_name)]))
        stored=json.loads((source/'docs/evidence'/result_name).read_text())
        if generated!=stored:raise ValueError('Generated evidence result mismatch: '+result_name)
    host=subprocess.run([os.sys.executable,'-m','unittest','tests.test_evidence_analysis','tests.test_submission_fixes','tests.crypto_correctness_tests.test_crypto.TestX25519RFC7748Rejection'],cwd=source,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (validation/'focused_host_checks.txt').write_bytes(host.stdout)
    if host.returncode:raise RuntimeError('Focused host checks failed')
    compiler_record=None
    if args.compiler_evidence:
        compiler_record=json.loads((source/'docs/evidence/CORRECTED_BUILD_PROVENANCE.json').read_text())
        data=args.compiler_evidence.read_bytes()
        if sha(data)!=compiler_record['archive_sha256']:raise ValueError('Compiler archive digest mismatch')
        compiled_commit=compiler_record['source_commit']
        for subtree in ('firmware','server'):
            if git('rev-parse',commit+':'+subtree)!=git('rev-parse',compiled_commit+':'+subtree):raise ValueError('Compiler source tree mismatch: '+subtree)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for rec in compiler_record['verified_artifacts']:
                names=[n for n in z.namelist() if n.endswith('/'+rec['path'])]
                if len(names)!=1 or sha(z.read(names[0]))!=rec['sha256']:raise ValueError('Compiler artifact mismatch')
        (validation/'esp32-idf55-compiler-artifacts.zip').write_bytes(data)
        (validation/'compiler-verification.json').write_text(json.dumps(compiler_record,indent=2)+'\n')
    pdf=out/'pdf';pdf.mkdir()
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']=git('show','-s','--format=%ct',commit).decode().strip()
    for tex,cwd,name in [('research_paper.tex',source/'docs','01_Manuscript.pdf'),('extended_technical_analysis.tex',source/'docs/submission','S1_Extended_Technical_Analysis.pdf')]:
        build=subprocess.run([env['CODEX_TECTONIC_PATH'],'-X','compile','--untrusted','--keep-logs','--outdir',str(pdf),tex],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (validation/(Path(tex).stem+'_build.log')).write_bytes(build.stdout)
        if build.returncode:raise RuntimeError('Compile failed: '+tex)
        (pdf/name).write_bytes((pdf/(Path(tex).stem+'.pdf')).read_bytes())
    provenance={'source_commit':commit,'measurement_source_commit':BASE,'repository':args.repository,'candidate_release_tag':args.tag,'status':'consistency revision; earlier submitted snapshot preserved; no replacement uploaded','hardware_execution':'no new execution during revision preparation; archived physical observations retained','preserved_historical_files':preserved,'generated_files':['source/docs/artifact_identity.tex','pdf/','validation/','BUILD_PROVENANCE.json','MANIFEST_SHA256.json'],'corrected_compiler_evidence':compiler_record,'source_export':'git archive; generated artifact_identity.tex identifies the exact frozen source, not the historical flashed binary'}
    (out/'BUILD_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf8')
    (out/'README.md').write_text('# Supplementary Material S2\n\nFrozen source, historical evidence and reproduction scripts for the ESP32 software article.\nStart with source/docs/reproduction_steps.md and docs/submission/COMNET_READINESS.md.\nNo new hardware data were created. Historical raw evidence bytes were checked against their source commit.\nThe exact source commit and file hashes are recorded in BUILD_PROVENANCE.json and MANIFEST_SHA256.json.\n',encoding='utf8')
    records=[{'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'MANIFEST_SHA256.json').write_text(json.dumps({'source_commit':commit,'files':records},indent=2)+'\n',encoding='utf8')
    archive=out.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(out).as_posix())
    with zipfile.ZipFile(archive) as z:
        for rec in records:
            if sha(z.read(rec['path']))!=rec['sha256']:raise RuntimeError('ZIP digest mismatch')
    archive.with_suffix('.zip.sha256').write_text(sha(archive.read_bytes())+'  '+archive.name+'\n',encoding='ascii')
    print(json.dumps({'commit':commit,'preserved_files':len(preserved),'verified_files':len(records),'pdf':str(pdf/'01_Manuscript.pdf'),'supplement':str(archive),'sha256':sha(archive.read_bytes())}))
if __name__=='__main__':main()
