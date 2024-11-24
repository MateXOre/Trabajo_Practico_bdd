const apiBaseUrl = "http://127.0.0.1:8000/api";

// Función para obtener el token CSRF desde las cookies
function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatos();

    // Manejar formulario para crear productos
    const formCreate = document.getElementById("form-create");
    formCreate.addEventListener("submit", async (e) => {
        e.preventDefault();
        const nombre = document.getElementById("nombre").value;
        const descripcion = document.getElementById("descripcion").value;
        const valor = parseFloat(document.getElementById("valor").value);

        const response = await fetch(`${apiBaseUrl}/datos/nuevo/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
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

// Obtener todos los productos
async function obtenerDatos() {
    const response = await fetch(`${apiBaseUrl}/datos/`);
    const productos = await response.json();
    const listaProductos = document.getElementById("lista-productos");
    listaProductos.innerHTML = "";

    productos.forEach((producto) => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${producto.nombre} - ${producto.descripcion} - $${producto.valor} 
            <button onclick="editarProducto(${producto.id}, '${producto.nombre}', '${producto.descripcion}', ${producto.valor})">Editar</button>
            <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
        `;
        listaProductos.appendChild(li);
    });
}

// Función para mostrar el modal de edición
function editarProducto(id, nombre, descripcion, valor) {
    document.getElementById("editar-id").value = id;
    document.getElementById("editar-nombre").value = nombre;
    document.getElementById("editar-descripcion").value = descripcion;
    document.getElementById("editar-valor").value = valor;

    document.getElementById("modal-editar").style.display = "block";
}

// Cerrar el modal de edición
function cerrarModal() {
    document.getElementById("modal-editar").style.display = "none";
}

// Manejar formulario para editar productos
const formEdit = document.getElementById("form-edit");
formEdit.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("editar-id").value;
    const nombre = document.getElementById("editar-nombre").value;
    const descripcion = document.getElementById("editar-descripcion").value;
    const valor = parseFloat(document.getElementById("editar-valor").value);

    const response = await fetch(`${apiBaseUrl}/datos/${id}/editar/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ nombre, descripcion, valor }),
    });

    if (response.ok) {
        alert("Producto actualizado exitosamente");
        cerrarModal();
        obtenerDatos();
    } else {
        alert("Error al actualizar producto");
    }
});

// Eliminar un producto
async function eliminarProducto(id) {
    if (confirm("¿Estás seguro de que quieres eliminar este producto?")) {
        const response = await fetch(`${apiBaseUrl}/datos/${id}/eliminar/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
        });

        if (response.ok) {
            alert("Producto eliminado correctamente");
            obtenerDatos();
        } else {
            alert("Error al eliminar producto");
        }
    }
}
