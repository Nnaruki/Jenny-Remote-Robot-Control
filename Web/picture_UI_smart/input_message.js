var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_move;
var WEBSOCKET = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET);
var ws = new WebSocket(WEBSOCKET);

$('#message_input').on('click', function () {
  const textbox = document.getElementById("input-message");
  const inputValue = textbox.value;
  const output = inputValue;
  var base64_message = window.btoa(unescape(encodeURIComponent(output))); 
  ws.send(base64_message);
  console.log(base64_message); 

});
});