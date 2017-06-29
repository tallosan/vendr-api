/* Test script for debugging notification socket. */

var io = require('socket.io-client');
var channel = 'notifications.pk.email';

// Note, we are explicitly setting the transport as websocket.
var ws_config = {transports: ['websocket'], upgrade: false};
var socket = io.connect('http://notify.zappme.xyz', ws_config);
socket.on('connect', function(sock_data){
	socket.emit('join', channel);
	console.log('connected to ' + channel);
});

socket.on(channel, function(djson) {
	console.log(djson);
});

socket.on('greeting', function(msg) {
	console.log(msg);
});

