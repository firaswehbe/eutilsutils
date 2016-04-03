# pmid2csv.py 

Takes PMID list as input, generates a csv with information obtained using
`Bio.Entrez.eSummary()`

* Pubmed ID
* Title: Article title
* Source: Abbreviated journal name
* SO: A convenenience string for citation source that the NCBI esummary e-util
service generates.

Example run using `input/fhw.pmid` file as input

```bash
$ python pmid2csv.py input/fhw.pmids output/fhw.csv
['pmid2csv.py', 'input/fhw.pmids', 'output/fhw.csv']
Read ids from input/fhw.pmids: 14
...
Sending Entrez.epost() from the pmids file
...
WebEnv: NCID_1_13915340_165.112.9.37_9001_1459696530_1599083637_0MetA0_S_MegaStore_F_1
query_key: 1
...
Requesting Entrez.esummary() based on the epost
...
Got response of length: 14
Writing to output/fhw.csv
...
```

