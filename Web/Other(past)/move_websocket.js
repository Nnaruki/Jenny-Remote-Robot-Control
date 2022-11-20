var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_move;
var WEBSOCKET = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET);

// ウェブサーバを接続する。
var webSocket = new WebSocket(WEBSOCKET);
// ソケット接続すれば呼び出す関数。
webSocket.onopen = function(message){
    console.log("move");
};
// ソケット接続が切ると呼び出す関数。
webSocket.onclose = function(message){
    ws.send("off");
//console.log("Server Disconnect...");
};
// ソケット通信中でエラーが発生すれば呼び出す関数。
webSocket.onerror = function(message){
    ws.send("off");
};

$(function () {
    var ws = new WebSocket(WEBSOCKET);

    $('#btn_front').on('click', function () {
        var output = "front";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
    });

    $('#btn_back').on('click', function () {
        var output = "back";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
    });

    $('#btn_right').on('click', function () {
        var output = "right";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
    });

    $('#btn_left').on('click', function () {
        var output = "left";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
    });
    $('#stop').on('click', function () {
        var output = "off";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);

    });

})
});