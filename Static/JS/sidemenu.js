const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle");
    
    toggle.addEventListener("click",()=>{
        sidebar.classList.toggle("close");
    });



function toggleConteudo(el) {
    el.classList.toggle("ativo");
}

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');

    searchInput.addEventListener('input', function () {
        const filtro = searchInput.value.toLowerCase();
        const clientes = document.querySelectorAll('.div-clique');

        clientes.forEach(cliente => {
            const texto = cliente.innerText.toLowerCase();

            if (texto.includes(filtro)) {
                cliente.style.display = 'block';
            } else {
                cliente.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');

    searchInput.addEventListener('input', function () {
        const filtro = searchInput.value.toLowerCase();
        const churnClientes = document.querySelectorAll('.churn-informacoes');

        churnClientes.forEach(cliente => {
            const texto = cliente.innerText.toLowerCase();

            if (texto.includes(filtro)) {
                cliente.style.display = 'flex'; // ou 'block', dependendo do layout
            } else {
                cliente.style.display = 'none';
            }
        });
    });
});

