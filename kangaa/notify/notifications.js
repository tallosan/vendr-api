/* 
 * NodeJS Server.
 *
 * Subscribe to Redis queue, and send out notifications on push. */

const PORT = 9000;

const REDIS_SERVER = 'localhost';
const REDIS_PORT = 9200;
const REDIS_NOTIFICATION_CHANNEL = 'notifications.*'

const BASE_AUTH_URL = 'http://api.zappme.xyz/v1/users/'
const BASE_AUTH_END = 'notifications/ws_auth/'

// Setup socket.io server.
var app	= require('express')()
var server = require('http').Server(app);
var io = require('socket.io')(server);
server.listen(PORT, function(){
	console.log('listening on port ' + PORT);
});

// Setup our Redis client.
var redis_sub = require('redis').createClient(port=REDIS_PORT, host=REDIS_SERVER);
redis_sub.psubscribe('notifications.*');


/* Handle incoming HTTP requests. */
app.get('/', function(req, res) {
	res.send('<script src="/socket.io/socket.io.js"></script><script>var socket = io();</script>');
});
/*
function auth(token, pk) {
	
	var request = require('request');
	var url = BASE_AUTH_URL + pk + BASE_AUTH_END;
	request(url, function(error, response, body) {
	
	});
}
*/
/* Handle incoming websocket connections. */
var clients = [];
io.on('connection', function(socket){
	clients.push(socket.id);

	/* Connect client to appropriate channel. */
	socket.on('join', function(channel) {

		// Authenticate request.
		console.log(socket.request.headers['authorization']);
		console.log(socket.request.headers['pk']);
		pk = socket.request.headers['pk'];
		
		console.log(channel);
		console.log(BASE_AUTH_URL + pk + BASE_AUTH_END);

		socket.join(channel);
		console.log('ws ' + socket.id + ' joined ' + channel);
		socket.emit('greeting', 'welcome ' + socket.id + ' to ' + channel);
	});

	/* Publish message on Redis push. */
	redis_sub.on('pmessage', function(pattern, channel, message) {

		// Strip whitespace. Channels must match exactly on both sides!
		channel = channel.replace(/ /g, '');
		console.log('pattern: ' + pattern + '\nchannel: ' + channel + '\nmessage: ' + message);
		socket.emit(channel, message);
	});

	/* Handle disconnects. */
	socket.on('disconnect', function() {
		var index = clients.indexOf(socket.id);
		if (index != -1) {
			clients.splice(index, 1);
			console.log('disconnect: ' + socket.id);
		}
	});
});

