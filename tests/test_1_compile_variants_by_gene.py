import unittest
import sys
import os

# Add the scripts folder to the python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))

from compile_variants_by_gene import extract_gene_positions, parse_vcf

class TestCompileVariantsByGene(unittest.TestCase):

    def test_extract_gene_positions(self):
        gff_file = 'test.gff'
        expected_output = {
            'gene1': {'contig1': (100, 200)},
            'gene2': {'contig1': (300, 400)},
            'CDS1': {'contig2': (500, 600)}
        }
        result = extract_gene_positions(gff_file)
        self.assertEqual(result, expected_output)

    def test_parse_vcf(self):
        vcf_file = 'test.vcf.gz'
        expected_output = {
            'chr1:100:A:T': {'sample1': (0, 1), 'sample2': (1, 1)},
            'chr1:200:G:C': {'sample1': (0, 0), 'sample2': (0, 1)}
        }
        result = parse_vcf(vcf_file)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()