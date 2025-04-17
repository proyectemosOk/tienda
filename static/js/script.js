document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/tipos")
        .then(res => res.json())
        .then(tipos => {
            const select = document.getElementById("tipo-select");
            tipos.forEach(t => {
                const option = document.createElement("option");
                option.value = t.nombre;
                option.textContent = t.nombre;
                select.appendChild(option);
            });
        });

    fetch("/api/servicios")
        .then(res => res.json())
        .then(servicios => {
            const contenedor = document.getElementById("servicios-checkboxes");
            servicios.forEach(s => {
                const label = document.createElement("label");
                label.innerHTML = `
                    <input type="checkbox" name="servicios" value="${s.nombre}">
                    ${s.nombre}
                `;
                contenedor.appendChild(label);
            });
        });
        console.log("hola")
});
