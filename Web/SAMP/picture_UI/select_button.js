var url = './data.json';
$.getJSON(url, function(data){
var HOST_IP = data.host;
var PORT = data.port_move;
var WEBSOCKET = "ws://" + HOST_IP + ":" + PORT + "/";
console.log(WEBSOCKET + "TALK");
var ws = new WebSocket(WEBSOCKET);

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

  // function clickBtn1(){
  
  //   const str = document.getElementById("select").value;
  //     // const color1 = document.form1.select;

  //     // // 値(数値)を取得
  //     // const num = color1.selectedIndex;
  //     // const num = document.form1.color1.selectedIndex;

  //     // // 値(数値)から値(value値)を取得
  //     // const message = color1.options[num].value;
  //     // const str = document.form1.color1.options[num].value;
  //   console.log(str);
  //   var base64_message = window.btoa(unescape(encodeURIComponent(str)));
  //   ws.send(base64_message);
  // }
}); 