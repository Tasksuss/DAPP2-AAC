package com.example.glassgaze

import kotlinx.coroutines.*
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.ServerSocket
import java.net.Socket

class RegionReceiver(private val callback: ((String) -> Unit)? = null) {
    private val HOST = "0.0.0.0"
    private val PORT = 5051
    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun start() {
        if (isRunning) return

        scope.launch {
            try {
                serverSocket = ServerSocket(PORT)
                isRunning = true
                println("[SERVER] Listening on $HOST:$PORT")

                while (isRunning && !serverSocket!!.isClosed) {
                    val clientSocket = serverSocket!!.accept()
                    println("[SERVER] Connection from ${clientSocket.inetAddress.hostAddress}")
                    launch {
                        handleClient(clientSocket)
                    }
                }
            } catch (e: Exception) {
                println("[SERVER ERROR] ${e.message}")
            }
        }
    }

    private suspend fun handleClient(socket: Socket) {
        try {
            socket.use { clientSocket ->
                val reader = BufferedReader(InputStreamReader(clientSocket.getInputStream()))
                var buffer = ""

                while (isRunning && !clientSocket.isClosed) {
                    val line = reader.readLine() ?: break
                    buffer += line + "\n" // preserve newline for parsing

                    while (buffer.contains('\n')) {
                        val lineEnd = buffer.indexOf('\n')
                        val message = buffer.substring(0, lineEnd).trim()
                        buffer = buffer.substring(lineEnd + 1)

                        if (message.isNotEmpty()) {
                            println("[SERVER] Received: $message")

                            // You can respond here if needed using clientSocket.getOutputStream().write(...)
                            withContext(Dispatchers.Main) {
                                callback?.invoke(message)
                            }
                        }
                    }
                }
                println("[SERVER] Client disconnected")
            }
        } catch (e: Exception) {
            println("[SERVER ERROR] Client handler: ${e.message}")
        }
    }

    fun stop() {
        isRunning = false
        try {
            serverSocket?.close()
        } catch (e: Exception) {
            println("[SERVER ERROR] Closing socket: ${e.message}")
        }
        scope.cancel()
    }
}
