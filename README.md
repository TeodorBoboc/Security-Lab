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
    - Pagina Home cu postări (dummy).
    - Pagina About.
    - Sistem de Înregistrare/Login.
    - Afișare username în navbar (dummy). 
    - Mesaje flash.
    - Template layout comun.

---

## În lucru
    - Înregistrare bază de date (Flask-SQLAlchemy).
    - Parole hash.
    - Flask-login.
    - Creare postări reale.
    - Testare vulnerabilități.
    - Securizare site.

---

## BUGS
    1. Problema Importului Circular (Circular Dependency)
        - În etapa de separare logică a fișierelor, m-am lovit de o problemă în Python.
            Am încercat să mut clasele User și Post în models.py pentru o organizare mai bună.
            - App.py importa user din models.py.
            - models.py importa db din App.py.
        - Am primit eroarea: **ImportError: cannot import name 'db' from 'App'**.
        - Când rulam App.py, fișierul primea numele __main__. Astfel, când models.py căuta from App import db, nu găsea fișierul App deoarece acesta rula deja, provocând eroarea.
        - În cuvinte:
            - Când rulăm App.py, acesta devine __main__, iar în models.py apelăm from App import db, dar App acum este __main__, deci nu știe unde să se uite.

        - *SOLUȚIA*
            - Folosim un Package Structure!
            
            - Am creat un folder principal (ex: App_pk) și am adăugat în el fișierul __init__.py (Fișierul __init__.py este un fișier special în Python folosit pentru a marca un director ca pachet Python și pentru a rula cod de inițializare atunci când acel pachet este importat). Acesta îi spune lui Python că folderul este un pachet.
            
            - Am mutat inițializarea obiectelor App și db în fișierul __init__.py.
            
            - Eliminarea Ciclicității: Am modificat importurile în models.py și routes.py pentru a prelua obiectele direct din pachet (from App_pk import app, db), nu dintr-un fișier individual.

            - Importul la final: În __init__.py, am plasat from App_pk import routes la sfârșitul fișierului. Această tehnică asigură că app și db sunt deja inițializate înainte ca rutele să încerce să le acceseze.

            - Punctul de Intrare (Entry Point): Am creat un fișier principal (App.py situat în folderul rădăcină) care are rolul unic de a porni serverul. Acesta doar importă aplicația configurată din pachet: from App_pk import app.