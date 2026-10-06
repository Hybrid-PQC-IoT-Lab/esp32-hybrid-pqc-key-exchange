"""Summarize preserved accepted rows; not all-attempt reliability."""
import argparse,csv,hashlib,json
from collections import Counter
from pathlib import Path
def summarize(path):
    with path.open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f))
    ids=[r['handshake_id'] for r in rows]
    if len(set(ids))!=len(ids): raise ValueError('Duplicate handshake IDs')
    return {'source':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'accepted_rows':len(rows),'protocol_labels_as_recorded':dict(Counter(r['protocol'] for r in rows)),
      'sitting_labels_as_recorded':dict(Counter(r['session_id'] for r in rows)),
      'all_attempts':None,'failure_rate':None,
      'interpretation':'Parser-accepted rows only. Protocol labels require negotiation evidence. TCP SYN count, uninterrupted duration, cryptographic success and memory stability cannot be established by this CSV alone.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path(__file__).resolve().parents[1]/'docs/evidence/endurance_summary.csv')
    p.add_argument('--output',type=Path);a=p.parse_args();t=json.dumps(summarize(a.input),indent=2)+'\n'
    if a.output:a.output.write_text(t,encoding='utf8')
    print(t)
