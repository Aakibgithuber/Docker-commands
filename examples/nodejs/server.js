// Minimal zero-dependency HTTP server used to demonstrate a production Node.js image.
const http = require('http');

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from a containerized Node.js app!\n');
});

server.listen(port, () => {
  console.log(`Node.js server listening on port ${port}`);
});
