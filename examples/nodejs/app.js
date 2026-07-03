// Minimal zero-dependency HTTP server used to demonstrate a
// production-style Node.js container image.
const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from a production-grade Node.js container!\n');
});

server.listen(PORT, () => {
  console.log(`Node.js server listening on port ${PORT}`);
});
