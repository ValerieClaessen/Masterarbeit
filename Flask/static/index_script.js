/**
 * Created by valerie on 20.03.19.
 */

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
socket.emit( 'my event', {
  data: 'User Connected'
} )
var form = $( 'form' ).on( 'submit', function( e ) {
  e.preventDefault()
  let user_name = $( 'input.username' ).val()
  let user_input = $( 'input.message' ).val()
    //let radio_color = $('input[name=optradio]:checked').val()
  socket.emit( 'my event', {
    user_name : user_name,
    message : user_input,
      //color : radio_color
  } )
  $( 'input.message' ).val( '' ).focus()
} )
} )
socket.on( 'my response', function( msg ) {
console.log( msg )
if( typeof msg.user_name !== 'undefined' ) {
  /*$( 'h3' ).remove()'/
  /*$( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )*/
  /*var currentVal = $('#chatbox').append('<b>' + msg.user_name + '</b> ' + msg.message);*/
    $('div.message_holder').append('<div class="card"><div class="card-body"><h6 class="card-subtitle mb-2 text-muted text-left">' + msg.user_name + '</h6><p class="card-text float-${side}">' + msg.message + '</p></div></div>');
    updateScroll();
}
})

function myFunction() {
    document.getElementById("demo").style.color = "red";
}

function oeffnefenster (url) {
   fenster = window.open(url, "fenster1", "width=600,height=400,status=yes,scrollbars=yes,resizable=yes");
   fenster.focus();
}

function updateScroll(){
    var element = document.getElementById("message_holder");
    element.scrollTop = element.scrollHeight;
}

function getUserColor() {
    let radio_color = $('input[name=optradio]:checked').val()
    return radio_color

}

function setUserColor() {
    document.getElementById("gly").style.color = getUserColor();

}

