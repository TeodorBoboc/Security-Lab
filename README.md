# Security Lab - Learning Project

## Descriere
    Acesta este primul meu proiect web.
    
    Scopul proiectului este de a invata fluxul real al unei aplicatii , de la frontend
    pana la backend si securitate
    Proiectul se concentreaza pe structura repetitiva: Create->Break->Fix

    Am folosit pas cu pas:
    -Frontend: HTML,CSS,Jinja2,Bootstrap.
    -Backend: Python,Flask,Flask-wtf.
    -(urmeaza) Database & securitate
 
 ---

## Scopul Proiectului
    -Sa invat Flask si structura unei aplicatii web.
    -Intelegerea metodelor HTTP
    -Implementarea unui sistem de autentificare (login / register).
    -Creearea si manipularea unei baze de date
    -Identificarea vulnerabilitatilor unui site.
    -Securizarea unui site.
    -Invatare Linux
---

## Functionalitati Implementate
    -Pagina Home cu postari (dummy).
    -Pagina About.
    -Sistem de Intregistrare/Login.
    -Afisare username in navbar (dummy). 
    -Mesaje flash.
    -Template layout comun.

---

## In lucru
    -Inregistrare baza de date (Flask-SQLalchemy).
    -Parole hash.
    -Flask-login.
    -Creare postari reale.
    -Testare vulnerabilitati.
    -Securizare site.

---

## BUGS
    1. Problema Importului Circular (Circular Dependency)
        -In etapa de separare logica a fiserelor, m-am lovit de o problema in Python
            Am incercat sa mut clasele User si Post in models.py pentru o organizare mai buna.
            -App.py importa user din models.py
            -models.py importa db din App.py
        -Am primit eroarea:**ImportError: cannot import name 'db' from 'App'**.
        -Cand rulam App.py fisierul primea numele __main__.Astfle, cand models.py cauta from App import db, nu gasea fisierul App deoarece acesta rula deja, provocand eroarea.
        -In cuvinte:
            -Cand rulam App.py acesta devine __main__, iar in models.py apelam from App import db, dar App acum este __main__, deci nu stie unde sa se uite.
        -*SOLUTIA*
            -Folosim un Package Structure!
            -Am creeat un folder principal (ex:App_pk) si am adaugat in el fisierul __init__.py (Fișierul __init__.py este un fișier special în Python folosit pentru a marca un director ca pachet Python și pentru a rula cod de inițializare atunci când acel pachet este importat.) acesta ii spune lui Python ca folderul este un pachet.
            -Am mutat initializarea obiectelor App si db in fisierul __init__.py.
            -