# pmid2pmcid.py 

Takes PMID list as input, generates a csv with information obtained using
`Bio.Entrez.eSummary()`

* Pubmed ID as `pmid`
* PMCID as `pmcid`

Example run using `input/fhw.pmid` file as input

```bash
$ python pmid2csv.py input/fhw.pmids output/fhw.csv
```

