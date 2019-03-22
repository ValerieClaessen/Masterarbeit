/**
 * Created by valerie on 20.03.19.
 */
function myFunction() {
    document.getElementById("demo").style.color = "red";
}

function oeffnefenster (url) {
   fenster = window.open(url, "fenster1", "width=600,height=400,status=yes,scrollbars=yes,resizable=yes");
   fenster.focus();
}