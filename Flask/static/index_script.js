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
    let cb = $( '#cb_inappropriate' ).val()
    let hs = $( '#hs_inappropriate' ).val()
    let user_evaluation = $('input[name=optradio]:checked').val();
  console.log(cb)
  console.log(hs)
  console.log(user_evaluation)

  socket.emit( 'my event', {
    user_name : user_name,
    message : user_input,
      cyberbullying :cb,
      hatespeech : hs,
      color: user_color,
      evaluation: user_evaluation
  } )
  $( 'input.message' ).val( '' ).focus()
} )
} )

socket.on( 'my response', function( msg ) {
    console.log( msg )

    //Unterscheideung zwischen ausgewählten Buttons fehlt noch
    if( typeof msg.user_name !== 'undefined' ) {
        if( msg.cyberbullying == 1 || msg.hatespeech == 1) {
            if (msg.evaluation == 'i1') {
                $( '#loader' ).remove()
                $('#input_chatmessage').val('');
                $('#message_appropriate').modal('hide');
            }
            else {
                $( '#message_default' ).remove()
                $('#message_appropriate').modal('hide');
                $( '#loader' ).remove()
                $('div.message_holder').append('<div class="card"><div class="card-body"><h6 class=" " style="color: ' + msg.color + '";>&nbsp;&nbsp;' + msg.user_name + '</h6><p class="card-text float-left">&nbsp;&nbsp;&nbsp;&nbsp;' + msg.message + '</p></div></div>');
                $('#input_chatmessage').val('');
                updateScroll();
            }
        }
        else if (msg.evaluation == 'a1') {
            $( '#message_default' ).remove()
            $('#message_appropriate').modal('hide');
            $( '#loader' ).remove()
            $('div.message_holder').append('<div class="card"><div class="card-body"><h6 class=" " style="color: ' + msg.color + '";>&nbsp;&nbsp;' + msg.user_name + '</h6><p class="card-text float-left">&nbsp;&nbsp;&nbsp;&nbsp;' + msg.message + '</p></div></div>');
            $('#input_chatmessage').val('');
            updateScroll();
        }
        else {
            $( '#message_default' ).remove()
            $('#message_appropriate').modal('hide');
            $( '#loader' ).remove()
            $('div.message_holder').append('<div class="card"><div class="card-body"><h6 class="text-muted">&nbsp;&nbsp;' + msg.user_name + '</h6><p class="card-text float-left text-muted">&nbsp;&nbsp;&nbsp;&nbsp;' + msg.message + '</p></div></div>');
            $('#input_chatmessage').val('');
            updateScroll();
        }
    }
})

function oeffnefenster (url) {
   fenster = window.open(url, "fenster1", "width=600,height=400,status=yes,scrollbars=yes,resizable=yes");
   fenster.focus();
}

$(function () {
    $('#ml_button').bind('click', function() {
        $('#msg_inappropriate').remove()
        $('#msg_appropriate').remove()
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
                    console.log(cb);
                    console.log(hs);

                    if( cb == 1 || hs == 1) {
                        if (cb == 1) {
                            $('#cb_inappropriate').val('1');
                            $('#cb_appropriate').val('1');
                        }
                        else {
                            $('#cb_inappropriate').val('0');
                            $('#cb_appropriate').val('0');
                        }

                        if (hs == 1) {
                            $('#hs_inappropriate').val('1');
                            $('#hs_appropriate').val('1');
                        }
                        else {
                            $('#hs_inappropriate').val('0');
                            $('#hs_appropriate').val('0');
                        }
                        $('div.inappropriate-header').append('<div id="msg_inappropriate"><p><b>Your message: </b>' + message + '</p></div>')
                        $('#message_inappropriate').modal('show')
                    }
                    else {
                        $('#cb_appropriate').val('0');
                        $('#cb_inappropriate').val('0');
                        $('#hs_appropriate').val('0');
                        $('#hs_inappropriate').val('0');

                        $('div.appropriate-header').append('<div id="msg_appropriate"><p><b>Your message: </b>' + message + '</p></div>')
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

var message_evaluate = "";
function save_for_evaluation() {
    to_eval = document.getElementById("input_chatmessage");
    message_evaluate = to_eval
    console.log(to_eval)
}





