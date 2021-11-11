$(".sidebar-dropdown > a").click(function () {
    $(".sidebar-submenu").slideUp(200);
    if (
        $(this)
            .parent()
            .hasClass("active")
    ) {
        $(".sidebar-dropdown").removeClass("active");
        $(this)
            .parent()
            .removeClass("active");
    } else {
        $(".sidebar-dropdown").removeClass("active");
        $(this)
            .next(".sidebar-submenu")
            .slideDown(200);
        $(this)
            .parent()
            .addClass("active");
    }
});

$("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");
});
$("#show-sidebar").click(function () {
    $(".page-wrapper").addClass("toggled");
});



/**
 * Agregar inputs para crear mas horarios en las funciones - peliculas
 */

document.addEventListener('click', event => {
    let button = event.target;
    if (button.id === 'button-new-show') {
        const list = document.querySelector('#new-date-shows');
        const id = "timedate-" + Math.floor(Math.random() * 999999);
        const li = document.createElement('div');
        li.classList.add('row');
        li.id = id;
        li.innerHTML =
            `<div class="form-group col-8">
                <input class="form-control mt-2" type="datetime-local" name="datetime[]" required>
            </div>
            <div class="form-group col-4">
                <button type="button" data-id="${id}"
                    class="btn btn-danger form-control mt-2">Borrar</button>
            </div>`;
        list.appendChild(li);
    }
    if (button.dataset.id) {
        document.querySelector(`#${button.dataset.id}`).remove();
    }
})
