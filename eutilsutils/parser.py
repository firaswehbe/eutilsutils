from eutilsutils.model import PMPaper
from eutilsutils import EutilsUtils

class PMPaperLoadError (RuntimeError):
    """Thrown when reading PM records that don't map to our schema"""
    pass

def loadEfetch2PMPapers(eutilsutilsobj, efetch_result, skip_existing=True):
    """
    Should return a list indicating parsed/loaded or retrieved instances in database
    """
    if getattr(efetch_result,'tag',None) != 'PubmedArticleSet':
        raise PMPaperLoadError('Wrong root tag for efetch')
    mypmpaper_list = []
    with eutilsutilsobj.db.session_maker.begin() as mysession:
        for mypmarticle in efetch_result['PubmedArticle']:
            # These two nested keys should be required per DTD
            # If not, a raised key error should break the session
            mymedlinecitation = mypmarticle['MedlineCitation']
            mypmid = str(mymedlinecitation['PMID'])
            myPMPaper = mysession.get(PMPaper,mypmid)
            if myPMPaper is not None and skip_existing:
                # We just did a database look up; keep track of cost in large batches
                # If record in database add it to container, print message, and skip
                mypmpaper_list.append((mypmid,'in db - loaded from db only'))
                print(f"PMID: {mypmid} exists in the database, skipping...")
                continue
            elif myPMPaper is None:
                mypmpaper_list.append((mypmid,'not in db - parsed and inserted'))
                myPMPaper = PMPaper(id=mypmid)
            else:
                mypmpaper_list.append((mypmid,'in db - parsed and updated'))
            # Session.merge() returns the new object loaded/created in session, use that going forward
            myPMPaper = mysession.merge(myPMPaper) 
            myPMPaper.title = mymedlinecitation['Article']['ArticleTitle']
            # Add other attributes later


    # Should commit session or rollback at the end of the begin() context
    # Should close the session as well given the construct used to start the context

    return mypmpaper_list
