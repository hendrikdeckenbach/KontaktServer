from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

form_html = """
<!doctype html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <title>Daten-Eingabe</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
     <style>
  .form-check-input {
    outline: 1px solid #333333; /* leichter blauer Rahmen um die Checkbox */
    border-radius: 0.25rem;
    width: 1.2rem;
    height: 1.2rem;
    transition: box-shadow 0.2s;
  }

  .form-check-input:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* leichter Schatten beim Fokus */
  }
</style>

  </head>
  <body class="bg-light">

<script>
window.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const errorDiv = document.getElementById("tel-error");
    const lebensstilDiv = document.getElementById("lebensstilFrage");

    // Telefon-Prüfung
    form.addEventListener("submit", function(event) {
        const tel = document.querySelector("input[name='tel']").value.trim();
        const telPattern = /^\\+\\d{10,14}$/;
        if (!telPattern.test(tel)) {
            errorDiv.textContent = "Die eingegebene Telefonnummer konnte nicht gefunden werden. Richtig wäre z.B. +4915123456789.";
            errorDiv.style.display = "block";
            event.preventDefault();
        } else {
            errorDiv.style.display = "none";
        }
    });

    // Polizei Ja/Nein -> Lebensstil anzeigen
    const polizeiRadios = document.querySelectorAll("input[name='polizei']");
    polizeiRadios.forEach(radio => {
        radio.addEventListener("change", function() {
            if (document.getElementById("polizeiJa").checked) {
                lebensstilDiv.style.display = "block";
            } else {
                lebensstilDiv.style.display = "none";
            }
        });
    });
});
</script>

<div class="container py-5">
  <div class="row gx-4">
    <!-- Formular links -->
    <div class="col-lg-7 mb-4">
      <div class="card shadow p-4" style="border-radius: 1rem;">
        <h2 class="mb-4 text-center">Mache einen unverbindlichen Ersttermin mit uns aus</h2>
        <form method="post" action="/submit">

      <!-- Name -->
      <div class="mb-3">
        <label class="form-label">Wie ist dein Name?</label>
        <input type="text" class="form-control" name="name" required>
      </div>

      <!-- Email -->
      <div class="mb-3">
        <label class="form-label">Wie lautet deine E-Mail Adresse?</label>
        <input type="email" class="form-control" name="email" required>
      </div>

      <!-- Telefonnummer -->
      <div class="mb-3">
        <label class="form-label">Unter welcher Telefonnummer können wir dich erreichen? <small class="text-danger">Wichtiges Pflichtfeld*</small></label>
        <input type="text" class="form-control" name="tel" placeholder="inkl. Vorwahl, z.B. +49" required>
        <div id="tel-error" class="text-danger mt-1" style="display:none;"></div>
      </div>

      <!-- Polizei/Lehrkraft Ja/Nein -->
      <div class="mb-3">
        <label class="form-label">Bist du bei der Polizei oder als Lehrkraft tätig?</label><br>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="polizei" id="polizeiJa" value="Ja">
          <label class="form-check-label" for="polizeiJa">Ja</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="polizei" id="polizeiNein" value="Nein">
          <label class="form-check-label" for="polizeiNein">Nein</label>
        </div>
      </div>

      <!-- Themen / Interessen -->
      <div class="mb-3">
        <label class="form-label">Welche Themen interessieren dich? (Mehrfachauswahl möglich)</label><br>

        <div class="form-check" id="lebensstilFrage" style="display:none">
          <input class="form-check-input" type="checkbox" name="themen" value="Pension">
          <label class="form-check-label">Wie kann ich in der Pension meinen Lebensstil beibehalten, ohne jetzt auf viel zu verzichten?</label>
        </div>

        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="themen" value="Absicherung">
          <label class="form-check-label">Wie sichere ich mich optimal ab, ohne zu viel zu bezahlen?</label>
        </div>

        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="themen" value="Investieren">
          <label class="form-check-label">Wie kann ich mein Geld sinnvoll investieren und vor der Inflation schützen?</label>
        </div>

        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="themen" value="Immobilie">
          <label class="form-check-label">Wie kann ich mir meine Traumimmobilie leisten, trotz der aktuell sehr schwierigen Zinslage?</label>
        </div>

        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="themen" value="Förderung">
          <label class="form-check-label">Wie erhalte ich mehr Förderung und Steuervorteile für meinen Vermögensaufbau?</label>
        </div>

        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="themen" value="ProfiInvest">
          <label class="form-check-label">Wie kann ich ohne Aufwand, wie ein Profiinvestor in Immobilien investieren?</label>
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100">Jetzt beraten lassen</button>

    </form>
  </div>
</div>

    <!-- Kontaktkarte rechts -->
    <div class="col-lg-5 mb-4">
      <div class="card shadow p-4" style="border-radius: 1rem;">
        <!-- Foto -->
  
        
        <h5 class="card-title mb-3">Kontaktiere deinen Ansprechpartner</h5>
<div class="d-flex align-items-center mb-3">
  <img src="https://i.imgur.com/ietiTHb.jpeg" alt="Foto Max Mustermann" class="rounded-circle me-3" style="width:150px; height:150px; object-fit:cover;">
  <div>
    <strong>Marc-Hendrik André Deckenbach</strong><br>
    <span>Gärtnerweg 10</span><br>
    <span>63110 Rodgau</span><br>
    <span>Telefon: +49 173 873 862 8</span><br>
    <span>E-Mail: hendrik.deckenbach@gmail.com</span>
  </div>
</div>
<a href="mailto:hendrik.deckenbach@gmail.com" class="btn btn-primary w-100 mt-3">Per E-Mail Kontaktieren</a>

      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

@app.route("/")
def form():
    return render_template_string(form_html)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    tel = request.form.get("tel")
    polizei = request.form.get("polizei")
    themen = request.form.getlist("themen")  # mehrere ausgewählte Optionen


    msg_text = f"Neue Daten:\nName: {name}\nEmail: {email}\nTelefon: {tel}\nPolizei oder Lehrkraft: {polizei}\nThemen: {', '.join(themen)}"
    msg = MIMEText(msg_text)
    msg["Subject"] = "Neue Eingabe von Website"
    msg["From"] = "hendrik.deckenbach@gmail.com"
    msg["To"] = "hendrik.deckenbach@gmail.com"

    # Bestätigungsmail an den User
    confirm_text = f"Hallo {name},\n\nVielen Dank für deine Eingabe. Wir haben folgende Daten erhalten:\n\nName: {name}\nTelefon: {tel}\nPolizei oder Lehrkraft: {polizei}\nThemen: {', '.join(themen)}\n\nBeste Grüße!"
    confirm_msg = MIMEText(confirm_text)
    confirm_msg["Subject"] = "Bestätigung deiner Eingabe"
    confirm_msg["From"] = "hendrik.deckenbach@gmail.com"
    confirm_msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("hendrik.deckenbach@gmail.com", "ouou bshp ffys zbdx")
        server.send_message(msg)
        server.send_message(confirm_msg)  # an den User


    return "<h3 style='text-align:center; margin-top:50px;'>Danke! Deine Daten wurden übermittelt ✅</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
