import base64
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    if 'pdf' not in request.files:
        return jsonify({"error": "No 'pdf' file found in the request"}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        start = int(request.form.get('start', 1))
        end = int(request.form.get('end', 0)) 
    except ValueError:
        return jsonify({"error": "Start and end limits must be valid integers"}), 400

    try:
        pdf_bytes = file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = doc.page_count
        
        if end == 0 or end > total_pages:
            end = total_pages
            
        if start < 1 or start > end:
            return jsonify({"error": f"Invalid page range. Document has {total_pages} pages."}), 400

        output_images = []

        for i in range(start - 1, end):
            page = doc[i]
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            b64_string = base64.b64encode(img_bytes).decode('utf-8')
            
            output_images.append({
                "page": i + 1,
                "image_data": f"data:image/png;base64,{b64_string}" 
            })

        doc.close() 
        return jsonify({"images": output_images}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while processing the PDF: {str(e)}"}), 500


@app.route('/extract_subsections', methods=['POST'])
def extract_subsections():
    if 'pdf' not in request.files:
        return jsonify({"error": "No 'pdf' file found in the request"}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        start = int(request.form.get('start', 1))
        end = int(request.form.get('end', 0)) 
    except ValueError:
        return jsonify({"error": "Start and end limits must be valid integers"}), 400

    try:
        pdf_bytes = file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = doc.page_count
        
        if end == 0 or end > total_pages:
            end = total_pages
            
        if start < 1 or start > end:
            return jsonify({"error": f"Invalid page range. Document has {total_pages} pages."}), 400
        
        found_subsections = []
        seen_section_numbers = set() 
        
        regex_pattern = re.compile(r"^\s*(\d+\.\d+(?:\.\d+)*)\s+(.+)$", re.MULTILINE)

        for page_num in range(start - 1, end):
            text = doc[page_num].get_text("text")
            matches = regex_pattern.finditer(text)
            
            for match in matches:
                section_num = match.group(1)
                title = match.group(2).strip()
                
                if section_num not in seen_section_numbers:
                    seen_section_numbers.add(section_num)
                    found_subsections.append({
                        "section_number": section_num,
                        "title": title,
                        "page": page_num + 1 
                    })

        doc.close()
        
        return jsonify({
            "subsections": found_subsections,
            "total_subsections_found": len(found_subsections)
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while extracting text: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)