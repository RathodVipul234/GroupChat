function scroll_down(){
    var messageBody = document.querySelector('.messages');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;    
}


$( document ).ready(function() {
    scroll_down()
});


const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);
console.log("chatSocket", chatSocket)

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.command == "send"){
        if (send_by_user == data.sender ){
            var class_name = "replies"
            var user_identity = ""
        }else{
            var class_name = "sent"
            var user_identity = `<span style='float: right; font-weight: 800'>By ${data.sender}</span>`
        }
        $("#message_room").append(`<li class="${class_name} ">`+ 
            '<img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="">'+
            `<p>${data.message}<br>${user_identity}</p></li>`);

        scroll_down()
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

$(document).on("click", "#chat-message-submit", function(e){
    const messageInputDom = $('#chat-message-input');
    const message = messageInputDom.val();
    if(message.trim().length != 0){
        chatSocket.send(JSON.stringify({
            "command":"send",
            "message": message,
            "send_by_user" :send_by_user,
            "group":roomName
        }));
    }
    messageInputDom.val("");
})

