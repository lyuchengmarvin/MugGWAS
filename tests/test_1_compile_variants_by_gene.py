import unittest
import sys
import os

# Add the scripts folder to the python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))

from compile_variants_by_gene import extract_gene_positions, parse_vcf

class TestCompileVariantsByGene(unittest.TestCase):

    def test_extract_gene_positions(self):
        gff_file = 'tests/test.gff'
        expected_output = {
            'gene1': {'contig1': (100, 200)},
            'gene2': {'contig1': (300, 400)},
            'CDS1': {'contig2': (500, 600)}
        }
        result = extract_gene_positions(gff_file)
        self.assertEqual(result, expected_output)

    def test_gene_spanning_multiple_contigs(self):
        """Test handling of genes that span multiple contigs."""
        # create a test GFF file with a gene spanning multiple contigs
        test_gff_path = 'tests/test_multicontig.gff'
        with open(test_gff_path, 'w') as f:
            f.write("""##gff-version 3
            contig1\tprediction\tgene\t100\t200\t.\t+\t.\tID=multicontig_gene
            contig2\tprediction\tgene\t50\t150\t.\t+\t.\tID=multicontig_gene
            contig1\tprediction\tCDS\t300\t400\t.\t+\t.\tID=single_gene
            """)
            
        try:
            result = extract_gene_positions(test_gff_path)
            expected_output = {
                'multicontig_gene': {
                    'contig1': (100, 200),
                    'contig2': (50, 150)
                },
                'single_gene': {
                    'contig1': (300, 400)
                }
            }
            self.assertEqual(result, expected_output)
        finally:
            if os.path.exists(test_gff_path):
                os.remove(test_gff_path)
            
    def test_duplicate_gene_ids(self):
        """Test handling of duplicate gene IDs with different positions."""
        # create a test GFF file with duplicate gene IDs
        test_gff_path = 'tests/test_duplicate.gff'
        with open(test_gff_path, 'w') as f:
            f.write("""##gff-version 3
            contig1\tprediction\tgene\t100\t200\t.\t+\t.\tID=duplicate_gene
            contig1\tprediction\tgene\t300\t400\t.\t+\t.\tID=duplicate_gene
            contig2\tprediction\tCDS\t500\t600\t.\t+\t.\tID=unique_gene
            """)
            
        try:
            result = extract_gene_positions(test_gff_path)
            # the function should preserve both positions for the duplicate gene ID
            expected_output = {
                'duplicate_gene': {
                    'contig1': [(100, 200), (300, 400)]  #should store both positions
                },
                'unique_gene': {
                    'contig2': (500, 600)
                }
            }
            self.assertEqual(result, expected_output)
        finally:
            if os.path.exists(test_gff_path):
                os.remove(test_gff_path)

    def test_parse_vcf(self):
        vcf_file = 'tests/test.vcf.gz'
        expected_output = {
            'chr1:100:A:T': {'sample1': (0, 1), 'sample2': (1, 1)},
            'chr1:200:G:C': {'sample1': (0, 0), 'sample2': (0, 1)}
        }
        result = parse_vcf(vcf_file)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
