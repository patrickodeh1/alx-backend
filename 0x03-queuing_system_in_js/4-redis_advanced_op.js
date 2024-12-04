import { createClient, print } from "redis";

const redisClient = createClient();

redisClient.on('connect', () => {
    console.log('Redis client connected to the server');
});

redisClient.on('error', (error) => {
    console.error(`Redis client not connected to the server: ${error.message}`);
});

function createHash() {
    const key = 'HolbertonSchools';
    const values = {
        Portland: 50,
        Seattle: 80,
        NewYork: 20,
        Bogota: 20,
        Cali: 40,
        Paris: 2,
    };
    
    for (const [field, value] of Object.entries(values)) {
        redisClient.hset(key, field,value, print);
    }
}

function displayHash() {
    redisClient.hgetall('HolbertonSchools', (error, result) => {
        if (error) {
            console.error(`Error retrieving hash: ${error.message}`);
        } else {
            console.log(result);
        }
    });
}

createHash();
displayHash();
