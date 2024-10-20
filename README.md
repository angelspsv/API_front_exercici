## Fitxer README.md de la segona pràctica d'Angel Ivanov

# M13 - Exercici pràctic FastAPI: L’API d’alumnes

# Apartat 1: Crida de l’API des de la web

_Imatge de la visualizatció de les dades al navegador_
![Imatge de la visualizatció de les dades al navegador](captura_practica2_apartat1.jpg)

.
.

_Imatge de la visualizatció del select-join a la bbdd_
![Imatge de la visualizatció del select-join a la bbdd](captura_bbdd_query_join.jpg)

.
.

_Imatge de l'execució de la query amb el Swagger_
![Imatge de l'execució de la query amb el Swagger](captura_swagger_apar1.jpg)

.
.

# Apartat 2: Consultes avançades

+ _order by_
_Imatge de l'execució en el swagger de la query select amb ORDER BY ASC_

![Imatge de l'execució en el swagger de la query select amb ORDER BY ASC](captura_swagger_query_orderby_asc_apat2.jpg)

.
.

_Imatge de l'execució en el swagger de la query select amb ORDER BY DESC_

![Imatge de l'execució en el swagger de la query select amb ORDER BY DESC](captura_swagger_query_orderby_desc_apat2.jpg)

.
.

+ _contain_
_Imatge de l'execució en el swagger de la query select amb CONTAIN_

![Imatge de l'execució en el swagger de la query select amb contain](captura_swagger_query_contain_apat2.jpg)

.
.

+ _skip & limit_
_Imatge de l'execució en el navegador i a Heidi de la query select amb SKIM & LIMIT_

![Imatge de l'execució en el navegador de la query select amb skip & limit](captura_bbdd_query_skip_limit_apat2.jpg)

.
.

_Imatge de l'execució en el swagger de la query amb SKIM & LIMIT_

![Imatge de l'execució en el swagger de la query select amb skip & limit](captura_bbdd_query_skip_limit_apat2_2.jpg)

.
.


# Apartat 3: Càrrega massiva d’alumnes

_Imatge de l'execució de la primera part del codi: insert de camps a la taula Aula_

![Imatge de l'execució de la primera part del codi: insert aula des de csv](captura_bbdd_insert_aules.jpg)

.
.

_Imatge de la taula aula abans del insert de dades des d'un fitxer csv_

![Imatge de la taula aula abans del insert de dades des d'un fitxer csv](captura_bbdd_insert_aules_abans.jpg)

.
.

_Imatge de l'execució del mètode post en el swagger_

![Imatge de l'execució del mètode post en el swagger](captura_swagger_loadalumnes_exit.jpg)

.
.

_Imatge de l'execució del mètode post i del resultat en la consola_

![Imatge de l'execució en la consola](captura_consola_loadalumnes_exit.jpg)

.
.

_Imatge després d'un nou insert des d'un fitxer csv i el resultat a la taula alumne i el swagger_

![Imatge nou insert taula alumne i swagger](captura_alumne_despres.jpg)

.
.

_Imatge després d'un nou insert des d'un fitxer csv i el resultat a la taula aula i del resultat en la consola. En el primer insert de dos alumnes, Daniel és inserit sense problemes, però en el segon insert tornem ha intentar l'insert de Daniel i una altra alumna(Laura). La segona alumna s'ha inserit correctament i Daniel no per la restricció (UNIQUE) definida a la taula alumne/bbdd_

![Imatge despres nou insert taula aula i consola](captura_aula_despres.jpg)





------------------------Leyenda MarkDown------------------- lista no numerada: +/*/- Elemento 1 encabezado: ### Titulo 1 negrita: /texto en negrita/ cursiva: /texto cursiva/ enlace: Visita Google imagen desde archivo: ![Texto alternativo](URL de la imagen)