package com.example.glassgaze

import android.content.Context
import android.graphics.*
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.util.AttributeSet
import android.view.View
import kotlinx.coroutines.*
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.ServerSocket
import java.net.Socket
import java.util.*
import kotlin.math.*

class AACKeyboardView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    // Constants
    companion object {
        private val RIGHT = listOf("a", "e", "i", "o", "u")
        private val TOP = listOf("s", "t", "n", "r", "d", "l", "h")
        private val LEFT = listOf("c", "w", "m", "g", "y", "p", "f")
        private val BOTTOM = listOf("j", "b", "q", "k", "v", "z", "x")
        
        private const val SELECTION_THRESHOLD = 4
        private const val MAX_DISPLAY_CHARS = 7
        
        private val STATES = listOf("MAIN", "RIGHT", "TOP", "LEFT", "BOTTOM", "NUM")
    }

    // Colors
    private val colorBackground = Color.parseColor("#f8fafc")
    private val colorBorder = Color.parseColor("#3b82f6")
    private val colorText = Color.parseColor("#1e293b")
    private val colorRing = Color.parseColor("#e2e8f0")
    private val colorConfirm = Color.parseColor("#10b981")
    private val colorCancel = Color.parseColor("#ef4444")
    private val colorSide = Color.parseColor("#f1f5f9")

    // Paints
    private val paintBackground = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintBorder = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintRing = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintText = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintHighlight = Paint(Paint.ANTI_ALIAS_FLAG)

    // State variables
    private var currentState = "MAIN"
    private var currentText = ""
    private var centerX = 0f
    private var centerY = 0f
    private var ringRadius = 200f
    private var innerRadius = 60f

    // Text-to-Speech
    private var tts: TextToSpeech? = null

    // Counters
    private val counters = mutableMapOf<String, Int>().apply {
        put("TOP", 0)
        put("RIGHT", 0)
        put("BOTTOM", 0)
        put("LEFT", 0)
        put("NUM", 0)
        put("RETURN", 0)
        put("DELETE", 0)
        put("CONFIRM", 0)
        put("CENTER", 0)
    }
    
    private val secondaryCounters = mutableMapOf<String, Int>()

    // Character positions
    private val characterPositions = mutableMapOf<Pair<String, String>, Pair<Float, Float>>()
    private val sectorMappings = mutableMapOf<String, Map<String, List<Int>>>()

    // Socket receiver
    private var regionReceiver: RegionReceiver? = null

    init {
        initializePaints()
        initializeCounters()
        initializeMappings()
        initializeTTS()
        startSocketListener()
    }

    private fun initializePaints() {
        paintBackground.color = colorBackground
        paintBorder.apply {
            color = colorBorder
            style = Paint.Style.STROKE
            strokeWidth = 6f
        }
        paintRing.color = colorRing
        paintText.apply {
            color = colorText
            textSize = 48f
            textAlign = Paint.Align.CENTER
        }
        paintHighlight.color = colorBorder
    }

    private fun initializeCounters() {
        // Initialize secondary counters for each character
        val sections = mapOf(
            "RIGHT" to RIGHT,
            "TOP" to TOP,
            "LEFT" to LEFT,
            "BOTTOM" to BOTTOM
        )
        
        sections.forEach { (section, chars) ->
            chars.forEachIndexed { i, _ ->
                secondaryCounters["${section}_$i"] = 0
            }
        }
        
        // Initialize number counters
        (0..9).forEach { num ->
            secondaryCounters["NUM_$num"] = 0
        }
    }

    private fun initializeMappings() {
        // MAIN Interface mapping
        sectorMappings["MAIN"] = mapOf(
            "TOP" to listOf(3, 4, 5, 6, 7),
            "LEFT" to listOf(8, 9, 10, 11, 12, 13),
            "BOTTOM" to listOf(14, 15, 16, 17, 18),
            "RIGHT" to listOf(19, 20, 1, 2)
        )
        
        // NUM Interface mapping
        sectorMappings["NUM"] = mapOf(
            "1" to listOf(1),
            "2" to listOf(2, 3, 4),
            "3" to listOf(5, 6),
            "4" to listOf(7, 8),
            "5" to listOf(9, 10),
            "6" to listOf(11, 12),
            "7" to listOf(13, 14),
            "8" to listOf(15, 16),
            "9" to listOf(17, 18, 19),
            "0" to listOf(20)
        )
    }

    private fun initializeTTS() {
        tts = TextToSpeech(context) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale.US
            }
        }
    }

    private fun startSocketListener() {
        regionReceiver = RegionReceiver { command ->
            Handler(Looper.getMainLooper()).post {
                processCommand(command)
            }
        }
        regionReceiver?.start()
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        centerX = w / 2f
        centerY = h / 2f
        ringRadius = minOf(w, h) * 0.4f
        innerRadius = minOf(w, h) * 0.12f
        computeCharacterPositions()
    }

    private fun computeCharacterPositions() {
        // Compute positions for MAIN view - radial arrangement
        val sectorInfo = mapOf(
            "TOP" to Triple(90f, ringRadius * 0.5f, TOP),
            "RIGHT" to Triple(0f, ringRadius * 0.5f, RIGHT),
            "BOTTOM" to Triple(270f, ringRadius * 0.5f, BOTTOM),
            "LEFT" to Triple(180f, ringRadius * 0.5f, LEFT)
        )

        sectorInfo.forEach { (section, info) ->
            val (centerAngle, centerRadius, letters) = info
            letters.forEachIndexed { i, char ->
                val angleRad = Math.toRadians(centerAngle.toDouble())
                val x = centerX + centerRadius * cos(angleRad).toFloat()
                val y = centerY - centerRadius * sin(angleRad).toFloat()
                characterPositions[Pair(char, "MAIN")] = Pair(x, y)
            }
        }

        // Compute positions for secondary views - full circle
        val sections = mapOf("RIGHT" to RIGHT, "TOP" to TOP, "LEFT" to LEFT, "BOTTOM" to BOTTOM)
        sections.forEach { (section, chars) ->
            chars.forEachIndexed { i, char ->
                val startAngle = 360f * i / chars.size
                val endAngle = 360f * (i + 1) / chars.size
                val textAngle = Math.toRadians(((startAngle + endAngle) / 2).toDouble())
                
                val x = centerX + (ringRadius * 0.9f) * cos(textAngle).toFloat()
                val y = centerY - (ringRadius * 0.9f) * sin(textAngle).toFloat()
                characterPositions[Pair(char, section)] = Pair(x, y)
            }
        }

        // Compute positions for numbers
        (0..9).forEach { i ->
            val startAngle = 360f * i / 10
            val endAngle = 360f * (i + 1) / 10
            val textAngle = Math.toRadians(((startAngle + endAngle) / 2).toDouble())
            
            val x = centerX + (ringRadius * 0.9f) * cos(textAngle).toFloat()
            val y = centerY - (ringRadius * 0.9f) * sin(textAngle).toFloat()
            characterPositions[Pair(i.toString(), "NUM")] = Pair(x, y)
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        // Clear background
        canvas.drawColor(colorBackground)
        
        // Draw based on current state
        when (currentState) {
            "MAIN" -> drawMainView(canvas)
            "NUM" -> drawNumView(canvas)
            in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") -> drawSecondaryView(canvas)
        }
        
        // Draw corner buttons
        drawCornerButtons(canvas)
        
        // Draw center circle
        drawCenterCircle(canvas)
    }

    private fun drawMainView(canvas: Canvas) {
        // Draw outer ring
        canvas.drawCircle(centerX, centerY, ringRadius, paintBorder)
        
        // Draw four main sections
        val sections = listOf("TOP", "RIGHT", "BOTTOM", "LEFT")
        val startAngles = listOf(45f, 315f, 225f, 135f)
        
        sections.forEachIndexed { index, section ->
            val rect = RectF(
                centerX - ringRadius, centerY - ringRadius,
                centerX + ringRadius, centerY + ringRadius
            )
            
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(counters[section] ?: 0)
            }
            
            canvas.drawArc(rect, startAngles[index], 90f, true, paint)
            canvas.drawArc(rect, startAngles[index], 90f, false, paintBorder)
        }
        
        // Draw character labels
        val letterSections = mapOf("TOP" to TOP, "RIGHT" to RIGHT, "BOTTOM" to BOTTOM, "LEFT" to LEFT)
        letterSections.forEach { (section, letters) ->
            letters.forEach { char ->
                characterPositions[Pair(char, "MAIN")]?.let { (x, y) ->
                    canvas.drawText(char, x, y + paintText.textSize / 3, paintText)
                }
            }
        }
    }

    private fun drawSecondaryView(canvas: Canvas) {
        // Draw outer ring
        canvas.drawCircle(centerX, centerY, ringRadius, paintBorder)
        
        val letters = when (currentState) {
            "RIGHT" -> RIGHT
            "TOP" -> TOP
            "LEFT" -> LEFT
            "BOTTOM" -> BOTTOM
            else -> emptyList()
        }
        
        letters.forEachIndexed { i, char ->
            val startAngle = 360f * i / letters.size
            val sweepAngle = 360f / letters.size
            
            val rect = RectF(
                centerX - ringRadius, centerY - ringRadius,
                centerX + ringRadius, centerY + ringRadius
            )
            
            val counterKey = "${currentState}_$i"
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
            }
            
            canvas.drawArc(rect, startAngle, sweepAngle, true, paint)
            canvas.drawArc(rect, startAngle, sweepAngle, false, paintBorder)
            
            // Draw character
            characterPositions[Pair(char, currentState)]?.let { (x, y) ->
                canvas.drawText(char, x, y + paintText.textSize / 3, paintText)
            }
        }
    }

    private fun drawNumView(canvas: Canvas) {
        // Draw outer ring
        canvas.drawCircle(centerX, centerY, ringRadius, paintBorder)
        
        (0..9).forEach { i ->
            val startAngle = 360f * i / 10
            val sweepAngle = 36f
            
            val rect = RectF(
                centerX - ringRadius, centerY - ringRadius,
                centerX + ringRadius, centerY + ringRadius
            )
            
            val counterKey = "NUM_$i"
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
            }
            
            canvas.drawArc(rect, startAngle, sweepAngle, true, paint)
            canvas.drawArc(rect, startAngle, sweepAngle, false, paintBorder)
            
            // Draw number
            characterPositions[Pair(i.toString(), "NUM")]?.let { (x, y) ->
                canvas.drawText(i.toString(), x, y + paintText.textSize / 3, paintText)
            }
        }
    }

    private fun drawCornerButtons(canvas: Canvas) {
        val buttonSize = 100f
        val margin = 50f
        
        // Define button positions and colors
        val buttons = listOf(
            Triple("NUM", margin + buttonSize/2, margin + buttonSize/2),
            Triple("⟲", width - margin - buttonSize/2, margin + buttonSize/2),
            Triple("X", margin + buttonSize/2, height - margin - buttonSize/2),
            Triple("✔", width - margin - buttonSize/2, height - margin - buttonSize/2)
        )
        
        buttons.forEach { (text, x, y) ->
            val buttonKey = when (text) {
                "NUM" -> "NUM"
                "⟲" -> "RETURN"
                "X" -> "DELETE"
                "✔" -> "CONFIRM"
                else -> ""
            }
            
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(counters[buttonKey] ?: 0)
            }
            
            canvas.drawRect(
                x - buttonSize/2, y - buttonSize/2,
                x + buttonSize/2, y + buttonSize/2,
                paint
            )
            
            canvas.drawRect(
                x - buttonSize/2, y - buttonSize/2,
                x + buttonSize/2, y + buttonSize/2,
                paintBorder
            )
            
            val textColor = when (text) {
                "✔" -> colorConfirm
                "X" -> colorCancel
                else -> colorText
            }
            
            val textPaint = Paint(paintText).apply { color = textColor }
            canvas.drawText(text, x, y + paintText.textSize / 3, textPaint)
        }
    }

    private fun drawCenterCircle(canvas: Canvas) {
        // Draw center circle background
        val centerPaint = Paint(paintRing).apply {
            color = getHighlightColor(counters["CENTER"] ?: 0)
        }
        canvas.drawCircle(centerX, centerY, innerRadius, centerPaint)
        canvas.drawCircle(centerX, centerY, innerRadius, paintBorder)
        
        // Draw text
        val displayText = getCenterCircleText()
        canvas.drawText(displayText, centerX, centerY + paintText.textSize / 3, paintText)
    }

    private fun getHighlightColor(counter: Int): Int {
        return when {
            counter == 0 -> colorRing
            counter >= SELECTION_THRESHOLD -> colorBorder
            else -> {
                val alpha = (counter.toFloat() / SELECTION_THRESHOLD * 255).toInt()
                Color.argb(alpha, 51, 136, 255) // #3388ff with variable alpha
            }
        }
    }

    private fun getCenterCircleText(): String {
        return if (currentState == "NUM") {
            "."
        } else {
            if (currentText.length <= MAX_DISPLAY_CHARS) {
                currentText
            } else {
                currentText.takeLast(MAX_DISPLAY_CHARS)
            }
        }
    }

    private fun processCommand(command: String) {
        try {
            val commandNum = command.toIntOrNull() ?: return
            
            when (commandNum) {
                in 1..20 -> processSectorInput(commandNum)
                in 21..25 -> processButtonInput(commandNum)
            }
            
            invalidate() // Trigger redraw
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun processSectorInput(sector: Int) {
        when (currentState) {
            "MAIN" -> {
                sectorMappings["MAIN"]?.forEach { (section, sectors) ->
                    if (sector in sectors) {
                        counters[section] = (counters[section] ?: 0) + 1
                        if ((counters[section] ?: 0) >= SELECTION_THRESHOLD) {
                            resetAllCounters()
                            currentState = section
                        }
                        return
                    }
                }
            }
            "NUM" -> {
                sectorMappings["NUM"]?.forEach { (number, sectors) ->
                    if (sector in sectors) {
                        val counterKey = "NUM_$number"
                        secondaryCounters[counterKey] = (secondaryCounters[counterKey] ?: 0) + 1
                        if ((secondaryCounters[counterKey] ?: 0) >= SELECTION_THRESHOLD) {
                            addNumber(number)
                        }
                        return
                    }
                }
            }
            in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") -> {
                val letters = when (currentState) {
                    "RIGHT" -> RIGHT
                    "TOP" -> TOP
                    "LEFT" -> LEFT
                    "BOTTOM" -> BOTTOM
                    else -> emptyList()
                }
                
                // Simplified character selection - map sectors 1-N to characters 0-(N-1)
                if (sector <= letters.size) {
                    val char = letters[sector - 1]
                    addCharacter(char)
                }
            }
        }
    }

    private fun processButtonInput(buttonCode: Int) {
        when (buttonCode) {
            21 -> { // NUM
                counters["NUM"] = (counters["NUM"] ?: 0) + 1
                if ((counters["NUM"] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                    currentState = "NUM"
                }
            }
            22 -> { // RETURN
                counters["RETURN"] = (counters["RETURN"] ?: 0) + 1
                if ((counters["RETURN"] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                    currentState = "MAIN"
                }
            }
            23 -> { // DELETE
                if (currentState !in listOf("TOP", "RIGHT", "BOTTOM", "LEFT")) {
                    counters["DELETE"] = (counters["DELETE"] ?: 0) + 1
                    if ((counters["DELETE"] ?: 0) >= SELECTION_THRESHOLD) {
                        resetAllCounters()
                        if (currentText.isNotEmpty()) {
                            currentText = currentText.dropLast(1)
                        } else {
                            speakText("No")
                        }
                    }
                }
            }
            24 -> { // CONFIRM
                if (currentState !in listOf("TOP", "RIGHT", "BOTTOM", "LEFT")) {
                    counters["CONFIRM"] = (counters["CONFIRM"] ?: 0) + 1
                    if ((counters["CONFIRM"] ?: 0) >= SELECTION_THRESHOLD) {
                        resetAllCounters()
                        if (currentText.isNotEmpty()) {
                            confirmText()
                        } else {
                            speakText("Yes")
                        }
                    }
                }
            }
            25 -> { // CENTER
                counters["CENTER"] = (counters["CENTER"] ?: 0) + 1
                if ((counters["CENTER"] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                    if (currentState == "NUM") {
                        addDecimalPoint()
                    } else {
                        addSpace()
                    }
                }
            }
        }
    }

    private fun addCharacter(char: String) {
        currentText += char
        resetAllCounters()
        currentState = "MAIN"
    }

    private fun addNumber(num: String) {
        currentText += num
        resetAllCounters()
        // Stay in NUM state
    }

    private fun addSpace() {
        currentText += " "
        resetAllCounters()
    }

    private fun addDecimalPoint() {
        currentText += "."
        resetAllCounters()
    }

    private fun confirmText() {
        if (currentText.isNotEmpty()) {
            speakText(currentText)
            currentText = ""
            resetAllCounters()
            currentState = "MAIN"
        }
    }

    private fun speakText(text: String) {
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
    }

    private fun resetAllCounters() {
        counters.keys.forEach { counters[it] = 0 }
        secondaryCounters.keys.forEach { secondaryCounters[it] = 0 }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        tts?.shutdown()
        regionReceiver?.stop()
    }
}

// Region Receiver for socket communication
class RegionReceiver(private val callback: (String) -> Unit) {
    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun start() {
        if (isRunning) return
        
        isRunning = true
        scope.launch {
            try {
                serverSocket = ServerSocket(5051)
                println("Listening on port 5051")
                
                while (isRunning) {
                    try {
                        val clientSocket = serverSocket?.accept()
                        clientSocket?.let { socket ->
                            launch { handleClient(socket) }
                        }
                    } catch (e: Exception) {
                        if (isRunning) {
                            println("Error accepting connection: ${e.message}")
                        }
                    }
                }
            } catch (e: Exception) {
                println("Error starting server: ${e.message}")
            }
        }
    }

    private suspend fun handleClient(socket: Socket) {
        withContext(Dispatchers.IO) {
            try {
                val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                var line: String?
                
                while (reader.readLine().also { line = it } != null && isRunning) {
                    line?.trim()?.let { command ->
                        if (command.isNotEmpty()) {
                            println("Received command: $command")
                            callback(command)
                        }
                    }
                }
            } catch (e: Exception) {
                println("Error handling client: ${e.message}")
            } finally {
                try {
                    socket.close()
                } catch (e: Exception) {
                    println("Error closing socket: ${e.message}")
                }
            }
        }
    }

    fun stop() {
        isRunning = false
        scope.cancel()
        try {
            serverSocket?.close()
        } catch (e: Exception) {
            println("Error closing server socket: ${e.message}")
        }
    }
}