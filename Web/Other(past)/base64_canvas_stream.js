var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_picture;
var WEBSOCKET_PICTURE = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET_PICTURE);

// ウェブサーバを接続する。
var webSocket = new WebSocket(WEBSOCKET_PICTURE);

// ソケット接続すれば呼び出す関数。
webSocket.onopen = function(message){
    webSocket.send("TEST_server");

};
// ソケット接続が切ると呼び出す関数。
webSocket.onclose = function(message){
    console.log("Server Disconnect...");
};
// ソケット通信中でエラーが発生すれば呼び出す関数。
webSocket.onerror = function(message){
    console.log("error...");
};
// ソケットサーバからメッセージが受信すれば呼び出す関数。
webSocket.onmessage = function(message){
    var str = message.data;
    // console.log(str);
    var headSlice  = str.slice(2);
    var footSlice  = headSlice.slice( 0, -1 );
    //console.log(footSlice)
    var data = "data:image/jpeg;base64," + footSlice; //Base64データ
    //console.log(data);
    //2Dコンテキストのオブジェクトを生成する
    var cvs = document.getElementById('cvs1');
    var ctx= cvs.getContext('2d');
    //画像オブジェクトを生成
    var img = new Image();
    img.src = data;
    
    //画像をcanvasに設定
    img.onload = function(){
        ctx.drawImage(img, 0, 0, 800,600);
    }
};
// サーバにメッセージを送信する関数。
function sendMessage(){
    var message = document.getElementById("textMessage");
    messageTextArea.value += "Send to Server => "+message.value+"\n";
    // WebSocketでtextMessageのオブジェクトの値を送信する。
    webSocket.send(message.value);
    //textMessageオブジェクトの初期化
    message.value = "";
}
// 通信を切断する。
function disconnect(){
    webSocket.close();
}
});
