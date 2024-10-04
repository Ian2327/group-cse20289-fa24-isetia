from flask import Flask, request, send_file, jsonify
import checktests, os, subprocess, gogo

app = Flask(__name__)

ndid = 902275643
port = (54000 + (ndid % 150))


def create_pdf(year, month, interface):
    prepend = ""
    docx = f"{prepend}{year}-{month}-{'Wired' if interface == 'eth0' else 'WiFi'}.docx"
    docx_extra = f"{prepend}{year}-{month}-{'WiFi' if interface == 'eth0' else 'Wired'}.docx"
    pdf = f"{prepend}{year}-{month}-{'Wired' if interface == 'eth0' else 'WiFi'}.pdf"
        
    if not os.path.exists(pdf):
        if not os.path.exists(docx):
            url = "http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-all.json"
            text = "intro.txt"
            checktests.process_data(year, month, text, url, False, prepend)
        if os.path.exists(docx):
            try:
                gogo.convert(docx, pdf)
                os.remove(docx)
                os.remove(docx_extra)
            except Exception as e:
                return f"Error create PDF: {e}"
        else:
            return "Failed to create docx"
    return pdf

@app.route('/hw04', methods=['GET'])
def retrieve_pdf():
    year = request.args.get('year')
    month = request.args.get('month')
    interface = request.args.get('interface')

    if not year or not month or not interface:
        return jsonify({"Error": "Missing year, month, or interface."}), 400
    
    try:
        year = int(year)
        month = int(month)
    except:
        return jsonify({"Error": "Invalid year or month format."}), 400
        
    if interface not in ['eth0', 'wlan0']:
        return jsonify({"Error":"Invalid interface."}), 400

    pdf_path = create_pdf(year, month, interface)
    
        
    if isinstance(pdf_path, str) and not os.path.exists(pdf_path):
            return jsonify({"Error": pdf_path}), 500

    try:
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
