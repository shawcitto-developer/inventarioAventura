document.addEventListener('DOMContentLoaded', () => {
    const modalEl = document.getElementById('modalGeneral');
    const contenido = document.getElementById('modalContenido');
    const modal = new bootstrap.Modal(modalEl);
    const csrf = document.querySelector('meta[name="csrf-token"]').content;
    let urlActual = '';

    // 1) Todas las tablas con class="tabla-datos": DataTables en español y adaptable a celulares
    if (window.jQuery && $.fn.DataTable) {
        $('.tabla-datos').DataTable({
            responsive: true,
            language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' },
        });
    }

    // 2) Abrir un modal: cualquier elemento con data-modal-url="..." (crear, editar, eliminar)
    document.addEventListener('click', async (e) => {
        const boton = e.target.closest('[data-modal-url]');
        if (!boton) return;
        e.preventDefault();
        urlActual = boton.dataset.modalUrl;
        const resp = await fetch(urlActual);
        contenido.innerHTML = await resp.text();
        modal.show();
    });

    // 3) Enviar el formulario del modal sin cambiar de página
    document.addEventListener('submit', async (e) => {
        const form = e.target.closest('#modalContenido form');
        if (!form) return;
        e.preventDefault();
        const resp = await fetch(urlActual, { method: 'POST', body: new FormData(form) });
        if (resp.ok) {
            location.reload();                       // guardó bien: recarga la tabla (y muestra el mensaje)
        } else {
            contenido.innerHTML = await resp.text(); // hay errores: el modal sigue abierto con los avisos
        }
    });

    // 4) Acciones de un solo clic: data-post-url="..." (inscribirse, confirmar pago)
    document.addEventListener('click', async (e) => {
        const boton = e.target.closest('[data-post-url]');
        if (!boton) return;
        e.preventDefault();
        boton.disabled = true;
        await fetch(boton.dataset.postUrl, { method: 'POST', headers: { 'X-CSRFToken': csrf } });
        location.reload();
    });

    // 5) Los mensajes se cierran solos a los 4 segundos
    setTimeout(() => {
        document.querySelectorAll('.alerta-flotante').forEach(a => bootstrap.Alert.getOrCreateInstance(a).close());
    }, 4000);

    // 6) Buscador y filtro por categoría del catálogo (sin recargar)
    const buscador = document.getElementById('buscador');
    const filtro = document.getElementById('filtroCategoria');
    if (buscador && filtro) {
        const filtrar = () => {
            const texto = buscador.value.toLowerCase();
            document.querySelectorAll('.item-exp').forEach(el => {
                const coincide = el.dataset.texto.includes(texto) && (!filtro.value || el.dataset.cat === filtro.value);
                el.classList.toggle('d-none', !coincide);
            });
        };
        buscador.addEventListener('input', filtrar);
        filtro.addEventListener('change', filtrar);
    }
});
