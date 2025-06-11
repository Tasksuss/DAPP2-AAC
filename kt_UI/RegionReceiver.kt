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
                println("[INFO] Listening on $HOST:$PORT")
                
                while (isRunning && !serverSocket!!.isClosed) {
                    try {
                        val clientSocket = serverSocket!!.accept()
                        println("[INFO] Connection from ${clientSocket.remoteSocketAddress}")
                        
                        launch {
                            handleClient(clientSocket)
                        }
                    } catch (e: Exception) {
                        if (isRunning) {
                            println("[ERROR] Accept failed: ${e.message}")
                        }
                    }
                }
            } catch (e: Exception) {
                println("[ERROR] Server socket failed: ${e.message}")
            }
        }
    }

    private suspend fun handleClient(socket: Socket) {
        try {
            socket.use { clientSocket ->
                val reader = BufferedReader(InputStreamReader(clientSocket.getInputStream()))
                var buffer = ""
                
                while (isRunning && !clientSocket.isClosed) {
                    try {
                        val data = reader.readLine()
                        if (data == null) {
                            println("[INFO] Client disconnected")
                            break
                        }
                        
                        buffer += data
                        while (buffer.contains('\n')) {
                            val lineEnd = buffer.indexOf('\n')
                            val line = buffer.substring(0, lineEnd).trim()
                            buffer = buffer.substring(lineEnd + 1)
                            
                            if (line.isNotEmpty()) {
                                println("[INFO] Received region: $line")
                                withContext(Dispatchers.Main) {
                                    callback?.invoke(line)
                                }
                            }
                        }
                    } catch (e: Exception) {
                        println("[ERROR] Error while receiving: ${e.message}")
                        break
                    }
                }
            }
        } catch (e: Exception) {
            println("[ERROR] Client handling failed: ${e.message}")
        }
    }

    fun stop() {
        isRunning = false
        try {
            serverSocket?.close()
        } catch (e: Exception) {
            println("[ERROR] Error closing server socket: ${e.message}")
        }
        scope.cancel()
    }
}
