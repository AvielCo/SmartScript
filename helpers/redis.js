const redis = require('redis');
const redisClient = redis.createClient({ port: 6379, address: 'localhost' });

redisClient.on('connect', () => {
  console.log('[REDIS] Connected');
});

redisClient.on('ready', () => {
  console.log('[REDIS] Ready');
});

redisClient.on('error', (err) => {
  console.log('[REDIS] ', err);
});

redisClient.on('end', () => {
  console.log('[REDIS] Disconnected');
});

process.on('SIGINT', () => {
  redisClient.quit();
});

module.exports = redisClient;
