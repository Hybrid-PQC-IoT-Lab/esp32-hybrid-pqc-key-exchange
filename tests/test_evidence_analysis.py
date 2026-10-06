import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    spec=importlib.util.spec_from_file_location(path.stem,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

class TestEvidenceAnalysis(unittest.TestCase):
    def test_endurance_denominator_is_not_invented(self):
        report=load(ROOT/'tools/summarize_endurance_csv.py').summarize(ROOT/'docs/evidence/endurance_summary.csv')
        self.assertEqual(report['accepted_rows'],sum(report['protocol_labels_as_recorded'].values()))
        self.assertIsNone(report['all_attempts']);self.assertIsNone(report['failure_rate'])

    def test_duplicate_sessions_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'duplicate.csv'
            p.write_text('handshake_id,protocol,session_id\n1,Hybrid-PQC,1\n1,Hybrid-PQC,1\n')
            with self.assertRaises(ValueError):load(ROOT/'tools/summarize_endurance_csv.py').summarize(p)

    def test_energy_uses_input_window(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'window.csv'
            p.write_text('Mode,Supply_Voltage_V,Peak_Current_A,Handshake_Duration_s\nx,5,0.15,2\n')
            report=load(ROOT/'benchmarks/energy_calculation.py').calculate_energy(p)
            self.assertEqual(report['estimates'][0]['calculated_window_energy_j'],1.5)

    def test_nonfinite_electrical_input_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'invalid.csv'
            p.write_text('Mode,Supply_Voltage_V,Peak_Current_A,Handshake_Duration_s\nx,5,nan,1\n')
            with self.assertRaises(ValueError):load(ROOT/'benchmarks/energy_calculation.py').calculate_energy(p)
