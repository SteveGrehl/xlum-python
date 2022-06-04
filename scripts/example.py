import logging
import os
DIRNAME = os.path.dirname(__file__)
import sys
sys.path.append(
    os.path.join(
        DIRNAME,
        '../xlum')
)
import importer


def main():
    logging.basicConfig(level=logging.DEBUG)

    obj = importer.from_xlum(
        os.path.join(
            DIRNAME, 
            "../assets/xlum_example.xlum"
        )
        # "/Users/sgrehl/Documents/GIT/xlum/R-package/xlum_v2/inst/extdata/xlum_example.xlum"
        # "/Users/sgrehl/Downloads/BDX16646_OSL_SAR.xlum"
        # "/Users/sgrehl/Downloads/BDX16646_RF70.xlum"
    )
    logging.debug(obj)

if __name__ == '__main__':
    main()