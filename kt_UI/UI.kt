package com.example.glassgaze

import android.content.Context
import android.graphics.*
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.util.AttributeSet
import android.view.View
import java.util.*
import kotlin.math.*

class AACKeyboardView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    companion object {
        // set character arrays
        private val RIGHT = listOf("a", "e", "i", "o", "u")
        private val TOP = listOf("s", "t", "n", "r", "d", "l", "h")
        private val LEFT = listOf("c", "w", "m", "g", "y", "p", "f")
        private val BOTTOM = listOf("j", "b", "q", "k", "v", "z", "x")
        private val NUMBERS = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")

        private const val SELECTION_THRESHOLD = 4
        private const val MAX_DISPLAY_CHARS = 6

        private val STATES = listOf("MAIN", "RIGHT", "TOP", "LEFT", "BOTTOM", "NUM")
    }

    // setting Colors
    private val colorBackground = Color.parseColor("#f8fafc")
    private val colorBorder = Color.parseColor("#3b82f6")
    private val colorText = Color.parseColor("#1e293b")
    private val colorRing = Color.parseColor("#e2e8f0")
    private val colorConfirm = Color.parseColor("#10b981")
    private val colorCancel = Color.parseColor("#ef4444")
    private val colorSide = Color.parseColor("#f1f5f9")

    // Paint objects
    private val paintBackground = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintBorder = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintRing = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintText = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintHighlight = Paint(Paint.ANTI_ALIAS_FLAG)

    // Layout variables - matching Python exactly
    private var centerX = 0f
    private var centerY = 0f
    private var canvasWidth = 500f
    private var canvasHeight = 500f
    private var ringSize = 400f
    private var innerRadius = 60f

    // Square boundary for Google Glass rectangular screen
    private var squareSize = 0f
    private var squareLeft = 0f
    private var squareTop = 0f
    private var squareRight = 0f
    private var squareBottom = 0f

    // State variables
    private var currentState = "MAIN"
    private var currentText = ""
    // Add these variables after the existing state variables

    // Light point display variables
    private var lightPointPosition: String? = null
    private var lightPointStartTime: Long = 0
    private val LIGHT_POINT_DURATION = 3000L // 3 seconds in milliseconds
    private val lightPointPaint = Paint(Paint.ANTI_ALIAS_FLAG)

    // Text-to-Speech
    private var tts: TextToSpeech? = null

    // Sector mappings matching Python exactly
    private val sectorMappings = mapOf(
        "MAIN" to mapOf(
            "TOP" to listOf(3, 4, 5, 6, 7),
            "LEFT" to listOf(8, 9, 10, 11, 12, 13),
            "BOTTOM" to listOf(14, 15, 16, 17, 18),
            "RIGHT" to listOf(19, 20, 1, 2)
        ),
        "NUM" to mapOf(
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
        ),
        // Individual character mappings for secondary states
        "a" to mapOf("0" to listOf(1, 2, 3, 4)),
        "e" to mapOf("0" to listOf(5, 6, 7, 8)),
        "i" to mapOf("0" to listOf(9, 10, 11, 12)),
        "o" to mapOf("0" to listOf(13, 14, 15, 16)),
        "u" to mapOf("0" to listOf(17, 18, 19, 20)),
        "s" to mapOf("0" to listOf(1, 2, 3)),
        "t" to mapOf("0" to listOf(4, 5, 6)),
        "n" to mapOf("0" to listOf(7, 8, 9)),
        "r" to mapOf("0" to listOf(10, 11)),
        "d" to mapOf("0" to listOf(12, 13, 14, 15)),
        "l" to mapOf("0" to listOf(16, 17)),
        "h" to mapOf("0" to listOf(18, 19, 20))
    )

    // Counter system matching Python exactly
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

    // Character positions storage
    private val characterPositions = mutableMapOf<Pair<String, String>, Pair<Float, Float>>()
    private val arcAngles = mutableMapOf<Pair<String, String>, Pair<Float, Float>>()

    // Socket receiver
    private var regionReceiver: RegionReceiver? = null

    init {
        initializePaints()
        initializeCounters()
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
            textSize = 32f
            textAlign = Paint.Align.CENTER
            typeface = Typeface.MONOSPACE
        }

        paintHighlight.color = colorBorder
        lightPointPaint.apply {
            color = Color.YELLOW  // or any bright color you prefer
            style = Paint.Style.FILL
        }
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
        NUMBERS.forEach { num ->
            secondaryCounters["NUM_$num"] = 0
        }
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

        // Calculate square boundary for rectangular Google Glass screen
        squareSize = minOf(w, h).toFloat()
        centerX = w / 2f
        centerY = h / 2f

        // Define square boundaries
        squareLeft = centerX - squareSize / 2
        squareTop = centerY - squareSize / 2
        squareRight = centerX + squareSize / 2
        squareBottom = centerY + squareSize / 2

        // Scale ring and inner circle based on square size
        val scale = squareSize / canvasWidth
        ringSize = 400f * scale
        innerRadius = 60f * scale

        // Update text size based on scale
        paintText.textSize = 32f * scale

        computeCharacterPositions()
    }

    private fun computeCharacterPositions() {
        characterPositions.clear()
        arcAngles.clear()

        // MAIN VIEW: Radial arrangement within sectors (exactly matching Python)
        // MAIN VIEW: Radial arrangement within sectors (exactly matching Python)
        val sectorInfo = mapOf(
            "TOP" to Triple(270f, ringSize * 0.25f, TOP),      // TOP angle should be 90 degrees
            "RIGHT" to Triple(0f, ringSize * 0.25f, RIGHT),
            "BOTTOM" to Triple(90f, ringSize * 0.25f, BOTTOM),
            "LEFT" to Triple(180f, ringSize * 0.25f, LEFT)
        )

        sectorInfo.forEach { (section, info) ->
            val (centerAngle, centerRadius, letters) = info

            letters.forEachIndexed { i, char ->
                val baseRadius = ringSize * 0.075f
                val angleSpread = 50f

                val angles = if (letters.size == 1) {
                    listOf(centerAngle)
                } else {
                    val startAngle = centerAngle - angleSpread / 2
                    val endAngle = centerAngle + angleSpread / 2
                    val charAngle = startAngle + i * angleSpread / (letters.size - 1)
                    listOf(charAngle)
                }

                val charAngle = Math.toRadians(angles[0].toDouble())
                val radiusVariation = baseRadius + (i % 2) * ringSize * 0.0125f
                val totalRadius = centerRadius + radiusVariation * 0.7f

                val x = centerX + totalRadius * cos(charAngle).toFloat()
                val y = centerY - totalRadius * sin(charAngle).toFloat()  // Make sure this is correct

                characterPositions[Pair(char, "MAIN")] = Pair(x, y)
            }
        }

        // SECONDARY VIEW: Full circle with equal segments (exactly matching Python)
        val secondaryRadius = ringSize * 0.3f
        val sections = mapOf("RIGHT" to RIGHT, "TOP" to TOP, "LEFT" to LEFT, "BOTTOM" to BOTTOM)

        sections.forEach { (section, chars) ->
            chars.forEachIndexed { i, char ->
                val startAngle = 360f * i / chars.size
                val endAngle = 360f * (i + 1) / chars.size
                val textAngle = Math.toRadians(((startAngle + endAngle) / 2).toDouble())

                // Store angles for arc drawing
                arcAngles[Pair(char, section)] = Pair(startAngle, endAngle - startAngle)

                // Position text at 90% of radius
                val x = centerX + (secondaryRadius * 0.9f) * cos(textAngle).toFloat()
                val y = centerY - (secondaryRadius * 0.9f) * sin(textAngle).toFloat()
                characterPositions[Pair(char, section)] = Pair(x, y)
            }
        }

        // NUMBERS: 10 equally spaced positions (exactly matching Python)
        NUMBERS.forEachIndexed { i, num ->
            val startAngle = 360f * i / NUMBERS.size
            val endAngle = 360f * (i + 1) / NUMBERS.size
            val textAngle = Math.toRadians(((startAngle + endAngle) / 2).toDouble())

            // Store angles for arc drawing
            arcAngles[Pair(num, "NUM")] = Pair(startAngle, endAngle - startAngle)

            // Position text at 90% of radius
            val x = centerX + (secondaryRadius * 0.9f) * cos(textAngle).toFloat()
            val y = centerY + (secondaryRadius * 0.9f) * sin(textAngle).toFloat()
            characterPositions[Pair(num, "NUM")] = Pair(x, y)
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        // Clear background
        canvas.drawColor(colorBackground)

        // Draw square boundary for Google Glass rectangular screen
        drawSquareBoundary(canvas)

        // Draw in correct order - matching Python exactly
        drawMainRing(canvas)
        drawCurrentStateContent(canvas)
        drawWedgeCornerButtons(canvas)
        drawCenterCircle(canvas)
        // Add light point drawing
        drawLightPoint(canvas)
    }

    private fun drawLightPoint(canvas: Canvas) {
        lightPointPosition?.let { position ->
            val currentTime = System.currentTimeMillis()
            if (currentTime - lightPointStartTime < LIGHT_POINT_DURATION) {
                val lightRadius = ringSize * 0.05f // Adjust size as needed

                val (x, y) = when (position) {
                    "center" -> Pair(centerX, centerY)
                    "top_mid" -> Pair(centerX, centerY - ringSize * 0.63f)
                    "bottom_mid" -> Pair(centerX, centerY + ringSize * 0.63f)
                    "left_mid" -> Pair(centerX - ringSize * 0.63f, centerY)
                    "right_mid" -> Pair(centerX + ringSize * 0.63f, centerY)
                    else -> Pair(centerX, centerY)
                }

                canvas.drawCircle(x, y, lightRadius, lightPointPaint)
            }
        }
    }

    private fun drawSquareBoundary(canvas: Canvas) {
        val boundaryPaint = Paint(paintBorder).apply {
            style = Paint.Style.STROKE
            strokeWidth = 4f
            alpha = 128 // Semi-transparent to show boundary without being intrusive
        }

        canvas.drawRect(squareLeft, squareTop, squareRight, squareBottom, boundaryPaint)
    }

    private fun drawMainRing(canvas: Canvas) {
        // Draw outer ring background - EXACTLY like Python
        val rect = RectF(
            centerX - ringSize / 2, centerY - ringSize / 2,
            centerX + ringSize / 2, centerY + ringSize / 2
        )

        // Background circle
        val bgPaint = Paint(paintRing).apply { color = colorBackground }
        canvas.drawOval(rect, bgPaint)
        canvas.drawOval(rect, paintBorder)
    }

    private fun drawCurrentStateContent(canvas: Canvas) {
        when (currentState) {
            "MAIN" -> drawMainView(canvas)
            "NUM" -> drawNumView(canvas)
            in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") -> drawSecondaryView(canvas)
        }
    }

    private fun drawMainView(canvas: Canvas) {
        val rect = RectF(
            centerX - ringSize / 2, centerY - ringSize / 2,
            centerX + ringSize / 2, centerY + ringSize / 2
        )

        // Draw four main sections with highlighting - EXACTLY like Python
        val sections = listOf("TOP", "RIGHT", "BOTTOM", "LEFT")
        val startAngles = listOf(45f, 315f, 225f, 135f)

        sections.forEachIndexed { index, section ->
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(counters[section] ?: 0)
            }

            // Draw filled arc
            canvas.drawArc(rect, startAngles[index], 90f, true, paint)
            // Draw border
            canvas.drawArc(rect, startAngles[index], 90f, true, paintBorder)
        }

        // Draw character labels - positioned exactly like Python
        // Draw character labels - positioned exactly like Python
        val letterSections = mapOf("TOP" to TOP, "RIGHT" to RIGHT, "BOTTOM" to BOTTOM, "LEFT" to LEFT)

        letterSections.forEach { (section, letters) ->
            letters.forEach { char ->
                characterPositions[Pair(char, "MAIN")]?.let { (x, y) ->
                    val textPaint = Paint(paintText).apply {
                        textSize = paintText.textSize * 0.6f  // Small text like Python
                        color = colorText  // Make sure color is set
                        textAlign = Paint.Align.CENTER
                        isAntiAlias = true
                    }
                    // Add some debugging - make sure coordinates are valid
                    if (x.isFinite() && y.isFinite()) {
                        canvas.drawText(char.uppercase(), x, y + textPaint.textSize / 3, textPaint)
                    }
                }
            }
        }
        TOP.forEach { char ->
            characterPositions[Pair(char, "MAIN")]?.let { (x, y) ->
                println("TOP char $char at position ($x, $y)")
            }
        }
    }

    private fun drawSecondaryView(canvas: Canvas) {
        val rect = RectF(
            centerX - ringSize / 2, centerY - ringSize / 2,
            centerX + ringSize / 2, centerY + ringSize / 2
        )

        val letters = when (currentState) {
            "RIGHT" -> RIGHT
            "TOP" -> TOP
            "LEFT" -> LEFT
            "BOTTOM" -> BOTTOM
            else -> emptyList()
        }

        // FIRST PHASE: Draw all the arcs (background)
        letters.forEachIndexed { i, char ->
            arcAngles[Pair(char, currentState)]?.let { (startAngle, sweepAngle) ->
                val counterKey = "${currentState}_$i"
                val paint = Paint(paintRing).apply {
                    color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
                }

                // Draw filled arc
                canvas.drawArc(rect, startAngle, sweepAngle, true, paint)
                // Draw border
                canvas.drawArc(rect, startAngle, sweepAngle, true, paintBorder)
            }
        }

        // SECOND PHASE: Draw all the text (foreground)
        letters.forEachIndexed { i, char ->
            characterPositions[Pair(char, currentState)]?.let { (x, y) ->
                val textPaint = Paint(paintText).apply {
                    color = colorText
                    textAlign = Paint.Align.CENTER
                    isAntiAlias = true
                    textSize = paintText.textSize  // Don't make it smaller
                }
                canvas.drawText(char, x, y + textPaint.textSize / 3, textPaint)
            }
        }
    }

    private fun drawNumView(canvas: Canvas) {
        val rect = RectF(
            centerX - ringSize / 2, centerY - ringSize / 2,
            centerX + ringSize / 2, centerY + ringSize / 2
        )

        // FIRST: Draw all the arcs (background)
        NUMBERS.forEach { num ->
            arcAngles[Pair(num, "NUM")]?.let { (startAngle, sweepAngle) ->
                val counterKey = "NUM_$num"
                val paint = Paint(paintRing).apply {
                    color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
                }

                // Draw filled arc
                canvas.drawArc(rect, startAngle, sweepAngle, true, paint)
                // Draw border
                canvas.drawArc(rect, startAngle, sweepAngle, true, paintBorder)
            }
        }

        // SECOND: Draw all the text (foreground)
        NUMBERS.forEach { num ->
            characterPositions[Pair(num, "NUM")]?.let { (x, y) ->
                val textPaint = Paint(paintText).apply {
                    color = colorText
                    textAlign = Paint.Align.CENTER
                    isAntiAlias = true
                    textSize = paintText.textSize  // Don't make it smaller
                }
                canvas.drawText(num, x, y + textPaint.textSize / 3, textPaint)
            }
        }
    }

    private fun drawWedgeCornerButtons(canvas: Canvas) {
        // Calculate wedge dimensions - each button extends exactly half the square side length
        val halfSide = squareSize / 4f  // Half of half the square (quarter of total)
        val circleRadius = ringSize / 2f

        // Button data: text, position, key
        val buttons = listOf(
            Triple("NUM", Pair(squareLeft, squareTop), "NUM"),           // Top-left
            Triple("⟲", Pair(squareRight, squareTop), "RETURN"),        // Top-right
            Triple("X", Pair(squareLeft, squareBottom), "DELETE"),       // Bottom-left
            Triple("✔", Pair(squareRight, squareBottom), "CONFIRM")     // Bottom-right
        )

        buttons.forEach { (text, pos, buttonKey) ->
            val (cornerX, cornerY) = pos

            // Create wedge path (intersection of circle and square corner)
            val wedgePath = Path()

            // Determine wedge boundaries based on corner position
            when {
                cornerX == squareLeft && cornerY == squareTop -> {
                    // Top-left wedge
                    wedgePath.moveTo(squareLeft, squareTop)
                    wedgePath.lineTo(squareLeft + halfSide, squareTop)
                    wedgePath.lineTo(squareLeft, squareTop + halfSide)
                    wedgePath.close()
                }
                cornerX == squareRight && cornerY == squareTop -> {
                    // Top-right wedge
                    wedgePath.moveTo(squareRight, squareTop)
                    wedgePath.lineTo(squareRight - halfSide, squareTop)
                    wedgePath.lineTo(squareRight, squareTop + halfSide)
                    wedgePath.close()
                }
                cornerX == squareLeft && cornerY == squareBottom -> {
                    // Bottom-left wedge
                    wedgePath.moveTo(squareLeft, squareBottom)
                    wedgePath.lineTo(squareLeft + halfSide, squareBottom)
                    wedgePath.lineTo(squareLeft, squareBottom - halfSide)
                    wedgePath.close()
                }
                cornerX == squareRight && cornerY == squareBottom -> {
                    // Bottom-right wedge
                    wedgePath.moveTo(squareRight, squareBottom)
                    wedgePath.lineTo(squareRight - halfSide, squareBottom)
                    wedgePath.lineTo(squareRight, squareBottom - halfSide)
                    wedgePath.close()
                }
            }

            // Clip the wedge with the circle boundary
            val circlePath = Path()
            circlePath.addCircle(centerX, centerY, circleRadius, Path.Direction.CW)

            // Create intersection path
            val intersectionPath = Path()
            intersectionPath.op(wedgePath, circlePath, Path.Op.INTERSECT)

            // Draw wedge background with highlighting - Enhanced with blue background
            val paint = Paint(paintRing).apply {
                color =  getHighlightColor(counters[buttonKey] ?: 0)
//                style = Paint.Style.FILL
            }

            canvas.drawPath(intersectionPath, paint)

// Draw wedge border - make it less prominent when highlighted
            val borderPaint = Paint(paintBorder).apply {
                style = Paint.Style.STROKE
                // Reduce border opacity when button is highlighted
                alpha = if ((counters[buttonKey] ?: 0) > 0) 128 else 255
            }
            canvas.drawPath(intersectionPath, borderPaint)
            // Calculate text position (center of the wedge)
            val textX = when {
                cornerX == squareLeft -> squareLeft + halfSide * 0.5f  // Move text more toward center
                else -> squareRight - halfSide * 0.5f
            }
            val textY = when {
                cornerY == squareTop -> squareTop + halfSide * 0.5f    // Move text more toward center
                else -> squareBottom - halfSide * 0.5f
            }

            // Draw text with appropriate color
            val textColor = when (text) {
                "✔" -> colorConfirm
                "X" -> colorCancel
                else -> colorText
            }

            val textPaint = Paint(paintText).apply {
                color = textColor
                textSize = paintText.textSize * 0.8f  // Increase text size slightly
                textAlign = Paint.Align.CENTER       // Ensure center alignment
                typeface = Typeface.DEFAULT_BOLD     // Make text bolder for visibility
            }
            canvas.drawText(text, textX, textY + textPaint.textSize / 3, textPaint)
        }
    }

    private fun drawCenterCircle(canvas: Canvas) {
        // Draw center circle
        val centerPaint = Paint(paintRing).apply {
            color = getHighlightColor(counters["CENTER"] ?: 0)
        }

        canvas.drawCircle(centerX, centerY, innerRadius, centerPaint)
        canvas.drawCircle(centerX, centerY, innerRadius, paintBorder)

        // Draw center text
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
            // Add string command handling before number parsing
            when (command.lowercase()) {
                "center" -> showLightPoint("center")
                "top_mid" -> showLightPoint("top_mid")
                "left_mid" -> showLightPoint("left_mid")
                "bottom_mid" -> showLightPoint("bottom_mid")
                "right_mid" -> showLightPoint("right_mid")
                else -> {
                    // Existing number command processing
                    val commandNum = command.toIntOrNull() ?: return
                    when (commandNum) {
                        in 1..20 -> processSectorInput(commandNum)
                        in 21..25 -> processButtonInput(commandNum)
                    }
                }
            }

            invalidate() // Trigger redraw
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    private fun showLightPoint(position: String) {
        lightPointPosition = position
        lightPointStartTime = System.currentTimeMillis()

        // Schedule removal after 3 seconds
        Handler(Looper.getMainLooper()).postDelayed({
            lightPointPosition = null
            invalidate()
        }, LIGHT_POINT_DURATION)
    }

    private fun processSectorInput(sector: Int) {
        when (currentState) {
            "MAIN" -> {
                sectorMappings["MAIN"]?.forEach { (section, sectors) ->
                    if (sector in sectors) {
                        counters[section] = (counters[section] ?: 0) + 1
                        if (counters[section]!! >= SELECTION_THRESHOLD) {
                            counters[section] = 0
                            resetAllCounters()
                            currentState = section
                        }
                        return
                    }
                }
                dimCurrentSelection()
            }

            in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") -> {
                val section = currentState
                val chars = when (section) {
                    "RIGHT" -> RIGHT
                    "TOP" -> TOP
                    "LEFT" -> LEFT
                    "BOTTOM" -> BOTTOM
                    else -> emptyList()
                }

                // Direct sector-to-character mapping for secondary views
                val sectorFound = when (section) {
                    "RIGHT" -> {
                        when (sector) {
                            in 1..4 -> { incrementCharacterCounter(section, 0, "u"); true }
                            in 5..8 -> { incrementCharacterCounter(section, 1, "o"); true }
                            in 9..12 -> { incrementCharacterCounter(section, 2, "i"); true }
                            in 13..16 -> { incrementCharacterCounter(section, 3, "e"); true }
                            in 17..20 -> { incrementCharacterCounter(section, 4, "a"); true }
                            else -> false
                        }
                    }
                    "TOP" -> {
                        when (sector) {
                            in 1..3 -> { incrementCharacterCounter(section, 0, "h"); true }
                            in 4..6 -> { incrementCharacterCounter(section, 1, "l"); true }
                            in 7..9 -> { incrementCharacterCounter(section, 2, "d"); true }
                            in 10..11 -> { incrementCharacterCounter(section, 3, "r"); true }
                            in 12..15 -> { incrementCharacterCounter(section, 4, "n"); true }
                            in 16..17 -> { incrementCharacterCounter(section, 5, "t"); true }
                            in 18..20 -> { incrementCharacterCounter(section, 6, "s"); true }
                            else -> false
                        }
                    }
                    "LEFT" -> {
                        when (sector) {
                            in 1..3 -> { incrementCharacterCounter(section, 0, "f"); true }
                            in 4..6 -> { incrementCharacterCounter(section, 1, "p"); true }
                            in 7..9 -> { incrementCharacterCounter(section, 2, "y"); true }
                            in 10..12 -> { incrementCharacterCounter(section, 3, "g"); true }
                            in 13..15 -> { incrementCharacterCounter(section, 4, "m"); true }
                            in 16..18 -> { incrementCharacterCounter(section, 5, "w"); true }
                            in 19..20 -> { incrementCharacterCounter(section, 6, "c"); true }
                            else -> false
                        }
                    }
                    "BOTTOM" -> {
                        when (sector) {
                            in 1..3 -> { incrementCharacterCounter(section, 0, "x"); true }
                            in 4..6 -> { incrementCharacterCounter(section, 1, "z"); true }
                            in 7..9 -> { incrementCharacterCounter(section, 2, "v"); true }
                            in 10..12 -> { incrementCharacterCounter(section, 3, "k"); true }
                            in 13..15 -> { incrementCharacterCounter(section, 4, "q"); true }
                            in 16..18 -> { incrementCharacterCounter(section, 5, "b"); true }
                            in 19..20 -> { incrementCharacterCounter(section, 6, "j"); true }
                            else -> false
                        }
                    }
                    else -> false
                }

                if (!sectorFound) {
                    dimCurrentSelection()
                }
            }

            "NUM" -> {
                sectorMappings["NUM"]?.forEach { (number, sectors) ->
                    if (sector in sectors) {
                        val counterKey = "NUM_$number"
                        secondaryCounters[counterKey] = (secondaryCounters[counterKey] ?: 0) + 1
                        if (secondaryCounters[counterKey]!! >= SELECTION_THRESHOLD) {
                            addNumber(number)
                        }
                        return
                    }
                }
                dimCurrentSelection()
            }
        }
    }

    private fun processButtonInput(buttonCode: Int) {
        when (buttonCode) {
            21 -> { // NUM
                counters["NUM"] = (counters["NUM"] ?: 0) + 1
                if (counters["NUM"]!! >= SELECTION_THRESHOLD) {
                    counters["NUM"] = 0
                    resetAllCounters()
                    currentState = "NUM"
                }
            }

            22 -> { // RETURN
                counters["RETURN"] = (counters["RETURN"] ?: 0) + 1
                if (counters["RETURN"]!! >= SELECTION_THRESHOLD) {
                    counters["RETURN"] = 0
                    resetAllCounters()
                    currentState = "MAIN"
                }
            }

            23 -> { // DELETE
                // Remove the early return line completely:
                // if (currentState in listOf("TOP", "RIGHT", "BOTTOM", "LEFT")) return

                counters["DELETE"] = (counters["DELETE"] ?: 0) + 1
                if (counters["DELETE"]!! >= SELECTION_THRESHOLD) {
                    counters["DELETE"] = 0
                    if (currentText.isNotEmpty()) {
                        currentText = currentText.dropLast(1)
                    } else {
                        tts("No")
                    }
                }
            }

            24 -> { // CONFIRM
                // Remove the early return line completely:
                // if (currentState in listOf("TOP", "RIGHT", "BOTTOM", "LEFT")) return

                counters["CONFIRM"] = (counters["CONFIRM"] ?: 0) + 1
                if (counters["CONFIRM"]!! >= SELECTION_THRESHOLD) {
                    counters["CONFIRM"] = 0
                    if (currentText.isNotEmpty()) {
                        confirmText()
                    } else {
                        tts("Yes")
                    }
                }
            }

            25 -> { // CENTER
                counters["CENTER"] = (counters["CENTER"] ?: 0) + 1
                if (counters["CENTER"]!! >= SELECTION_THRESHOLD) {
                    counters["CENTER"] = 0
                    if (currentState == "NUM") {
                        addDecimalPoint()
                    } else {
                        addSpace()
                    }
                }
            }
        }
    }

    private fun incrementCharacterCounter(section: String, charIndex: Int, char: String) {
        val counterKey = "${section}_$charIndex"
        secondaryCounters[counterKey] = (secondaryCounters[counterKey] ?: 0) + 1
        if (secondaryCounters[counterKey]!! >= SELECTION_THRESHOLD) {
            addCharacter(char)
        }
    }

    private fun resetAllCounters() {
        counters.keys.forEach { counters[it] = 0 }
        secondaryCounters.keys.forEach { secondaryCounters[it] = 0 }
    }

    private fun dimCurrentSelection() {
        when (currentState) {
            "MAIN" -> {
                var maxCounter = 0
                var maxSection: String? = null
                listOf("TOP", "RIGHT", "BOTTOM", "LEFT").forEach { section ->
                    val counter = counters[section] ?: 0
                    if (counter > maxCounter) {
                        maxCounter = counter
                        maxSection = section
                    }
                }
                maxSection?.let {
                    counters[it] = maxOf(0, (counters[it] ?: 0) - 1)
                }
            }

            in listOf("TOP", "RIGHT", "BOTTOM", "LEFT") -> {
                val section = currentState
                val chars = when (section) {
                    "RIGHT" -> RIGHT
                    "TOP" -> TOP
                    "LEFT" -> LEFT
                    "BOTTOM" -> BOTTOM
                    else -> emptyList()
                }

                var maxCounter = 0
                var maxKey: String? = null
                chars.indices.forEach { i ->
                    val counterKey = "${section}_$i"
                    val counter = secondaryCounters[counterKey] ?: 0
                    if (counter > maxCounter) {
                        maxCounter = counter
                        maxKey = counterKey
                    }
                }
                maxKey?.let {
                    secondaryCounters[it] = maxOf(0, (secondaryCounters[it] ?: 0) - 1)
                }
            }

            "NUM" -> {
                var maxCounter = 0
                var maxKey: String? = null
                NUMBERS.forEach { num ->
                    val counterKey = "NUM_$num"
                    val counter = secondaryCounters[counterKey] ?: 0
                    if (counter > maxCounter) {
                        maxCounter = counter
                        maxKey = counterKey
                    }
                }
                maxKey?.let {
                    secondaryCounters[it] = maxOf(0, (secondaryCounters[it] ?: 0) - 1)
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
            tts(currentText)
            currentText = ""
            resetAllCounters()
            currentState = "MAIN"
        }
    }

    private fun tts(text: String) {
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        tts?.shutdown()
        regionReceiver?.stop()
    }
}
