from os.path import dirname
from os.path import join
from os.path import realpath

import limix_reader as limr

def test_case1():
    root = dirname(realpath(__file__))
    root = join(root, 'data', 'case1')

    marker_csv = limr.reader.csv(join(root, 'marker.csv'), row_header=True,
                                 col_header=True)


    sample_csv = limr.reader.csv(join(root, 'sample.csv'), row_header=True,
                                 col_header=True)


    G_hdf5_1 = limr.reader.h5(join(root, 'hdf5-1.h5'), '/G', genotype=True)
    G_hdf5_2 = limr.reader.h5(join(root, 'hdf5-2.h5'), '/G', genotype=True)

    G_hdf5_1.sample_ids = limr.fetch.h5(join(root, 'hdf5-1.h5'), '/sample_ids')
    G_hdf5_2.sample_ids = limr.fetch.h5(join(root, 'hdf5-2.h5'), '/sample_ids')

    G_hdf5_1.marker_ids = limr.fetch.h5(join(root, 'hdf5-1.h5'), '/marker_ids')
    G_hdf5_2.marker_ids = limr.fetch.h5(join(root, 'hdf5-2.h5'), '/marker_ids')

    print("")
    # print(G_hdf5_1)
    # print(G_hdf5_2)
    # G_hdf5_1.col_header =

    ped = limr.reader.ped(join(root, 'example'))
    pass

# test_case1()
