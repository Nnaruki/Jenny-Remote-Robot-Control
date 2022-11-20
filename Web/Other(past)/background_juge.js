var url = './data.json';

$.getJSON(url, function(data){
    var HOST_IP = data.host;
    var PORT = data.port_move;
    var PORT_PICTURE = data.port_picture;
    var WEBSOCKET_MOVE = "ws://" + HOST_IP + ":" + PORT + "/";
    console.log(WEBSOCKET_MOVE);

    var WEBSOCKET_PICTURE = "ws://" + HOST_IP + ":" + PORT_PICTURE + "/";
    console.log(WEBSOCKET_PICTURE);

    // ウェブサーバを接続する。
    var webSocket = new WebSocket(WEBSOCKET_PICTURE);
    var webSocket_Move = new WebSocket(WEBSOCKET_MOVE);

    // ソケット接続すれば呼び出す関数。
    webSocket.onopen = function(message){
        document.getElementById('picture').innerHTML = "<p>Picture Server ON</p>";
        console.log(picture_server);
    };

webSocket.onmessage = function(message){
    if (message.data != "hey all, a new client has joined us"){
        var picture_server = document.getElementById("picture").innerText;
        var move_server = document.getElementById("move").innerText;
        // Serverが接続される→テキストによってBacgroundを変更
        if(picture_server == "Picture Server ON" && move_server == "Move Server ON"){
            document.getElementById('cvs1').style.backgroundColor = 'rgba(59, 195, 244)'; 
            }
        else if(picture_server == "Picture Server ON"){
            document.getElementById('cvs1').style.backgroundColor = 'rgb(216, 242, 49)';
            }
    }
};
// ソケット接続が切ると呼び出す関数。
webSocket.onclose = function(message){
    console.log("Server Disconnect...");
};
// ソケット通信中でエラーが発生すれば呼び出す関数。
webSocket.onerror = function(message){
    console.log("error...");
};
// 通信を切断する。
function disconnect(){
    webSocket.close();
}

webSocket_Move.onopen = function(){
    document.getElementById('move').innerHTML = "<p>Move Server ON</p>";
    var picture_server = document.getElementById("picture").innerText;
    var move_server = document.getElementById("move").innerText;
    // Serverが接続される→テキストによってBacgroundを変更
    if(move_server == "Move Server ON"){
        document.getElementById('cvs1').style.backgroundColor = 'rgb(216, 242, 49)';
        }
    // else if(picture_server == "Picture Server ON" && move_server == "Move Server ON"){
    //     document.getElementById('cvs1').style.backgroundColor = 'rgba(59, 195, 244)'; 
    //     }


}

webSocket_Move.onmessage = function(message){
};
// ソケット接続が切ると呼び出す関数。
webSocket_Move.onclose = function(message){
    console.log("Server Disconnect...");
};
// ソケット通信中でエラーが発生すれば呼び出す関数。
webSocket_Move.onerror = function(message){
    console.log("error...");
};
// 通信を切断する。
function disconnect(){
    webSocket.close();
}

});