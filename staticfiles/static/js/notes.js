const note = document.getElementById("form-note");
const container = document.getElementById("notes-container");
const jwt = localStorage.getItem("jwtToken");
const refreshToken = localStorage.getItem("refreshToken");
//Muestra las notas
//
const showNotes = (data) => {
  if (!data) {
    return (container.innerHTML = `<h2>No hay notas que mostrar</h2>`);
  }
 
  container.innerHTML = `<br>`
 
  for (const note of data) {
    
    console.log(note);
    container.innerHTML += `<div class="note">
          <h3>${note.title}</h3>
          <p>
            ${note.description}
          </p>
        </div>`;
  }
   container.innerHTML += `<h2>Lista de notas</h2>`;
};

//Consulta las notas

const request = () => {
  fetch("http://localhost:8000/api/all", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "jwtToken": jwt,
      "refreshToken": refreshToken,
    },
  }).then(response => response.json())
    .then(res => {
      console.log(res)
      showNotes(res.data)
    }).catch((err)=>{
      showNotes()
    })
    
};

// Envia las tareas
note.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = note["title"].value;
  const description = note["description"].value;

  const data = {
    title,
    description,
  };

  

  fetch("http://localhost:8000/api/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "jwtToken": jwt,
      "refreshToken": refreshToken,
    },
    body: JSON.stringify(data),
  }).then((response) => {
    // HTTP 301 response
    // Si responde positivo,recarga las tareas
    if (response.status == 201) {
      request();
    }
    note.reset()

  });
});

window.addEventListener("load", () => {
  request(); // Al cargar la vista ejecuta request
});
