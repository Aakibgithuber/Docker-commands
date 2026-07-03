// Minimal HTTP server for the Go Docker example. Uses only the
// standard library so it compiles to a single static binary.
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintln(w, `{"status":"ok"}`)
	})
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello from a production-grade Go container!")
	})

	log.Printf("Go server listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
