const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

// Redis client setup
const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Kue queue setup
const queue = kue.createQueue();

// Initial values
let reservationEnabled = true;

// Functions to manage seat reservation in Redis
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
}

// Initialize the number of available seats to 50
reserveSeat(50);

// Express server setup
const app = express();
const port = 1245;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errMessage}`);
  });
});

// Route to process the reservation queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    if (currentSeats <= 0) {
      done(new Error('Not enough seats available'));
      return;
    }

    await reserveSeat(currentSeats - 1);

    const updatedSeats = await getCurrentAvailableSeats();
    if (updatedSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
