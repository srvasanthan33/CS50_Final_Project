let docc = document.querySelector("#page");

docc.addEventListener("submit", function(e){
    
    pages = docc.querySelector("#pages_read").value;
    alert(pages);
    alert("If you have entered wrong book contact admin")

    if (pages > 100)
    {
        
        alert("Someone said there's no such thing as an honest man. He was probably a con man.");

    }
    if (pages < 10)
    {
        alert(" Progressing at a snail's pace is still progress, and slow progress is better than no progress. Never be stagnant, and never give up.");
    }
});