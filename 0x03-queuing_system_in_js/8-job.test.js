const kue = require('kue');
const chai = require('chai');
const expect = chai.expect;
const createPushNotificationsJobs = require('./8-job');

describe('createPushNotificationsJobs', function () {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    kue.Job.rangeByType('push_notification_code_3', 'active', 0, -1, 'asc', (err, selectedJobs) => {
      selectedJobs.forEach(job => job.remove());
    });
    queue.testMode.enter(); // Enter test mode
  });

  afterEach(() => {
    queue.testMode.clear(); // Clear the queue
    queue.testMode.exit();  // Exit test mode
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(42, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs({ key: 'value' }, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs('string', queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    const job1 = queue.testMode.jobs[0];
    const job2 = queue.testMode.jobs[1];

    expect(job1.type).to.equal('push_notification_code_3');
    expect(job1.data).to.deep.equal(jobs[0]);

    expect(job2.type).to.equal('push_notification_code_3');
    expect(job2.data).to.deep.equal(jobs[1]);
  });

  it('should log job creation for each job', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
    ];

    let consoleOutput = [];
    const storeLog = (output) => consoleOutput.push(output);

    const originalConsoleLog = console.log;
    console.log = storeLog;

    createPushNotificationsJobs(jobs, queue);

    console.log = originalConsoleLog; // Restore console.log

    expect(consoleOutput).to.include('Notification job created: 1');
    expect(consoleOutput).to.include('Notification job created: 2');
  });
});
