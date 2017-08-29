/* 
 * NodeJS Server.
 *
 * Subscribe to Redis queue, and send out notifications on push. */

const PORT = 9000;

const REDIS_SERVER = 'localhost';
const REDIS_PORT = 9200;

// Supported channels: Notifications & Inbox.
// N.B. -- Redis uses glob style for pattern matching, NOT regex! This doesn't
// give us much control over the inputted string, so we'll do what we can with
// this pattern and leave the rest to SocketIO. The patterns below will match
// any strings that being with 'users' and end with a supported channel. We can
// check that the user pk at least beings with a digit, however glob doesn't
// support matching for arbitrary length digits. Thus, the * wild card will have
// to do here, with the unfortunate side effect that it'll also match characters.
const REDIS_NOTIFICATION_CHANNEL_GLOB = 'users.[0-9]*.notifications';
const REDIS_MESSAGES_CHANNEL_GLOB = 'users.[0-9]*.inbox';

const BASE_AUTH_URL = 'http://api.vendr.xyz/v1/users/'
const BASE_AUTH_END = '/ws_auth/'

var Regex = require('regex');

// Setup socket.io server.
var app	= require('express')()
var server = require('http').Server(app);
var io = require('socket.io')(server);
server.listen(PORT, function(){
	console.log('listening on port ' + PORT);
});

// Setup our Redis client.
var redis_sub = require('redis').createClient(port=REDIS_PORT, host=REDIS_SERVER);
redis_sub.psubscribe(REDIS_NOTIFICATION_CHANNEL_GLOB);
redis_sub.psubscribe(REDIS_MESSAGES_CHANNEL_GLOB);

/* Handle incoming HTTP requests. */
app.get('/', function(req, res) {
	res.send('<script src="/socket.io/socket.io.js"></script><script>var socket = io();</script>');
});

/* Ensure that the channel is valid. We don't want to waste time dealing with
 * connections to a room we don't service. */
function validate_channel_name(channel_name) {

	var notification_regex = '^(?:users.[0-9]+.notifications)$';
	var inbox_regex = '^(?:users.[0-9]+.inbox)$';
	var valid_channel_regex = notification_regex + '|' +  inbox_regex;

	return channel_name.match(valid_channel_regex) != null;
}

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

		// Ensure the channel name is valid.
		if (validate_channel_name(channel) === false) {
			socket.disconnect();
		}

		// Get authentication credentials.
		//var oauth_token = socket.request.headers.cookie['authorization'];
		//var pk = socket.request.headers.cookie['pk'];
		
		//
		socket.join(channel);
		console.log('ws ' + socket.id + ' joined ' + channel);
		socket.emit('greeting', 'welcome ' + socket.id + ' to ' + channel);
		//

		/*
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
		*/
	});

	/* Publish message on Redis push. */
	redis_sub.on('pmessage', function(pattern, channel, message) {

		console.log('mesasage');
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

