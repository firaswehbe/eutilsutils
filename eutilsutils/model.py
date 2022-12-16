import sqlalchemy as SA
import sqlalchemy.orm as SAORM

EutilsUtilsBaseModel = SAORM.declarative_base()

class PMPaper(EutilsUtilsBaseModel):
    __tablename__ = 'pm_paper'

    id = SA.Column(SA.Integer, primary_key=True)
    title = SA.Column(SA.String(500))
    pdat = SA.Column(SA.Date)
    edat = SA.Column(SA.Date)