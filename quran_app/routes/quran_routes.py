from flask import Blueprint, jsonify, request
from models import QuranService,DoaService

# Blueprint
quran_bp = Blueprint('quran', __name__, url_prefix='/api')

# Services
quran_service = QuranService()
doa_service = DoaService()

@quran_bp.route('/surat', methods=['GET'])
def get_all_surat():
    data = quran_service.get_all_surat()
    return jsonify({"status": "success", "total": len(data), "data": data})

@quran_bp.route('/surat/<int:nomor>', methods=['GET'])
def get_surat_detail(nomor):
    data = quran_service.get_surat_by_nomor(nomor)
    if data:
        return jsonify({"status": "success", "data": data})
    return jsonify({"status": "error", "message": "Not found"}), 404

@quran_bp.route('/surat/juz/<int:juz>', methods=['GET'])
def get_surat_by_juz(juz):
    all_surat = quran_service.get_all_surat()
    filtered = [s for s in all_surat if s.get('juz') == juz]
    return jsonify({"status": "success", "juz": juz, "total": len(filtered), "data": filtered})

@quran_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({"status": "error", "message": "Query required"}), 400
    results = quran_service.search(q)
    return jsonify({"status": "success", "keyword": q, "total": len(results), "data": results})

@quran_bp.route('/doa', methods=['GET'])
def get_all_doa():
    data = doa_service.get_all_doa()
    return jsonify({"status": "success", "total": len(data), "data": data})

@quran_bp.route('/doa/random', methods=['GET'])
def get_random_doa():
    doa = doa_service.get_random_doa()
    return jsonify({"status": "success", "data": doa})

@quran_bp.route('/doa/daily', methods=['GET'])
def get_daily_doa():
    doa = doa_service.get_daily_doa()
    return jsonify({"status": "success", "data": doa})

@quran_bp.route('/info', methods=['GET'])
def get_info():
    return jsonify({
        "status": "success",
        "data": {
            "name": "Al-Qur'an Digital",
            "version": "3.0.0",
            "total_surat": quran_service.get_total_surat(),
            "total_doa": doa_service.get_total_doa(),
            "features": ["114 Surat", "30 Juz", "Dark Mode", "Doa Harian",]
        }
    })