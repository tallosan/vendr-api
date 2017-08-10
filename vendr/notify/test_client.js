/* Test script for debugging notification socket.
 *
 * Here, we connect a client to their notifications channel at:
 *	
 *	notifications.<user_pk>.<user_email>
 *
 * Note, we can also connect them to their inbox channel, although this
 * isn't really covered in this example, by directing them to:
 *
 *	users.<user_pk>.inbox
 *
 * */

var io = require('socket.io-client');
var notifications_channel = 'notifications.' + USER_PK + '.' + USER_EMAIL;
// var inbox_channel = 'users.' + USER_PK + '.inbox';

var token = OAUTH_TOKEN;
var pk = USER_PK;

// Note, we are explicitly setting the transport as websocket.
var ws_config = {
	transports: ['websocket'],
	upgrade: false,
	extraHeaders: {
		'Authorization': 'Bearer ' + token,
		'pk': pk
	}

};

var socket = io.connect('http://notify.vendr.xyz', ws_config);
socket.on('connect', function(sock_data){
	socket.emit('join', notifications_channel);
	console.log('connected to ' + notifications_channel);
});

socket.on(notifications_channel, function(djson) {
	console.log('\n');
	console.log(djson);
});

socket.on('greeting', function(msg) {
	console.log(msg);
});

