from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail, Message
from models import db, User, Recommendation
from forms import RecommendationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Remplacez par votre serveur SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Votre email
app.config['MAIL_PASSWORD'] = 'your_password'  # Votre mot de passe
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RecommendationForm()
    if form.validate_on_submit():
        # Enregistrement de la recommandation
        recommendation = Recommendation(content=form.content.data)
        db.session.add(recommendation)
        db.session.commit()
        
        # Envoi de l'email
        msg = Message('Nouvelle Recommandation', sender='your_email@example.com', recipients=['recipient@example.com'])
        msg.body = f'Nouvelle recommandation: {form.content.data}'
        mail.send(msg)

        return redirect(url_for('index'))
    return render_template('index.html', form=form)
