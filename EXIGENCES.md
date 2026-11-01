# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---------------------------------|--------------|---------------|------|
| 1 | ... résister aux injections SQL | SAST / DAST | Codage | S1 |
| 2 | ... exiger une authentification | Revue de code | Codage | S2 |
| 3 | ... empêcher un étudiant de modifier une note | Revue de code | Codage | S3 |
| 4 | ... limiter les modifications au module de l'enseignant | Revue de code | Codage | S4 |
| 5 | ... valider que la note est un nombre entre 0 et 20 | Revue de code | Codage | S5 |
| 6 | ... autoriser l'enseignant à modifier la note | Tests | Codage | S6 |
| 7 | ... ne pas divulguer de détails techniques en cas d'erreur | Revue de code | Codage | S7 |