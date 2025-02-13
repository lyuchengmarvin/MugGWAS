from muggwas import 1_compile_variants_by_gene as m1

def test_read_gff():
    gff_file = 'data/reference.gff'
    gene_dict = m1.read_gff(gff_file)
    assert gene_dict['gene1'] == {'start': 1, 'end': 100}
    assert gene_dict['gene2'] == {'start': 101, 'end': 200}
    assert gene_dict['gene3'] == {'start': 201, 'end': 300}

def test_read_vcf():
    vcf_file = 'data/sample.vcf'
    gene_dict = m1.read_gff('data/reference.gff')
    variant_dict = m1.read_vcf(vcf_file, gene_dict)
    assert variant_dict['gene1'] == {'A': 1, 'T': 1}
    assert variant_dict['gene2'] == {'C': 1, 'G': 1}
    assert variant_dict['gene3'] == {'A': 1, 'T': 1}
