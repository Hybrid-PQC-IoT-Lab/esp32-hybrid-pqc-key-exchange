"""Recalculate historical worksheet estimates, not sampled energy measurements."""
import argparse,csv,hashlib,json,math
from pathlib import Path
def calculate_energy(path):
    with path.open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
    estimates=[]
    for r in rows:
        v=float(r['Supply_Voltage_V']);i=float(r['Peak_Current_A']);t=float(r['Handshake_Duration_s'])
        if not all(math.isfinite(x) and x>0 for x in (v,i,t)):raise ValueError('Invalid voltage, current or duration')
        estimates.append({'mode':r['Mode'],'voltage_v':v,'assumed_current_a':i,'window_s':t,'calculated_window_energy_j':v*i*t})
    return {'source':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'estimates':estimates,
      'interpretation':'V x assumed I x fixed window. Not measured per-handshake energy, certified transient maximum or campaign-wide upper bound. No energy mean, SD or CI is generated.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path(__file__).resolve().parents[1]/'docs/evidence/power_energy_calculations.csv')
    p.add_argument('--output',type=Path);a=p.parse_args();t=json.dumps(calculate_energy(a.input),indent=2)+'\n'
    if a.output:a.output.write_text(t,encoding='utf8')
    print(t)
