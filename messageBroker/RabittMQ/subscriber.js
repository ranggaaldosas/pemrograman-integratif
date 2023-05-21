// Import amqplib module
const amqp = require('amqplib');

// Set connection string
const url = 'amqps://typubflw:KP3mHkkvfjPP9VPdzJaHf0rm5x3u-GKH@armadillo.rmq.cloudamqp.com/typubflw';

// Define the queue name
const queue = 'task_queue';

// Define the function to consume messages
async function consume() {
  // Create a connection using the connection string
  const connection = await amqp.connect(url);

  // Create a channel for the connection
  const channel = await connection.createChannel();

  // Assert the queue, this is idempotent (it only creates if it doesn't exist yet)
  // Set the queue option 'durable' to true for persistent messages
  await channel.assertQueue(queue, {
    durable: true
  });

  // Log that the consumer is waiting for messages
  console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

  // Consume messages from the queue
  // When a message is received, log the message
  // The option 'noAck' is set to true, meaning that the consumer does not acknowledge the messages
  channel.consume(queue, function(msg) {
    console.log(" [x] Received '%s'", msg.content.toString());
  }, {
    noAck: true
  });
}

// Call the consume function and handle any errors
consume().catch(console.error);