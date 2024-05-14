package main

import (
    "net/http"
    "sync"
)

func makeRequest(wg *sync.WaitGroup) {
    defer wg.Done()
    for {
        // attacks for both the unprotected and protected servers
        // http.Get("http://192.168.29.238:8000/")
        http.Get("http://192.168.29.238:8001/")
    }
}

func main() {
    numThreads := 1000 // Change this value to the desired number of threads

    var wg sync.WaitGroup
    wg.Add(numThreads)

    for i := 0; i < numThreads; i++ {
        go makeRequest(&wg)
    }

    wg.Wait()
}