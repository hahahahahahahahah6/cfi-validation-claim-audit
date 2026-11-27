import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from cfi_validation_claim_audit.audit import audit, claims, evidence
from cfi_validation_claim_audit.phrases import CFIVALIDATION, NOCFIVALIDATION, GENERIC_NAMES


class AuditTests(unittest.TestCase):
    def test_claims(self):
        for phrase in CFIVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase.upper().replace(' ', '-')), (True, False))
        for phrase in NOCFIVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase), (False, True))
        self.assertEqual(claims("doesn't validate cfi"), (False, True))
        self.assertEqual(claims('```\nvalidate cfi\n```\n~~~\nno cfi validation\n~~~'), (False, False))
        self.assertEqual(claims('`validate cfi`'), (True, False))
        for value, expected in [('documented cfi validation claim false', (True, False)), ('cfi validation claim audit', (True, False)), ('documented no cfi validation claim false', (False, True))]:
            self.assertEqual(claims(value), expected)

    def test_library_routes(self):
        for method in ('validate', 'is_valid'):
            for code in ('from stdnum.cfi import {0}\n{0}(x)', 'from stdnum.cfi import {0} as v\nv(x)', 'import stdnum.cfi as c\nc.{0}(x)', 'import stdnum.cfi\nstdnum.cfi.{0}(x)', 'from stdnum import cfi\ncfi.{0}(x)', 'import stdnum\nstdnum.cfi.{0}(x)'):
                with self.subTest(method=method, code=code):
                    self.assertTrue(evidence(code.format(method)))
        for name in GENERIC_NAMES:
            for code in ('obj.{0}(x)', 'from somewhere import {0}\n{0}(x)', 'from somewhere import {0} as v\nv(x)', 'obj = factory()\nobj.{0}(x)'):
                with self.subTest(name=name, code=code):
                    self.assertTrue(evidence(code.format(name)))

    def test_non_evidence(self):
        cases = ['import stdnum.cfi', 'validate(x)', 'is_valid(x)', 'validate_cfi(x)', 'obj.validate(x)', 'obj.is_valid(x)', 'obj.cfi(x)', 'obj.compact(x)', 'obj.info(x)', 'from stdnum.cfi import compact\ncompact(x)', 'from stdnum.cfi import info\ninfo(x)', 'from stdnum import cfi\ncfi.compact(x)', 'from stdnum import cfi\ncfi.info(x)', 'import re\nre.match("[A-Z]{6}", x)', 'import re\nre.search("x", x)', 'import re\nre.fullmatch("x", x)', 'len(x) == 6', 'x[0] in "ED"', 'lookup_instrument(x)', 'generate_classification_code(x)', 'validators.cfi(x)', 'idutils.cfi(x)', 'validators.other.validate_cfi(x)', 'idutils.other.validate_cfi(x)', 'import subprocess\nsubprocess.run(["checker"])', '"validate cfi"', 'from stdnum.cfi import validate\nvalidate', 'def validate_cfi(x): pass\nobj.validate_cfi(x)', 'from stdnum.cfi import validate\nvalidate = other\nvalidate(x)', 'from stdnum import cfi\ncfi = other\ncfi.validate(x)', 'from stdnum import cfi\nwith ctx() as cfi:\n cfi.validate(x)', 'from stdnum.cfi import validate\ndef validate(x): pass\nvalidate(x)', 'from stdnum.cfi import validate\nvalidate(x']
        for module in ('isin', 'figi', 'cusip', 'sedol', 'isni', 'ean', 'luhn'):
            for method in ('validate', 'is_valid', 'calc_check_digit'):
                cases.append('from stdnum import {0}\n{0}.{1}(x)'.format(module, method))
        for code in cases:
            with self.subTest(code=code):
                self.assertFalse(evidence(code))

    def test_filesystem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'README.md').write_text('validate cfi')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
            (root/'tests').mkdir()
            (root/'tests/test_x.py').write_text('from stdnum.cfi import validate\nvalidate(x)')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            for folder in ('examples', 'fixtures', 'docs'):
                (root/folder).mkdir()
                (root/folder/'x.py').write_text('from stdnum.cfi import validate\nvalidate(x)')
            (root/'one.py').write_text('from stdnum.cfi import validate')
            (root/'two.py').write_text('validate(x)')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            (root/'link.py').symlink_to(root/'tests/test_x.py')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            (root/'prod.py').write_text('from stdnum.cfi import validate\nvalidate(x)')
            self.assertEqual(audit(root), [])
            (root/'README.md').write_text('no cfi validation')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
            self.assertEqual(audit(root, ['prod.py']), [])
            (root/'README.md').write_text('nothing')
            (root/'docs/claim.md').write_text('validate cfi')
            self.assertEqual(audit(root, ['prod.py'])[0]['severity'], 'MEDIUM')

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'README.md').write_text('validate cfi')
            def run(*args):
                return subprocess.run([sys.executable, '-m', 'cfi_validation_claim_audit', *args], capture_output=True, text=True)
            self.assertEqual(run('--version').stdout.strip(), '0.1.0')
            result = run('audit', str(root), '--json')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['findings'][0]['severity'], 'HIGH')
            (root/'test_x.py').write_text('from stdnum.cfi import validate\nvalidate(x)')
            self.assertEqual(run('audit', str(root)).returncode, 0)
            self.assertEqual(run('audit', str(root), '--fail-on', 'medium').returncode, 2)
            self.assertEqual(run('audit', str(root/'missing')).returncode, 1)
            self.assertEqual(run('audit', str(root), '--fail-on', 'HIGH').returncode, 1)
            self.assertEqual(run('audit', str(root), '--ignore', 'README.md').stdout.strip(), 'PASS')

    def test_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(claims((root/'README.md').read_text()), (False, False))
        self.assertEqual(audit(root), [])


if __name__ == '__main__':
    unittest.main()
