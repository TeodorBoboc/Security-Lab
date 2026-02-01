# Security Lab - Learning Project

## Descriere
    Acesta este primul meu proiect web.
    
    Scopul proiectului este de a învăța fluxul real al unei aplicații, de la frontend
    până la backend și securitate.
    Proiectul se concentrează pe structura repetitivă: Create -> Break -> Fix.

    Am folosit pas cu pas:
    - Frontend: HTML, CSS, Jinja2, Bootstrap.
    - Backend: Python, Flask, Flask-WTF.
    - (Urmează) Database & Securitate.

---

## Scopul Proiectului
    - Să învăț Flask și structura unei aplicații web.
    - Înțelegerea metodelor HTTP.
    - Implementarea unui sistem de autentificare (login / register).
    - Crearea și manipularea unei baze de date.
    - Identificarea vulnerabilităților unui site.
    - Securizarea unui site.
    - Învățare Linux.

---

## Funcționalități Implementate
    - Pagina Home cu postări.
    - Pagina Home,About,Account.
    - Optimizare la incarcarea de poze.
    - Sistem de Înregistrare/Login.
    - Sistem poza de profil 
    - Afișare username în navbar. 
    - Mesaje flash.
    - Template layout comun.

---

## În lucru
    - Paginare
    - Testare vulnerabilități.
    - Securizare site.

---

## BUGS
    1. Problema Importului Circular (Circular Dependency):
        - În etapa de separare logică a fișierelor, m-am lovit de o problemă în Python.
            Am încercat să mut clasele User și Post în models.py pentru o organizare mai bună.
            - App.py importa user din models.py.
            - models.py importa db din App.py.
        - Am primit eroarea: **ImportError: cannot import name 'db' from 'App'**.
        - Când rulam App.py, fișierul primea numele __main__. Astfel, când models.py căuta from App import db, nu găsea fișierul App deoarece acesta rula deja, provocând eroarea.
        - În cuvinte:
            - Când rulăm App.py, acesta devine __main__, iar în models.py apelăm from App import db, dar App acum este __main__, deci nu știe unde să se uite.

        --SOLUȚIA--
            - Folosim Package Structure!
            
            - Am creat un folder principal (ex: App_pk) și am adăugat în el fișierul __init__.py (Fișierul __init__.py este un fișier special în Python folosit pentru a marca un director ca pachet Python și pentru a rula cod de inițializare atunci când acel pachet este importat). Acesta îi spune lui Python că folderul este un pachet.
            
            - Am mutat inițializarea obiectelor App și db în fișierul __init__.py.
            
            - Eliminarea Ciclicității: Am modificat importurile în models.py și routes.py pentru a prelua obiectele direct din pachet (from App_pk import app, db), nu dintr-un fișier individual.

            - Importul la final: În __init__.py, am plasat from App_pk import routes la sfârșitul fișierului. Această tehnică asigură că app și db sunt deja inițializate înainte ca rutele să încerce să le acceseze.

            - Punctul de Intrare (Entry Point): Am creat un fișier principal (App.py situat în folderul rădăcină) care are rolul unic de a porni serverul. Acesta doar importă aplicația configurată din pachet: from App_pk import app.
    
    2. Securitatea Parolelor si Prevenirea Timing Attacks:
        -Initial m-am gandit sa salvez in baza de date parolele in "plain text", insa acest lucru reprezinta o vulnerabilitate critica de securitate.Daca baza de date este compromisa, toate conturile devin accesibile de catre atacator.
        -Cea mai buna solutie este de a transforma parola intr un HASH de 60 de caractere asa cum am precizat in models.User folosind Flask-Bcrypt.
        -In terminal am primit eroare *Invalid salt* aparuta in: return hmac.compare_digest(bcrypt.hashpw(password, pw_hash), pw_hash)
        CAUZA ERORII:
            -In terminal am accesat python, am creat variabila hash_pw = bcrypt.generate_password_hash('test')
            -Am apelat functia de verificare bcrypt.check_password_hash('hash_pw', 'parola')
            -Rezultat:Python a incercat sa compare parola cu TEXTUL "hash_pw".
            -Deoarece testul "hash_pw" nu continea un SALT valid (prefixul $2b$12$... care ii spune functiei cum a fost creeat hash ul) s-a prabusit
            --SOLUTIE--
                -Ca prim parametru folosim variabila, fara ghilimele :)
            
            
            !!!Deep Dive: De ce hmac.compare_digest?!!!
                -Functia simpla hash_pw = bcrypt.generate_password_hash('test') v-a returna ex:
                        b'$2b$12$xpe0r7gN2bmC9O3mwtV.2OQRRvkZBXCv/fV.7uPtpdhvO6sVE0Tca'
                acest b | ne spune ca parola a fost ENCODED adica din text in biti, eu vreau sa compar doua stringuri.
                --SOLUTIE--
                    -la sfarsitul functiei adaugam .decode(utf-8) pentru a-l stoca ca si string care va face DECODE adica din biti in text
            
            !!!Vulnerabilitati!!!
                --TIMING ATTACKS--  
                -Analizand sursa erorii am descoperit ca Python nu folsoeste operatorul == pentru parole.
                -Operatorul == se opreste la prima litera gresita (VITEZA VARIABILA).Un ataacator poate masura timpul de raspundere pentru a ghici parola caracter cu caracter.
                -In documentatia HMAC apare compare_digest (https://docs.python.org/3/library/hmac.html) aceasta functie ofera un timp de comparatie constant spre deosebire de ==.
    
    3. Fenomenul de "Double Submit" și Prevenirea Re-trimiterii Formularelor:
        Problema: După procesarea unui formular (ex: Update Account sau Register), dacă serverul returnează direct o pagină folosind render_template, browserul păstrează datele formularului în memoria cache a cererii curente.

        CAUZA ERORII:
            -Dacă utilizatorul apasă Refresh (F5) după ce a primit confirmarea succesului, browserul va încerca să execute din nou ultima cerere (POST), afișând adesea un mesaj de avertizare: "Confirm Form Resubmission".

            Consecințe:
                -Dacă userul apasă "Yes", datele sunt trimise a doua oară.
                -În cazul înregistrării, baza de date va arunca o eroare de tipul IntegrityError deoarece va încerca să creeze un user duplicat (Username/Email deja existente).
                -Aplicația se va prăbuși cu un 500 Internal Server Error dacă eroarea nu este prinsă.

            --SOLUȚIA: PRG Pattern (Post/Redirect/Get)--
                -Logica de implementare:
                    -În loc să afișăm direct template-ul după succesul form.validate_on_submit(), folosim funcția redirect(url_for(...)).
                    -Această instrucțiune trimite un cod de stare HTTP 302 către browser, forțându-l să facă o cerere nouă de tip GET către o altă rută (sau chiar către aceeași rută, dar "curată").

            Efectul:
            -Datele sensibile din formular sunt eliminate din istoricul imediat al browserului.
            -Acum, dacă utilizatorul dă Refresh, el doar re-solicită pagina prin GET, fără a mai trimite datele de POST.
        
            !!! Deep Dive: De ce e vital pentru user experience? !!!
                -Pe lângă prevenirea erorilor de bază de date, acest pattern previne situațiile penibile în care un utilizator ar putea plăti de două ori pentru un produs (într-un magazin online) sau ar putea posta același comentariu de mai multe ori printr-un simplu refresh accidental.

---     

