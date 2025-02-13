from muggwas import 1_compile_variants_by_gene as m1

def test_read_gff():
    gff_file = 'data/reference.gff'
    gene_dict = m1.read_gff(gff_file)
    assert gene_dict['gene1'] == {'start': 1, 'end': 100}
    assert gene_dict['gene2'] == {'start': 101, 'end': 200}
    assert gene_dict['gene3'] == {'start': 201, 'end': 300}