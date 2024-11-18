const apiBaseUrl = "http://127.0.0.1:8000/api"

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatos();

    const formCreate = document.getElementById("form-create");
    formCreate.addEventListener("submit", async (e) => {
        e.preventDefault();
        const nombre = document.getElementById("nombre").value;
        const descripcion = document.getElementById("descripcion").value;
        const valor = parseFloat(document.getElementById("valor").value);

        const response = await fetch(`${apiBaseUrl}/datos/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nombre, descripcion, valor }),
        });

        if (response.ok) {
            alert("Producto agregado exitosamente");
            obtenerDatos();
            formCreate.reset();
        } else {
            alert("Error al agregar producto");
        }
    });
});

async function obtenerDatos() {
    const response = await fetch(`${apiBaseUrl}/datos/`);
    const productos = await response.json();
    const listaProductos = document.getElementById("lista-productos");
    listaProductos.innerHTML = "";

    productos.forEach((producto) => {
        const li = document.createElement("li");
        li.textContent = `${producto.nombre} - ${producto.descripcion} - $${producto.valor}`;
        listaProductos.appendChild(li);
    });
}