import { createClient } from 'redis';
import { promisify } from 'util';

const redsiClient = createClient();

redisClient.on('connect', () => {
    console.log('Redis client connected to the server');
})

redsiClient.on('error', (error) {
    console.error(`Redis client not connected to the server: ${error.message}`);
});

const getAsync = promisify(redsiClient.get).bind(redsiClient);

function setNewSchool(schoolName, value) {
    redisClient.set(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
    try{
        const result = await getAsync(schoolName);
        console.log(`${schoolName}`: ${result});
    } catch (error) {
        console.error(`Error retrieving value for ${schoolName}: ${error.message}`);
    }
}

(async () => {
    await displaySchoolValue('Holberton');
    setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');

})();
