
var image_socket = null;

var audio_socket = null;
var audio_ctx = null;
var scheduled_time = 0;
var delay_sec = 1;

function on_load(){
  // ここではaudioの再生に関する処理は許可されないのでWebSock処理のみ行う

  // 音声通信用WebSocket接続
  // audio_url = "ws://" + "192.168.0.44" + ":9002"
  audio_socket = new WebSocket(audio_url);
  audio_socket.binaryType = 'arraybuffer';
  audio_socket.onmessage = on_audio_message;

}

function on_button_play_audio(){
  // ユーザー操作イベントでAudioの再生操作を行う
  document.getElementById("button").value="on";

  if(audio_ctx == null){
    audio_ctx = new (window.AudioContext||window.webkitAudioContext)
  }
}

function on_audio_message(recv_data){
  audio_f32 = new Float32Array(recv_data.data);
  // console.log(audio_f32);
  if(audio_ctx != null){
    play_audio(audio_f32);
  }
  draw_audio_graph(audio_f32);
}

function play_audio(data){
  var audio_buffer = audio_ctx.createBuffer(1, data.length, 44100);
  var buffer_source = audio_ctx.createBufferSource();
  var current_time = audio_ctx.currentTime;

  audio_buffer.getChannelData(0).set(data);
  buffer_source.buffer = audio_buffer;
  buffer_source.connect(audio_ctx.destination);

  if (current_time < scheduled_time) {
    buffer_source.start(scheduled_time);
    scheduled_time += audio_buffer.duration;
  } else {
    buffer_source.start(current_time);
    scheduled_time = current_time + audio_buffer.duration + delay_sec;
  }
}

function draw_audio_graph(data){
  var canvas_image = document.getElementById('canvas_audio');
  var ctx_2d = canvas_image.getContext('2d');

  // db値計算（自信ない）
  sum_data = data.reduce((a,b)=>Math.abs(a)+Math.abs(b));
  mean_data = sum_data / data.length;
  dB = 20 * Math.log10(mean_data);

  // 前回描画をクリア
  ctx_2d.fillStyle = '#ffffff';
  ctx_2d.fillRect(0,0,500,40);

  var rate = 2;
  var graph_x = Math.abs(dB) * rate;
  ctx_2d.fillStyle = '#000000';
  ctx_2d.fillRect(0,0,graph_x,40);

  // 値表示
  ctx_2d.fillStyle = '#ff0000';
  ctx_2d.font = "10px serif";
  ctx_2d.fillText("db:" + dB , 5 , 10 );
}
