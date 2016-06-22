from pandas import read_csv

from numpy import empty

from .plink import read_bed_item
from .plink import read_bed_intidx

from .plink import read_map

from ..matrix import MatrixInterface
from ..table import Table

def _read_fam(filepath):
    column_names = ['family_id', 'individual_id', 'paternal_id', 'maternal_id',
                    'sex', 'phenotype']
    column_types = [bytes, bytes, bytes, bytes, bytes, float]


    df = read_csv(filepath, header=None, sep=r'\s+', names=column_names,
                  dtype=dict(zip(column_names, column_types)))
    table = Table(df)

    fid = table['family_id']
    iid = table['individual_id']
    n = table.shape[0]
    table.index_values = [fid[i] + '_' + iid[i] for i in range(n)]
    table.index_name = 'sample_id'

    return table

class BEDMatrix(MatrixInterface):
    def __init__(self, filepath, sample_ids, marker_ids):
        shape = (len(sample_ids), len(marker_ids))
        allelesA = None
        allelesB = None
        super(BEDMatrix, self).__init__(sample_ids, marker_ids,
                                        allelesA, allelesB, shape)

        self._filepath = filepath

    def _item(self, sample_id, marker_id):
        r = self._sample_map[sample_id]
        c = self._marker_map[marker_id]
        return read_bed_item(self._filepath, r, c, self.shape)

    @property
    def dtype(self):
        return int

    def _array(self, sample_ids, marker_ids):

        sample_idx = self._sample_map[sample_ids]
        marker_idx = self._marker_map[marker_ids]

        G = empty((len(sample_idx), len(marker_idx)))
        read_bed_intidx(self._filepath, sample_idx, marker_idx, self.shape, G)

        return G

def reader(basepath):
    sample_tbl = _read_fam(basepath + '.fam')
    marker_tbl = read_map(basepath + '.map')
    G = BEDMatrix(basepath + '.bed', sample_tbl.index_values,
                marker_tbl.index_values)
    return (sample_tbl, marker_tbl, G)
