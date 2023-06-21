(() => {

const listarActividades = async () => {
    try {
        const response = await fetch("/serializar");
        const data = await response.json();
        // console.log(data);
        armarCards(data);
    } catch (error) {
        console.log(error)      
    }
};

const cargaInicial = async () => {
    await listarActividades()
}

const armarCard = (activity, order) => {

    // console.log("armarCard");
    // console.log(activity);

    var div_featurette = document.createElement('div');
    div_featurette.classList.toggle("row");
    div_featurette.classList.toggle("featurette");
    console.log("order", order)
    // La imagen se alinea a izquierda o derecha alternativamente
    if (order==1) {
        html = `<div class="col-md-7">
                    <h2 class="featurette-heading">${activity["titulo"]}. <span class="text-muted">${activity["subtitulo"]}.</span></h2>
                    <p class="lead">${activity["descripcion"]}</p>
                    <p><a class="btn btn-lg btn-outline-primary" href="/contacto/">Conocer más</a></p>
                </div>
                <div class="col-md-5">
                    <img src="../media/${activity["imagen_de_portada"]}" class="bd-placeholder-img bd-placeholder-img-lg img-fluid float-start mx-auto" width="500" height="500"  alt=imagen de ${activity["titulo"]}>
                </div>
                `;
    } else {
        html = `<div class="col-md-7 order-md-2">
                <h2 class="featurette-heading">${activity["titulo"]}. <span class="text-muted">${activity["subtitulo"]}.</span></h2>
                <p class="lead">${activity["descripcion"]}</p>
                <p><a class="btn btn-lg btn-outline-primary" href="/contacto/">Conocer más</a></p>
            </div>
            <div class="col-md-5 order-md-1">
                <img src="../media/${activity["imagen_de_portada"]}" class="bd-placeholder-img bd-placeholder-img-lg img-fluid float-start mx-auto" width="500" height="500"  alt=imagen de ${activity["titulo"]}>
            </div>
        `;
    }


    div_featurette.innerHTML = html;
    return div_featurette;
};

const armarCards = (data) => {
    //recuperar el padre de las cards (<section class="multiple-product-container">)
    const contenedor = document.querySelector(".container", ".marketing");
    // Extraer la lista de actividades del json
    // Recorrer el array data y por cada elemento mandar a crear una card
    data_array = data["lista"];
    // console.log(data_array);
    var separador
    order=1
    data_array.forEach(element => {
        single_activity = element["fields"]
        // console.log(single_activity)
        separador = document.createElement('hr');
        separador.classList.toggle("featurette-divider");
        contenedor.appendChild(separador);
        card = armarCard(single_activity, order);
        contenedor.appendChild(card);
        (order == 1)?(order=2):(order=1)
        // agregar la card al DOM
    });
}

// alert("hoja Actividades")
window.addEventListener("load", async () => {
    listarActividades()
});

})();