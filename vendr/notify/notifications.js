/* 
 * NodeJS Server.
 *
 * Subscribe to Redis queue, and send out notifications on push. */

const PORT = 9000;

const REDIS_SERVER = 'localhost';
const REDIS_PORT = 9200;

// Our live channels cover both notifications, and messages.
const REDIS_NOTIFICATION_CHANNEL = 'users.[0-9]+.notifications';
const REDIS_MESSAGES_CHANNEL = 'users.[0-9]+.inbox';

const BASE_AUTH_URL = 'http://api.vendr.xyz/v1/users/'
const BASE_AUTH_END = '/ws_auth/'

// Setup socket.io server.
var app	= require('express')()
var server = require('http').Server(app);
var io = require('socket.io')(server);
server.listen(PORT, function(){
	console.log('listening on port ' + PORT);
});

// Setup our Redis client.
var redis_sub = require('redis').createClient(port=REDIS_PORT, host=REDIS_SERVER);
redis_sub.psubscribe(REDIS_NOTIFICATION_CHANNEL);
redis_sub.psubscribe(REDIS_MESSAGES_CHANNEL);

/* Handle incoming HTTP requests. */
app.get('/', function(req, res) {
	res.send('<script src="/socket.io/socket.io.js"></script><script>var socket = io();</script>');
});

/* Authorize a request. */
var request = require("request");
function authenticate(token, pk) {
	var options = {
		url: BASE_AUTH_URL + pk + BASE_AUTH_END,
		headers: {'authorization': token}
	}
	
	return new Promise(function(resolve, reject) {
		request(options, function(error, response, body) {
			resolve(response.statusCode);
		});
	});
}

/* Handle incoming websocket connections. */
var clients = [];
io.on('connection', function(socket){
	clients.push(socket.id);

	/* Connect client to appropriate channel. */
	socket.on('join', function(channel) {

		// Get authentication credentials.
		var oauth_token = socket.request.headers['authorization'];
		var pk = socket.request.headers['pk'];

		// Authenticate user. If they have the requisite credentials then
		// they can join their channel. If not, we'll disconnect them.
		response_code = authenticate(oauth_token, pk).then(function(response_code) {
			if (response_code == 200) {
				socket.join(channel);
				console.log('ws ' + socket.id + ' joined ' + channel);
				socket.emit('greeting', 'welcome ' + socket.id + ' to ' + channel);
			}
			else {
				socket.disconnect();
			}
		});
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

