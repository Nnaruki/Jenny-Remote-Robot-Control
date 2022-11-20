// Picture 側の処理を全て記載している

var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_picture;
var PRODUCT_NUMBER = data.product_number;
var WEBSOCKET_PICTURE = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET_PICTURE);

// ウェブサーバを接続する。
var webSocket = new WebSocket(WEBSOCKET_PICTURE);

// ソケット接続すれば呼び出す関数。
webSocket.onopen = function(message){
    webSocket.send(PRODUCT_NUMBER);
    document.getElementById('picture_circle').style.backgroundColor = 'rgb(216, 242, 49)';
    document.getElementById('picture_circle').innerHTML = "Picture Server ON";
    console.log(picture_server);

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
    document.getElementById('picture_circle').style.backgroundColor = 'rgba(59, 195, 244, 0.5)';
    var str = message.data;
    // console.log(str);
    // Base64を表示できる形式に加工
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
        ctx.drawImage(img, 0, 0, 800, 600);
    }

    if (message.data != "hey all, a new client has joined us"){
        var picture_server = document.getElementById("picture_circle").innerText;
        var move_server = document.getElementById("move_circle").innerText;
        // Serverが接続される→テキストによってBacgroundを変更
        if(picture_server == "Picture Server ON" && move_server == "Move Server ON"){
            document.getElementById('cvs1').style.backgroundColor = 'rgba(59, 195, 244)'; 
            }
        else if(picture_server == "Picture Server ON"){
            document.getElementById('cvs1').style.backgroundColor = 'rgb(216, 242, 49)';
            }
    }
};

// // 画像クリック時の処理
// $(function () {   

//     $('#btn_car').on('click', function () {
//         var output = "move_reboot";
//         // var base64_message = window.btoa(unescape(encodeURIComponent(output)));
//         webSocket.send(output);
//     });

// })


});


