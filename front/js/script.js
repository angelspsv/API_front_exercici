document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    //url del endpoint que fa el GET de mostrar alumnes amb aules
    
    const url = 'http://localhost:8000/alumne/listall';
    const options = {
        method: 'GET', 
        headers: {
          'Content-Type': 'application/json'
        },
    };

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            // Netejar la taula abans d'afegir res
            alumnesTableBody.innerHTML = ""; 
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.nom_alumne;
                row.appendChild(nomAluCell);

                const cicleCell = document.createElement("td");
                cicleCell.textContent = alumne.cicle;
                row.appendChild(cicleCell);

                const cursCell = document.createElement("td");
                cursCell.textContent = alumne.curs;
                row.appendChild(cursCell);

                const grupCell = document.createElement("td");
                grupCell.textContent = alumne.grup;
                row.appendChild(grupCell);

                const descAulaCell = document.createElement("td");
                descAulaCell.textContent = alumne.desc_aula;
                row.appendChild(descAulaCell);

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});