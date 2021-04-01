const redis = require('redis');

const client = redis.createClient({
  port: 6379,
  host: '127.0.0.1',
});

client.on('connect', () => {
  console.log('[REDIS] Connected to redis');
});

client.on('ready', () => {
  console.log('[REDIS] Ready to use');
});

client.on('error', (err) => {
  console.log('[REDIS]', err.message);
});

client.on('end', () => {
  console.log('[REDIS] Disconnected from redis.');
});

process.on('SIGINT', () => {
  client.quit();
});

module.exports = client;
