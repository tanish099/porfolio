from flask import Flask, render_template, request, redirect, url_for, make_response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)

user_data = {}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    global user_data
    user_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "skills": request.form['skills'],
        "projects": request.form['projects'],
        "about": request.form['about']
    }
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template("profile.html", data=user_data)

@app.route('/download_resume')
def download_resume():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"<b>{user_data['name']}</b>", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Email: {user_data['email']}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"About: {user_data['about']}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Skills: {user_data['skills']}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Projects: {user_data['projects']}", styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True)