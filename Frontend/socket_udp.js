
var PORT = 33333;
var HOST = '0.0.0.0';
var dgram = require('dgram');
var server = dgram.createSocket('udp4');
var app = require('express')();
const serve   = require('express-static');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var opn= require('opn');



//app.get('/css', function(req, res){
  //  res.sendFile(__dirname + '/css');
//});

app.use(serve(__dirname + '/'));


app.get('/tx.html', function(req, res){
    res.sendFile(__dirname + '/tx.html');
});

app.get('/index.html', function(req, res){
    res.sendFile(__dirname + '/index.html');
});
app.get('/', function(req, res){
    res.sendFile(__dirname + '/rx.html');
});


server.on('error', (err) => {
    console.log(`UDP SERVER ERROR:\n${err.stack}`);
    server.close();
});

server.on('listening', function () {
    var address = server.address();
    console.log('UDP SERVER IS RUNNING ON PORT ' + "" + address.port);
});

server.on('message', function (message, remote) {
    console.log(remote.address + ':' + remote.port +' - ' + message);
    io.on('connection', function(){
           
    });
    io.emit('gnuradio', message);
    console.log('MESSAGE SENT TO WEB PAGE');  
});

server.bind(PORT, HOST);
http.listen(3000, function(){
    console.log('HTTP SERVER IS RUNNING ON PORT 3000');
    opn('http://localhost:3000/rx.html'); 
});






      

    

