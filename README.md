# eutilsutils

Utilities for [Entrez E-Utilities](http://www.ncbi.nlm.nih.gov/books/NBK25500/)
based on [BioPython](http://biopython.org/wiki/Main_Page).

## Notebooks

Some explanation of how to run BioPython and some of the code written in this
repo will be demonstrated in Jupyter Notebooks which can be [viewed
here](notebooks/).

## Scripts

The [scripts](scripts/) directory will have some general utility scripts for
testing the code or to demonstrate the functionality.

* [pmid2csv.py](scripts/pmid2csv.md): Takes as input a file with pubmed IDs and
creates csv file with publication data
* [pmid2pmcid.py](scripts/pmid2pmcids.md): Takes as input a file with pubmed IDs
and creates a csv file with added PMCIDs.

## Installation and Running

Easy:

* Download and install [Anaconda](https://www.continuum.io/downloads).
* Clone this repo
* Load the conda environment that I created with all the package dependencies
as follows:

```bash
$ conda env create -f config/eutilsutils.yml
```

* Run the scripts and notebooks under this environment. I'll make sure all
dependencies are always included.

