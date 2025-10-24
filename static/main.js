// https://docs.djangoproject.com/en/3.2/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function getAllTodos(url) {
  
  fetch(url, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    }
  })
  .then(response => response.json())
  .then(data => {
    const todoList = document.getElementById("todoList");
    todoList.innerHTML = "";

    (data.context).forEach(todo => {
      const todoHTMLElement = `
        <li>
          <p>Task: ${todo.task}</p>
          <p>Completed?: ${todo.completed}</p>
        </li>`
        todoList.innerHTML += todoHTMLElement;
    });
  });
}



  const operationGetAllTodos = async (url) => {
      r = await fetch(url, {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        }
      })

      dt = await  r.json();

    const todoList = document.getElementById("todoList");
    todoList.innerHTML = "";

    (dt.context).forEach(todo => {
      const todoHTMLElement = `
        <li>
          <p>Task: ${todo.task}</p>
          <p>Completed?: ${todo.completed}</p>
        </li>`
        todoList.innerHTML += todoHTMLElement;
    });
};

const agregarTodo = async (url, data) => {
  console.log(data);
  const r = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({payload: data}),
  });
  return r.json();  
};



const actualizarTodo = async (url, data) => {
  const r = await fetch(url,{
    method: "PUT",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({payload: data})
  }
  )
}

const eliminarTodo = async (url) => {
  const r = await fetch(url, {
    method: "DELETE",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    }
  });

  return r.json();
};


function addTodo(url, payload) {
  fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({payload: payload})
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  });
}


function updateTodo(url, payload) {
  fetch(url, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({payload: payload})
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  });
}


function deleteTodo(url) {
  fetch(url, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  });
}
