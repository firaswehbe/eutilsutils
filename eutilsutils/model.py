import sqlalchemy as SA
import sqlalchemy.orm as SAORM

EutilsUtilsBaseModel = SAORM.declarative_base()

class PMPaper(EutilsUtilsBaseModel):
    __tablename__ = 'pm_paper'

    id = SA.Column(SA.Integer, primary_key=True)
    title = SA.Column(SA.String(500))
    journal = SA.Column(SA.String(250))
    pubdate_y = SA.Column(SA.Integer)
    pubdate_medline = SA.Column(SA.String(50))
    edat = SA.Column(SA.Date)