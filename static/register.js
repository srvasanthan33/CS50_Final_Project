var FORM = document.querySelector("#register_form");

FORM.addEventListener("submit",function(e){
    
    pass1 = FORM.querySelector("#Password1").value
    pass2 = FORM.querySelector('#Password2').value
    
    if (pass1 != pass2)
    {   
        e.preventDefault();
        alert("Passwords are not matching");
        
    }
});