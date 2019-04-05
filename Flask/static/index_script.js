/**
 * Created by valerie on 20.03.19.
 */
$(window).on('load',function(){
        $('#myModal').modal('show');

    });

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
socket.emit( 'my event', {
  data: 'User Connected'
} )

var form = $( 'form' ).on( 'submit', function( e ) {
  e.preventDefault()
  let user_name = $( 'input.username' ).val()
  let user_input = $( 'input.message' ).val()
    let user_color = $( 'input.color' ).val()
    let user_evaluation = $('input.eval_radio').val()
  socket.emit( 'my event', {
    user_name : user_name,
    message : user_input,
      color: user_color,
      evaluation: user_evaluation   //funktioniert noch nicht weil her noch kein radiobutton gechecked ist!

  } )
  $( 'input.message' ).val( '' ).focus()
} )
} )

socket.on( 'my response', function( msg ) {
    console.log( msg )

    //Unterscheideung zwischen ausgewählten Buttons fehlt noch
    if( typeof msg.user_name !== 'undefined' ) {
        $( '#message_default' ).remove()
        $('#message_appropriate').modal('hide');
        $( '#loader' ).remove()
        $('div.message_holder').append('<div class="card"><div class="card-body"><h6 class=" " style="color: ' + msg.color + '";>&nbsp;&nbsp;' + msg.user_name + '</h6><p class="card-text float-left">&nbsp;&nbsp;&nbsp;&nbsp;' + msg.message + '</p></div></div>');
        $('#input_chatmessage').val('');
        updateScroll();
    }
})

function oeffnefenster (url) {
   fenster = window.open(url, "fenster1", "width=600,height=400,status=yes,scrollbars=yes,resizable=yes");
   fenster.focus();
}

function remove_loader() {
    $( '#loader' ).remove()
    $('#input_chatmessage').val('');
}

$(function () {
    //xxxxx mit message austauschen im Modal!
    $('#ml_button').bind('click', function() {
        $( '#message_default' ).remove()
        $('div.message_holder').append('<div id="loader" class="loader"></div>')
        updateScroll();
        let message = $('#input_chatmessage').val();

        $.post('/machine_learning', {'sentence': message, 'cb': 0, 'hs': 0},
            function(data) {
                sentence = data["sentence"]
                cb = data["cb"]
                hs = data["hs"]

                if( typeof sentence !== 'undefined' ) {
                    console.log(sentence);
                    if( cb == 1 || hs == 1) {
                        $('#message_inappropriate').modal('show')
                    }
                    else {
                        $('#message_appropriate').modal('show')
                    }
                }
            });
        return false;
    });
});

function updateScroll(){
    var element = document.getElementById("message_holder");
    element.scrollTop = element.scrollHeight;
}

function getUserColor() {
    //let color = $('input[name=optradio]:checked').val()
    let color = $('input[name=name_color]').val()
    return color

}

function setUserColor() {
    document.getElementById("gly").style.color = getUserColor();
    addUser()
}

// hides popover after the next click
$('body').on('click', function (e) {
    if ($(e.target).data('toggle') !== 'popover'
        && $(e.target).parents('.popover.in').length === 0) {
        $('[data-toggle="popover"]').popover('hide');
    }
});

if ($('#message_inappropriate').is(':visible')) {
    $(document).ready(function () {
        $(window).keydown(function (event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                return false;
            }
        });
    });
}

$(document).ready(function() {
     $('#pop_over_button').attr('disabled','disabled');
     $('input[type="text"]').keyup(function() {
        if($('#input_chatmessage').val() != '') {
           $('input[type="submit"]').removeAttr('disabled');
        }
     });
 });



function enableButton_inap() {
            document.getElementById("submit_message_inappropriate").disabled = false;
        }

function enableButtonap() {
            document.getElementById("submit_message_appropriate").disabled = false;
        }

// function addUser() {
//     $('div.user_holder').append(msg.user_name)
//
// }



var message_evaluate = "";
function save_for_evaluation() {
    to_eval = document.getElementById("input_chatmessage");
    message_evaluate = to_eval
    console.log(to_eval)
}





