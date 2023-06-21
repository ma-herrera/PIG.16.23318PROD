
(() => {
    'use strict'
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
  
        form.classList.add('was-validated')
        setTimeout(function() {
          var successMessage = document.getElementById('success-message');
          if (successMessage) {
            successMessage.remove();
          }
        }, 2000);
     
      }, false)
    })
 
  })();


  /*------------- Verificar fortaleza de contraseña -------------*/

  function verificarFortaleza(){
        
    var contraseña = document.getElementById("password1").value;
    var longitud = contraseña.length;
    var mensaje = "";
    
    if (longitud === 0) {
    mensaje = "";
    document.getElementById("mensajePass").style.backgroundColor = "white";
    } else if (longitud < 5) {
    mensaje = "La contraseña es muy débil. Debe tener al menos 8 caracteres.";
    document.getElementById("mensajePass").style.backgroundColor = "red";
    document.getElementById("mensajePass").style.color = "white";
    
    } else if (longitud >= 5 && longitud < 10) {
    mensaje = "La contraseña es moderada. Debe tener al menos 10 caracteres para ser más segura.";
    document.getElementById("mensajePass").style.backgroundColor = "orange";
    document.getElementById("mensajePass").style.color = "black";
    } else {
    mensaje = "La contraseña es fuerte. ¡Bien hecho!";
    document.getElementById("mensajePass").style.backgroundColor = "greenyellow";
    document.getElementById("mensajePass").style.color = "black";
    }

    document.getElementById("mensajePass").innerHTML = mensaje;
  
}