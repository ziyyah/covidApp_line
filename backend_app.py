
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absensi_proyek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mandor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))


class Proyek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    mandor_id = db.Column(db.Integer, db.ForeignKey('mandor.id'))


class Pekerja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    posisi = db.Column(db.String(50))
    proyek_id = db.Column(db.Integer, db.ForeignKey('proyek.id'))


class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pekerja_id = db.Column(db.Integer, db.ForeignKey('pekerja.id'))
    tanggal = db.Column(db.Date)
    status_kehadiran = db.Column(db.String(50))


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    mandor = Mandor.query.filter_by(username=data['username'], password=data['password']).first()
    if mandor:
        return jsonify({"message": "Login berhasil", "mandor_id": mandor.id})
    return jsonify({"message": "Username atau password salah"}), 401


@app.route('/pekerja/<int:mandor_id>', methods=['GET'])
def get_pekerja(mandor_id):
    proyek = Proyek.query.filter_by(mandor_id=mandor_id).all()
    pekerja = []
    for p in proyek:
        pekerja += Pekerja.query.filter_by(proyek_id=p.id).all()
    return jsonify([{"id": p.id, "nama": p.nama, "posisi": p.posisi, "proyek_id": p.proyek_id} for p in pekerja])


@app.route('/absensi', methods=['POST'])
def input_absensi():
    data = request.json
    absensi = Absensi(
        pekerja_id=data['pekerja_id'],
        tanggal=datetime.strptime(data['tanggal'], '%Y-%m-%d'),
        status_kehadiran=data['status_kehadiran']
    )
    db.session.add(absensi)
    db.session.commit()
    return jsonify({"message": "Absensi berhasil ditambahkan!"})


@app.route('/gaji/<int:mandor_id>', methods=['GET'])
def hitung_gaji(mandor_id):
    tanggal_mulai = request.args.get('tanggal_mulai')
    tanggal_akhir = request.args.get('tanggal_akhir')
    proyek = Proyek.query.filter_by(mandor_id=mandor_id).all()
    pekerja_ids = [p.id for p in Pekerja.query.filter(Pekerja.proyek_id.in_([p.id for p in proyek])).all()]
    absensi = Absensi.query.filter(
        Absensi.pekerja_id.in_(pekerja_ids),
        Absensi.tanggal.between(tanggal_mulai, tanggal_akhir),
        Absensi.status_kehadiran == "Hadir"
    ).all()

    gaji = {}
    for a in absensi:
        pekerja = Pekerja.query.get(a.pekerja_id)
        gaji[pekerja.nama] = gaji.get(pekerja.nama, 0) + 100000

    return jsonify(gaji)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
