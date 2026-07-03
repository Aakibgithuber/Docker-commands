// Minimal, dependency-free HTTP server for the Java Docker example.
// Uses the JDK's built-in com.sun.net.httpserver so no build tool or external
// dependency is needed — it compiles with `javac` and runs on a JRE.
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);

        server.createContext("/health", exchange -> respond(exchange, "{\"status\":\"ok\"}", "application/json"));
        server.createContext("/", exchange ->
                respond(exchange, "Hello from a production-grade Java container!\n", "text/plain"));

        server.setExecutor(null);
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutting down.");
            server.stop(0);
        }));

        System.out.println("Java server listening on port " + port);
        server.start();
    }

    private static void respond(com.sun.net.httpserver.HttpExchange exchange, String body, String contentType)
            throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", contentType);
        exchange.sendResponseHeaders(200, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
