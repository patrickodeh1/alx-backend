import { createClient } from 'redis';

const redsiClient = createClient();

redisClient.on('connect', () => {
    console.log('Redis client connected to the server');
})

redsiClient.on('error', (error) {
    console.error(`Redis client not connected to the server: ${error.message}`);
});

function setNewSchool(schoolName, value) {
    redisClient.set(schoolName, value, print);
}

function displaySchoolValue(schoolName) {
    redsiClient.get(schoolName, (error, result) => {
        if (error) {
            console.error(`Error retrieving value for ${schoolName}: ${error.message}`);
        } else {
            console.log(`${schoolName}: ${result}`);
        }
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
