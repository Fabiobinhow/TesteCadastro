const API_URL = "http://127.0.0.1:5000/usuarios";

document.getElementById("formCadastro").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();

  if(!nome || !email) {
    alert('Preencha nome e email.');
    return;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email })
    });

    if (!res.ok) {
      const err = await res.json();
      alert(err.erro || 'Erro ao cadastrar usuário');
    } else {
      document.getElementById("formCadastro").reset();
      carregarUsuarios();
    }
  } catch (e) {
    alert('Erro ao conectar com o servidor. Verifique se o backend está rodando.');
  }
});

async function carregarUsuarios() {
  try {
    const res = await fetch(API_URL);
    const usuarios = await res.json();
    const lista = document.getElementById("listaUsuarios");
    lista.innerHTML = "";
    usuarios.forEach(u => {
      const li = document.createElement("li");
      li.textContent = `${u.nome} - ${u.email}`;
      lista.appendChild(li);
    });
  } catch (e) {
    console.error('Erro ao carregar usuários', e);
  }
}

// carrega ao iniciar
carregarUsuarios();
