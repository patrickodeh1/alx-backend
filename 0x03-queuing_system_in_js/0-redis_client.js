import { createClient } from 'redis';

const redsiClient = createClient();

redisClient.on('connect', () => {
    console.log('Redis client connected to the server');
})

redsiClient.on('error', (error) {
    console.error(`Redis client not connected to the server: ${error.message}`);
});

redsiClient.connect();