var menu = document.querySelector("#icon")
var nav= document.querySelector("nav")

// for get the menu on mobile screen

function Navmenu(){
    
    menu.addEventListener("click",function(){
    nav.style.display = "block";
})
}