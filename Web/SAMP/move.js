// Move皮の処理を全て記載している

var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_move;
var PRODUCT_NUMBER = data.product_number;
var WEBSOCKET = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET);

// ウェブサーバを接続する。
var ws = new WebSocket(WEBSOCKET);

// ソケット接続すれば呼び出す関数。
ws.onopen = function(message){
    ws.send(PRODUCT_NUMBER);
    document.getElementById('move_circle').style.backgroundColor = 'rgba(59, 195, 244, 0.5)';
    document.getElementById('move_circle').innerHTML = "Move Server ON";
    var move_server = document.getElementById('move_circle').innerHTML;
    console.log(move_server);
    // document.getElementById('move').innerHTML = "<p>Move Server ON</p>";
    var picture_server = document.getElementById("picture_circle").innerText;
    console.log(picture_server);
    // var move_server = document.getElementById("move").innerText;
    // Serverが接続される→テキストによってBacgroundを変更
    if(move_server == "Move Server ON"){
        document.getElementById('cvs1').style.backgroundColor = 'rgb(216, 242, 49)';
        }
    else if(picture_server == "Picture Server ON" && move_server == "Move Server ON"){
        document.getElementById('cvs1').style.backgroundColor = 'rgba(59, 195, 244)'; 
        }
};
// // ソケットサーバからメッセージが受信すれば呼び出す関数。
// ws.onmessage = function(message){
//     document.getElementById('move_circle').style.backgroundColor = 'rgba(59, 195, 244)';
//     console.log(message);
// };
 
// ソケット接続が切ると呼び出す関数。
ws.onclose = function(message){
    var output = "off";
    var base64_message = window.btoa(unescape(encodeURIComponent(output)));
    ws.send(base64_message);

};

// ソケット通信中でエラーが発生すれば呼び出す関数。
ws.onerror = function(message){
    var output = "off";
    var base64_message = window.btoa(unescape(encodeURIComponent(output)));
    ws.send(base64_message);
};

// 画像クリック時の処理
$(function () {

    var juge = 0;

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

    $('#live').on('click', function () {
        var output = "wake_up_camera";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
        // window.location.reload(false);
        // ws.send(PRODUCT_NUMBER + "_server");

    });

    $('#btn_car').on('click', function () {
        var output = "wake_up_move";
        var base64_message = window.btoa(unescape(encodeURIComponent(output)));
        ws.send(base64_message);
        setTimeout("location.reload()",5000);
    });


    $('#live_on_off').on('click', function () {
        var on = "camera_boot";
        var off = "camera_boot_off";
        if(juge==1)
        {
            var base64_message = window.btoa(unescape(encodeURIComponent(off)));
            ws.send(base64_message);
            juge = 0;
            document.getElementById('live_on_off').style.backgroundColor = 'rgb(242, 52, 49, 0.5)';
        }
        else
        {
            var base64_message = window.btoa(unescape(encodeURIComponent(on)));
            ws.send(base64_message);
            juge = 1;
            document.getElementById('live_on_off').style.backgroundColor = 'rgba(59, 195, 244, 0.5)';
        }

    });

})

// 入力フォームの処理
$('#message_input').on('click', function () {
    const textbox = document.getElementById("input-message");
    const inputValue = textbox.value;
    const output = inputValue;
    var base64_message = window.btoa(unescape(encodeURIComponent(output))); 
    ws.send(base64_message);
    console.log(base64_message); 
  
  });

// セレクトフォームの処理
$('#select_option').on('click', function () {
const str = document.getElementById("select").value;
    // const color1 = document.form1.select;

    // // 値(数値)を取得
    // const num = color1.selectedIndex;
    // const num = document.form1.color1.selectedIndex;

    // // 値(数値)から値(value値)を取得
    // const message = color1.options[num].value;
    // const str = document.form1.color1.options[num].value;
    console.log(str);
    var base64_message = window.btoa(unescape(encodeURIComponent(str)));
    ws.send(base64_message);
});

});
