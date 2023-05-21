// Import amqplib module
const amqp = require('amqplib');

// Set connection string
const url = 'amqps://typubflw:KP3mHkkvfjPP9VPdzJaHf0rm5x3u-GKH@armadillo.rmq.cloudamqp.com/typubflw';

// Define the queue name
const queue = 'task_queue';

// Define the function to produce messages
async function produce() {
  // Create a connection using the connection string
  const connection = await amqp.connect(url);

  // Create a channel for the connection
  const channel = await connection.createChannel();

  // Define the message
  let msg = 'Hello Rangga';

  // Assert the queue, this is idempotent (it only creates if it doesn't exist yet)
  // Set the queue option 'durable' to true for persistent messages
  await channel.assertQueue(queue, {
    durable: true
  });

  // Send a message to the queue
  // The message is sent as a buffer, and the option 'persistent' is set to true to make it persistent
  channel.sendToQueue(queue, Buffer.from(msg), {
    persistent: true
  });

  // Log the sent message
  console.log(" [x] Sent '%s'", msg);

  // Close the channel and connection
  await channel.close();
  await connection.close();
}

// Call the produce function and handle any errors
produce().catch(console.error);