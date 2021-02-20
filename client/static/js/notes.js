const notestrash = [
  {
    name: "I am name",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent pulvinar purus augue, sed luctus erat pulvinar in. Quisque pellentesque, mi vulputate molestie molestie, lorem erat blandit felis, eget posuere quam est id diam",
  },
];

const note = document.getElementById("form-note");
const container = document.getElementById("notes-container");

//Muestra las notas
//
const showNotes = (data) => {
  if (!data) {
    return (container.innerHTML = `<h2>No hay notas que mostrar</h2>`);
  }

  container.innerHTML = `<h2>Lista de notas</h2>`;
  for (const note of data) {
    console.log(note);
    container.innerHTML += `<div class="note">
          <h3>${note.name}</h3>
          <p>
            ${note.description}
          </p>
        </div>`;
  }
};

//Consulta las notas

const request = () =>{
  fetch("http://localhost:8000/api/all", {
    method: "GET",
    headers: { "Content-Type": "application/json" }, 
  }).then((response) => {

    // Si responde positivo,recarga las tareas
    if(response.status == 200){
      showNotes(response.data)
    }else{
      showNotes()
    }
    console.log(response);

    //Muestra error
  }).catch((err)=>{
    console.log(err);
    showNotes()
  });
}

// Envia las tareas 
note.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = note["name"].value;
  const description = note["description"].value;

  const data = {
    name,
    description,
  };

  console.log(data);

  fetch("http://localhost:8000/api/create", {
    method: "POST",
    mode: "no-cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((response) => {
    // HTTP 301 response
    // Si responde positivo,recarga las tareas
    if(response.status == 201){
      request()
    }
    console.log(response);
    //window.location.href = response.url; //Redirige
  });

});

window.addEventListener("load", () => {
  request(); // Al cargar la vista ejecuta request
});
