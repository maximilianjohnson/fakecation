from fakecation import db

class Image(db.Model):
    __tablename__ = "image_db"

    image_ID = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    number_ppl = db.Column(db.Integer)
    genders = db.Column(db.String(100))
    filepath = db.Column(db.String(100))

    def __init__(self, lat, lon, num, genders, fp):
        self.latitude = lat
        self.longitude = lon
        self.number_ppl = num
        self.genders = str(genders)
        self.filepath = fp
        
