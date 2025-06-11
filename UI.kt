package com.example.glassgaze

import android.content.Context
import android.graphics.*
import androi", "7", "8", "9",d.os.Handler
import android.os. "0")
        
        private const val SELECTION_THRESHOLD = 4
        private const val MAX_DISPLAY_CHARS = 7
        
        private valLooper
import android.speech.tts.TextToSpeech
import androi STATES = listOf("MAIN", "RIGHTd.util.AttributeSet
import android.view.View
import kotlinx.coroutines.*
import java.io.Buffere", "TOP", "LEFT", "BOTTOM", "NUM")
    }

    // Colors matching Python exactly
    private val colorBackground = ColordReader
import java.io.InputStreamReader.parseColor("#f8fafc")
    private
import java.net.ServerSocket
import java.net.Socket
import java.util.*
import kotlin.math.*

class AACKeyboardView @JvmOverloads constructor( val colorBorder = Color.parseColor("#3b82f6")
    private val color
    context: Context,
    attrs: AttributeSet? = null,
    defText = Color.parseColor("#1e293StyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    // Constants matching Python exactly
    companion object {
        private val RIGHTb")
    private val colorRing = Color.parseColor("#e2e8f0") = listOf("a", "e", "i", "
    private val colorConfirm = Color.parseColor("#10b981")
    private valo", "u")
        private val TOP = listOf("s", "t", "n", "r", "d", "l", "h colorCancel = Color.parseColor("#ef4444")
    private val colorSide = Color.parseColor")
        private val LEFT = listOf("c", "w", "m", "g", "y", "p", "f")
        private val("#f1f5f9")

    // Pa BOTTOM = listOf("j", "b", "qints
    private val paintBackground = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintBorder = Paint(Paint.ANTI_ALIAS_FLAG)", "k", "v", "z", "x")
        private val NUMBERS = listOf("1
    private val paintRing = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintText = Paint(Paint.", "2", "3", "4",ANTI_ALIAS_FLAG)
    private val paintHighlight = Paint(Paint "5", "6", "7", ".ANTI_ALIAS_FLAG)

    // Layout constants matching Python (500x500 canvas)
    private var canvasSize = 500f
    private8", "9", "0")
        
        private const val SELECTION_THRESHOLD = 4
        private const val MAX_DISPLAY_CHARS = 7
        
        private val STATES var centerX = 250f
    private var centerY = 250f
    private var ringSize = 400f // Increased from 300 by 1/3
    private var = listOf("MAIN", "RIGHT", "TOP", " ringOffset = 50f //LEFT", "BOTTOM", "NUM")
    }

    // Colors matching Python exactly
    private (500 - 400) / 2
    private var innerRadius = 60 val colorBackground = Color.parseColor("#f8fafc")
    private val colorBf // 120/2 for center circle
    private var outerRadius = 200f // 400/2 for ringorder = Color.parseColor("#3b82f6")

    // State variables
    private var currentState = "MAIN"
    
    private val colorText = Color.parseprivate var currentText = ""

    // Text-to-Speech
    private var tts: TextToSpeech? = null

    // Sector mappings matching Python exactly
    private val sectorMappings = mapOf(
        "MAIN" to mapOf(
            "TOPColor("#1e293b")
    private val colorRing = Color.parseColor("#e2e8f0")
    private val colorConfirm = Color.parseColor("#10b981")
    private val" to listOf(3, 4, 5, 6, 7),
            "LEFT colorCancel = Color.parseColor("#ef4444")
    private val colorSide = Color.parseColor" to listOf(8, 9, ("#f1f5f9")

    // Paint10, 11, 12, 13),
            "BOTTOM" to listOf(14, 15, 16, 17, 18),
            "RIGHT" to listOf(19, 20, 1, 2)
        ),
         objects
    private val paintBackground = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintBorder = Paint(Paint.ANTI_ALIAS_FLAG)
    private val"NUM" to mapOf(
            "1" to listOf(1),
            "2" to listOf(2, 3, paintRing = Paint(Paint.ANTI_ALIAS_FLAG)
    private val paintText = Paint(Paint.ANTI_ALIAS_FLAG)
     4),
            "3" to listOf(5, 6),
            "4" to listOf(7, 8),
            "5"private val paintHighlight = Paint(Paint.ANTI_ to listOf(9, 10),ALIAS_FLAG)

    // Layout variables - matching Python exactly
    
            "6" to listOf(11, 12),
            "7" to listOf(13, 14),
            "8" to listOf(15, private var centerX = 0f
    private var centerY = 0f
    private var canvasWidth = 50016),
            "9" to listOf(17, 18, 19),
            "0" to listOf(20)f  // Fixed canvas size like Python
    private var can
        ),
        // Individual character mappings forvasHeight = 500f
    private var ringSize = 400f     // Matches Python ring_size
    private var innerRadius = 60 secondary states
        "a" to mapOf("f   // Matches Python circle_size / 2

    // State variables
    private var0" to listOf(1, 2, 3 currentState = "MAIN"
    private var currentText, 4)),
        "e" to mapOf("0" to listOf(5, 6, 7, 8)),
        "i" = ""

    // Text-to-Speech
    private var tts: TextToSpeech? = null

    // Counter system matching Python exactly
    private val counters = m to mapOf("0" to listOf(utableMapOf<String, Int>().9, 10, 11, 12)),
        "o" to mapOf("0" to listOf(13, 14, 15, 16)),
        "u" to mapOf("0" to listapply {
        put("TOP", 0)Of(17, 18, 19, 20)),
        "s" to mapOf("
        put("RIGHT", 0)
        put("BOTTOM", 0)
        0" to listOf(1, 2, 3)),
        "t" to mapOf("0" to listOf(4, 5,put("LEFT", 0)
        put("NUM", 0)
        put("RETURN 6)),
        "n" to mapOf("0" to listOf(7, 8,", 0)
        put("DELETE", 0)
        put("CONFIRM", 0) 9)),
        "r" to map
        put("CENTER", 0)
    }
    
    private valOf("0" to listOf(10, secondaryCounters = mutableMapOf<String 11)),
        "d" to mapOf("0, Int>()

    // Character positions storage
    private val characterPositions = mutableMapOf" to listOf(12, 13, 14, 15)),
        "l" to mapOf("0" to<Pair<String, String>, Pair<Float, Float>>()
    private val characterAngles = mutableMapOf<Pair listOf(16, 17)),
        "h" to mapOf("0" to listOf(<String, String>, Pair<Float, Float>>() // For arc angles

    // Sector18, 19, 20))
    )

    // Unified counter mappings matching Python exactly
    private val sectorMappings = mapOf(
        " system
    private val counters = mutableMapOf<String, Int>().apply {
        // Main sectionMAIN" to mapOf(
            "TOP counters
        put("TOP", 0)
        put("RIGHT" to listOf(3, 4, 5, 6, 7),
            "", 0)
        put("BOTTOMLEFT" to listOf(8, 9, 10, 11, 12, 13),
            "BOTTOM" to listOf", 0)
        put("LEFT",(14, 15, 16,  0)
        // Corner button counters
        put17, 18),
            "RIGHT"("NUM", 0)
        put("RETURN to listOf(19, 20, 1, 2)
        ),
        "NUM" to mapOf(", 0)
        put("DELETE", 0)
        put("CONFIRM
            "1" to listOf(1),
            "2" to listOf(2, 3, 4),
            "3"", 0)
        put("CENTER", 0)
    }
    
    private val secondaryCounters = mutableMapOf<String to listOf(5, 6),
            "4" to listOf(7, 8),
            "5" to listOf(9, Int>()

    // Character, 10),
            "6" to listOf(11 positions
    private val characterPositions = mutableMapOf<Pair<String, String>,, 12),
            "7" to Pair<Float, Float>>()
    private val arcAngles = mutableMap listOf(13, 14),
            "8" to listOf(15, 16),
            "9" to listOf(17, 18, 19),
            Of<Pair<String, String>, Pair<Float, Float>>()

    // Socket receiver
    private var region"0" to listOf(20)
        )
    )

    // SocketReceiver: RegionReceiver? = null

    init {
        initializePaints()
        initialize receiver
    private var regionReceiver: RegionReceiver? = null

    initCounters()
        initializeTTS()
        startSocketListener()
    } {
        initializePaints()
        initializeCounters()
        initializeT

    private fun initializePaints() {
        paintBackground.color = colorBackgroundTS()
        computeCharacterPositions()
        startSocketListener()
    }
        
        paintBorder.apply {
            color = colorBorder
            style = Paint.Style

    private fun initializePaints() {
        paintBackground.color = colorBackground
        
        paintBorder.apply {
            color =.STROKE
            strokeWidth = 6 colorBorder
            style = Paint.Style.STROKE
            strokeWidth = 6f
        }
        
        paintRing.color = colorRingf
        }
        
        paintRing.color = colorRing
        
        paintText.apply {
            color = colorText
            textSize = when {
        
        paintText.apply {
            color = colorText
            textSize = 32
                canvasSize < 300 -> 24f  // Adjusted for Glass display
            textAlign = Paint.f  // Small font
                canvasSize < 600 -> 32f  // Middle font  
                elseAlign.CENTER
            typeface = Typeface.MONOSPACE
        }
        
        paintHighlight.color = colorBorder
    } -> 48f              // Large font
            }
            textAlign = Paint.

    private fun initializeCounters() {Align.CENTER
            typeface = Typeface
        // Initialize secondary counters exactly like Python
        val sections = mapOf(
            "RIGHT.MONOSPACE
        }
        
        paintHighlight.color = colorBorder
    }

    private fun initializeCounters()" to RIGHT,
            "TOP" to TOP, {
        // Initialize secondary counters for each character
        val sections = mapOf(
            "RIGHT" to RIGHT
            "LEFT" to LEFT,
            "BOTTOM" to BOTTOM
        )
        
        sections.forEach { (section, chars,
            "TOP" to TOP,
            "LEFT" to LEFT,
            ") ->
            chars.forEachIndexed { i, _ ->
                secondaryCounters["BOTTOM" to BOTTOM
        )
        
        sections.forEach { (section, chars) ->
            chars.forEachIndexed { i, _ ->
                secon${section}_$i"] = 0
            }daryCounters["${section}_$i"]
        }
        
        // Initialize number counters
        NUMBERS.forEach { num ->
            secondary = 0
            }
        }
        
        // Initialize number counters
        Counters["NUM_$num"] = 0
        NUMBERS.forEach { num ->
            secondaryCounters["NUM_$num"]}
    }

    private fun initializeTTS() {
        tts = TextToSpeech(context) { status -> = 0
        }
    }
            if (status == TextToSpeech.SUCCESS) {
                t

    private fun initializeTTS() {
        tts = TextToSpeech(ts?.language = Locale.US
            }
        }
    }

    privatecontext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale.US
            }
        }
    }

    private fun startSocketListener() {
         fun startSocketListener() {
        regionReceiver = RegionReceiver { command ->
            Handler(Looper.getMainLooper()).post {
                processCommand(command)
            regionReceiver = RegionReceiver { command ->
            Handler(Looper.}
        }
        regionReceiver?.startgetMainLooper()).post {
                process()
    }

    override fun onSCommand(command)
            }
        }
        regionReceiver?.start()
    }

    overrideizeChanged(w: Int, h: Int, oldw: Int, oldh: Int fun onSizeChanged(w: Int,) {
        super.onSizeChange h: Int, oldw: Int, oldh: Int) {
        super.ond(w, h, oldw, oldh)
        // Use fixed dimensions like Python, but scale if needed
        val scaleSizeChanged(w, h, oldw, oldh)
        
        // Scale everything proportionally to maintain aspect ratio
        val scale = minOf(w, h) / canvasSize
        canvasSize = min = minOf(w.toFloat() / canvasWidth, h.toFloat() / canvasHeight)
        
        centerX = w / 2f
        centerY = h / Of(w, h).toFloat()
        centerX = w / 2f2f
        ringSize = 400f * scale
        centerY = h / 2f
        ringSize = 400f * scale
        ringOffset = (canvasSize - ring
        innerRadius = 60f * scale
        
        // Adjust text size based on scale
        paintText.textSize = 32f * scale
        
        computeCharacterPositions()
    }

    private fun computeCharacterPositions() {
        // MAIN VIEW: Radial arrangement within sectors -Size) / 2f
        innerRadius = 60f * scale
        outerRadius = ringSize / 2f
         EXACTLY like Python
        val sectorInfo = mapOf(
            "TOP" to Triple(
        // Update text size based on scale
        paintText.textSize = when {
            canvasSize < 300 -> 16f
            canvasSize < 600 -> 24f  90f, ringSize * 0.25
            else -> 32f
        }
        
        computeCharacterPositions()
    }

    private fun computeCharacterf, TOP),      // center_radiusPositions() {
        characterPositions.clear() = 100 scaled
            "RIGHT"
        arcAngles.clear()

        // MAIN VIEW: Radial arrangement within to Triple(0f, ringSize * 0.25f, RIGHT), sectors (exactly matching Python)
        val sectorInfo = mapOf(
            "
            "BOTTOM" to Triple(270f, ringSize *TOP" to Triple(90f, outerRadius * 0.5f, TOP),
            "RIGHT" to Triple(0 0.25f, BOTTOM),
            "LEFT" to Triple(180ff, outerRadius * 0.5f, RIGHT), 
            ", ringSize * 0.25f, LEFT)
        )

        sectorInfo.forEach { (section, infoBOTTOM" to Triple(270) ->
            val (centerAnf, outerRadius * 0.5gle, centerRadius, letters) = info
            
            letters.forEachIndexed { i, char ->
                val basef, BOTTOM),
            "LEFT" to Triple(180f, outerRadius *Radius = ringSize * 0.075f  // 30 scaled
                val angleSpread = 50f
                
                if 0.5f, LEFT)
         (letters.size == 1) {)

        sectorInfo.forEach {
                    val angleRad = Math.toRadians( (section, info) ->
            val (centerAngle, centerRadius, letters) = info
            centerAngle.toDouble())
                    val x = centerX + centerRadius * cos(angleRad).letters.forEachIndexed { i, char ->
                val baseRadius = outerRadius * 0.15f
                val angletoFloat()
                    val y = centerY - centerRadius * sin(angleRaSpread = 50f // degrees
                
                val angles = if (letters.size == 1) {d).toFloat()
                    characterPositions[
                    listOf(centerAngle)
                } else {
                    valPair(char, "MAIN")] = Pair( startAngle = centerAngle - angleSpread / 2
                    val enx, y)
                } else {dAngle = centerAngle + angleSpread / 2
                    (
                    val startAngle = centerAngle - angleSpread / 2
                    0 until letters.size).map { 
                        startAngle + it * angleSpread / (val endAngle = centerAngle + angleSpread / 2
                    val charAngle = startAnletters.size - 1)
                    }
                }
                
                val charAngle = Math.toRadians(gle + i * angleSpread / (letters.size - 1)
                    
                    val charAngleRad = Math.toRadians(charAngle.toDouble())
                    angles[i].toDouble())
                val radiusVariation = baseval radiusVariation = baseRadius +Radius + (i % 2) * outerRadius * 0.025f
                val x = centerX + (i % 2) * ringSize * 0.0125f
                    val totalRadius = centerRadius + radiusVariation * 0.7f
                    
                 (centerRadius + radiusVariation * 0.7f) * cos(char    val x = centerX + totalRadius * cos(charAngleRad).toFloat()
                    val y = centerY - totalRadius * sin(charAngleRad).toFloat()
                    characterPositions[Pair(char, "MAIN"Angle).toFloat()
                val y = centerY - (centerRadius + radiusVariation * 0.7f) * sin(charAngle).toFloat()
                
                characterPositions[Pair(char, "MAIN")] =)] = Pair(x, y)
                }
            }
        } Pair(x, y)
            }

        // SECONDARY VIEW: Full circle with equal
        }

        // SECONDARY VIEW: Full circle with equal segments (exactly matching Python) segments - EXACTLY like Python
        val secondaryRadius = ringSize * 0.3f  
        val sections = mapOf("RIGHT// 120 scaled
        val sections = mapOf("" to RIGHT, "TOP" to TOP, "LEFT" to LEFT, "BOTTOM"RIGHT" to RIGHT, "TOP" to TOP, "LEFT" to LEFT, "BOTTOM" to BOTTOM)
        
        sections. to BOTTOM)
        sections.forEach { (sectionforEach { (section, chars) ->
            , chars) ->
            chars.forEachIndexed { i, char ->
                val startchars.forEachIndexed { i, char ->
                val startAngle = 360Angle = 360f * i / chars.size
                val endAngle = 360f * (i + 1) / chars.size
                val textAngle = Mathf * i / chars.size
                val endAngle = 360f * (i.toRadians(((startAngle + en + 1) / chars.size
                dAngle) / 2).toDouble())val textAngle = Math.toRadians(((startAngle + endAngle) / 
                
                // Store arc angles for drawing
                arcAngles[Pair(char2).toDouble())
                
                // Store angles for arc drawing
                characterAngles[Pair(char, section)] = Pair(startAngle, en, section)] = Pair(startAngle, endAngle - startAngle)
                
                val x = centerX + (outerRadius * 0.9f) * cos(textAngledAngle)
                
                // Position text at 90% of radius
                val x = centerX +).toFloat()
                val y = centerY - (outerRadius * 0.9f) * sin(textAngle). (secondaryRadius * 0.9f)toFloat()
                characterPositions[Pair * cos(textAngle).toFloat()
                val y = centerY - (secondaryRadius * 0.9f) * sin(textAngle).toFloat()
                characterPositions[Pair(char, section)] = Pair(x, y)
            }
        }

        // NUMBERS(char, section)] = Pair(x, y)
            }
        }

        // NUMBERS: 10 equally spaced positions (exactly matching Python)
        NUMBERS.forEachIndexed { i, num ->
            val startAngle = 360f * i /: 10 equally spaced positions - EXACTLY like Python
        NUMBERS.forEachIndexed { i, NUMBERS.size
            val endAngle = 360f * (i + 1) num ->
            val startAngle = 360 / NUMBERS.size
            val textAnf * i / NUMBERS.size
            gle = Math.toRadians(((startval endAngle = 360f * (i + 1)Angle + endAngle) / 2).toDouble())
            
            // Store arc angles for drawing
            arcAngles / NUMBERS.size
            val textAngle = Math.toRadians(((startAngle + endAn[Pair(num, "NUM")]gle) / 2).toDouble())
            
            // Store angles for arc drawing
            characterAngles[ = Pair(startAngle, endAngle - startAngle)
            
            val x = centerX + (outerRadius * 0.9f) * cos(Pair(num, "NUM")] = Pair(startAngle, endAngle)
            
            // Position text at 90% of radius
            val x = centertextAngle).toFloat()
            val y = centerY - (outerRadius *X + (secondaryRadius * 0.9f) * cos(textAngle).toFloat()
            val y = centerY 0.9f) * sin(textAngle).toFloat()
            characterPosit - (secondaryRadius * 0.9ions[Pair(num, "NUM")] = Pair(x, y)
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onf) * sin(textAngle).toFloat()
            characterPositions[PairDraw(canvas)
        
        // Clear(num, "NUM")] = Pair background
        canvas.drawColor(colorBackground)(x, y)
        }
    }

    override
        
        // Draw in correct layer order
        drawOuterRing(canvas)
        
        when (currentState) {
            "MAIN fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        // Clear" -> drawMainView(canvas)
            "NUM" -> drawNumView(canvas)
             background
        canvas.drawColor(colorBackground)
        
        // Draw in correct order - matching Python exactly
        drawMainRing(canvas)
        drawCurrentStateContent(canvas)
        in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") ->drawCornerButtons(canvas)
        drawCenter drawSecondaryView(canvas)
        Circle(canvas)
    }

    private fun drawMainRing(canvas: Canvas) {}
        
        drawCornerButtons(canvas)
        drawCenterCircle(canvas)
    }

    private fun drawOuterRing
        // Draw outer ring background - EXACTLY like Python
        val offset = ((canvas: Canvas) {
        val rect = RectF(
            centerX - outerRadius, centerY - outerRadius,minOf(width, height) - ringSize) / 2
        val rect = RectF(
            centerX - ringSize / 2, centerY - ringSize / 2,
            centerX + outerRadius, centerY + outerRadius
        )
        
        // Draw background circle
        val backgroundPaint = Paint(paintRing).apply { 
            style
            centerX + ringSize / 2, centerY + ringSize / 2
         = Paint.Style.FILL
            color = colorBackground 
        }
        )
        
        // Background circle
        val bgPaint = Paint(paintRing).apply {canvas.drawOval(rect, backgroundPaint)
        
        // Draw border
        canvas.drawO color = colorBackground }
        canvas.drawOval(rect, bgPaint)
        canvas.drawOval(rect, paintBorder)
    }

    private fun drawCurrentStateContent(val(rect, paintBorder)
    }

    private fun drawMainView(canvas: Canvas) {
        val rect = Rcanvas: Canvas) {
        when (currentState) {ectF(
            centerX - outerRadius, centerY - outerRadius,
            centerX + outerRadius, centerY + outerRadius
        )
        
            "MAIN" -> drawMainView(canvas)
            
        // Draw four main sections matching Python exactly"NUM" -> drawNumView(canvas)
            in listOf("RIGHT", "TOP", "LEFT", "BOTTOM") -> drawSecondaryView(canvas
        val sections = listOf("TOP", "RIGHT", "BOTTOM", "LEFT"))
        }
    }

    private fun drawMainView(canvas: Canvas) {
        val
        val startAngles = listOf( rect = RectF(
            centerX - ring45f, 315f, 225f, 135f)
        
        sections.forEachIndexed { index, section ->
            val paint = Paint(paintRSize / 2, centerY - ringSize / 2,
            centerX + ringSize / 2, centerY + ringSize / 2
        )
        
        ing).apply {
                style = Paint.Style.FILL
                color = getHighlightColor(counters[// Draw four main sections with highlighting - EXACTLY like Python
        val sections = listOf("TOP", "RIGHT", "section] ?: 0)
            }
            
            // Draw filled arc (NOT using useCenter to avoid pie slice effect)
            canvasBOTTOM", "LEFT")
        val.drawArc(rect, startAngles[index], 90f, false, paint)
            
             startAngles = listOf(45f, 315f, 225f, 135f)
        
        sections.forEachIndexed { index// Draw border
            canvas.drawArc(rect, start, section ->
            val paint = Paint(paintRAngles[index], 90f, false, paintBorder)
        }
        
        // Draw character labels
        val letterSections = maping).apply {
                color = getHighlightColor(counters[section] ?: 0)
            }
            
            Of("TOP" to TOP, "RIGHT" to RIGHT, "BOTTOM" to BOTTOM, "// Draw filled arc
            canvas.drawArc(rect, startAngles[indexLEFT" to LEFT)
        letterSections.forEach { (section, letters) ->
            letters], 90f, true, paint)
            // Draw border
            canvas.drawArc(rect, startAngles[index], 90f, true, paintBorder).forEach { char ->
                character
        }
        
        // Draw character labels - positioned exactly like Python
        valPositions[Pair(char, "MAIN")]?.let { (x, y) ->
                    canvas letterSections = mapOf("TOP" to TOP, "RIGHT" to RIGHT, "BOTTOM".drawText(char, x, y + paintText.textSize / to BOTTOM, "LEFT" to LEFT) 3, paintText)
                }
            }
        }
    }

    private fun drawSecondaryView(canvas: Canvas) {
        val rect = R
        letterSections.forEach { (section, lettersectF(
            centerX - outer) ->
            letters.forEach { char ->
                Radius, centerY - outerRadius,
            centerX + outerRadius, centerY + outerRadius
        )
        characterPositions[Pair(char, "
        val letters = when (currentState) {
            "RIGHT" -> RIGHT
            MAIN")]?.let { (x, y) ->
                    val textPaint = Paint(paint"TOP" -> TOP
            "LEFT"Text).apply { 
                        text -> LEFT
            "BOTTOM" ->Size = paintText.textSize * 0.6f  // Small text like Python
                     BOTTOM
            else -> emptyList()
        }
        
        letters.forEachIndexed { i, char ->
            }
                    canvas.drawText(chararcAngles[Pair(char, current, x, y + textPaint.textState)]?.let { (startAngle, sweepAngle) ->
                val counterSize / 3, textPaint)
                }
            }
        }
    }

    private fun drawSecondaryView(canvasKey = "${currentState}_$i"
                val paint = Paint(paintR: Canvas) {
        val rect = RectF(
            centerX - ringSize / 2, centering).apply {
                    style = Paint.Style.FILL
                    color = getHighlightColor(secondaryCountersY - ringSize / 2,
            centerX + ringSize / 2, center[counterKey] ?: 0)
                }
                
                // Draw filleY + ringSize / 2
        )
        
        val letters = when (currentStated arc
                canvas.drawArc(rect, startAngle, sweepAngle,) {
            "RIGHT" -> RIGHT
            "TOP" -> TOP
            "LEFT false, paint)
                
                // Draw border
                canvas.drawArc(rect, startAngle, sweepAngle, false, paintBorder)
                
                // Draw character
                characterPositions[Pair(char," -> LEFT
            "BOTTOM" -> BOTTOM
            else -> emptyList()
        }
        
        letters.forEachIndexed { i, char ->
            characterAngles[Pair(char, currentState)]?.let { (startAngle, currentState)]?.let { (x, y) ->
                    canvas.drawText(char, x, y + paintText.textSize / 3, paintText)
                 endAngle) ->
                val sweepAngle = endAngle - startAngle
                
                val}
            }
        }
    }

    private fun drawNumView(canvas: Canvas) {
        val rect = RectF counterKey = "${currentState}_$i"
                (
            centerX - outerRadius,val paint = Paint(paintRing).apply {
                    color = getHighlightColor(secon centerY - outerRadius,
            centerX + outerRadius, centerY + outerRadius
        )
        
        NUMBERS.forEach { num ->
            daryCounters[counterKey] ?: 0)
                }
                
                // Draw filled arc
                canvas.drawArcarcAngles[Pair(num, "NUM(rect, startAngle, sweepAn")]?.let { (startAngle, sweepAngle) ->
                val counterKeygle, true, paint)
                // Draw border
                canvas.drawArc(rect, startAngle, sweepAngle, true, paintBorder)
                
                // Draw character = "NUM_$num"
                val paint = Paint(paintRing
                characterPositions[Pair(char,).apply {
                    style = Paint.Style.FILL
                    color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
                 currentState)]?.let { (x, y}
                
                // Draw filled arc
                canvas.drawArc(rect, start) ->
                    canvas.drawText(char, x, y + paintText.textSize / 3, paintText)
                }Angle, sweepAngle, false, paint)
                
                // Draw border
            }
        }
    }

    private fun drawNumView(canvas: Canvas
                canvas.drawArc(rect, startAngle, sweepAngle, false,) {
        val rect = RectF(
            centerX - ringSize /  paintBorder)
                
                // Draw2, centerY - ringSize / 2,
            centerX + ringSize /  number
                characterPositions[Pair(num2, centerY + ringSize / 2
        )
        
        NUMBERS.forEach { num ->
            characterAngles[Pair(num, ", "NUM")]?.let { (x, y) ->
                    canvas.drawTextNUM")]?.let { (startAngle, endAngle) ->
                val sweep(num, x, y + paintAngle = endAngle - startAngle
                
                val counterKey = "Text.textSize / 3, paintText)
                }
            }
        }
    }

    private fun drawCornerNUM_$num"
                val paint = Paint(paintRing).apply {
                Buttons(canvas: Canvas) {
        val    color = getHighlightColor(secondaryCounters[counterKey] ?: 0)
                }
                
                // buttonSize = outerRadius * 0.25f
        val margin = outerRadius * 0.125f
        
         Draw filled arc
                canvas.drawArc// Calculate button positions relative to canvas size
        val buttons = listOf(
            Triple("NUM", margin(rect, startAngle, sweepAngle, true, paint)
                // Draw + buttonSize/2, margin + button border
                canvas.drawArc(rect, startAngle, sweepAngle,Size/2),
            Triple("⟲", width - margin - buttonSize/2, margin + buttonSize/2), true, paintBorder)
                
                // Draw number
                characterPositions
            Triple("X", margin + buttonSize/2, height - margin - buttonSize[Pair(num, "NUM")]?./2),
            Triple("✔", width - margin - buttonSize/2,let { (x, y) ->
                    canvas.drawText(num, height - margin - buttonSize/2)
        )
        
        buttons.forEach { (text, x, y) ->
             x, y + paintText.textSize / 3, paintText)
                }
            }
        }
    }

    val buttonKey = when (text) {private fun drawCornerButtons(canvas: Canvas) {
        val buttonSize = ringSize * 0.2f  
                "NUM" -> "NUM"
                "⟲" -> "// Scale with display
        val margin = ringSize * 0.1f
        
        // Button positions - matching Python layout exactly
        val buttonsRETURN"
                "X" -> "DELETE"
                "✔" -> " = listOf(
            Triple("NUM",CONFIRM"
                else -> ""
            }
             centerX - ringSize/2 
            val paint = Paint(paintR+ margin + buttonSize/2,ing).apply {
                style = Paint.Style.FILL
                color = getHigh centerY - ringSize/2 + marginlightColor(counters[buttonKey] ?: 0)
            }
             + buttonSize/2),
            Triple("⟲", centerX + ringSize/2 
            // Draw button backgroun- margin - buttonSize/2, centerY - ringSize/2 + margin + buttonSize/2),
            Triple("X", centerX - ringSize/2 + margin + buttonSize/2, centerYd
            canvas.drawRect(
                x - buttonSize/2, y - buttonSize/2,
                x + buttonSize/2, y + buttonSize/2 + ringSize/2 - margin - buttonSize/2),
            Triple("✔,
                paint
            )
            
            // Draw button border
            canvas.drawRect(
                x - buttonSize/2", centerX + ringSize/2 - margin - buttonSize/2, centerY +, y - buttonSize/2,
                 ringSize/2 - margin - buttonSize/2)
        )
        
        x + buttonSize/2, y + buttonSize/2,
                paintbuttons.forEach { (text, x, y) ->Border
            )
            
            // Draw text with appropriate color
            val textColor = when (text) {
            val buttonKey = when (text) {
                "✔" -> colorConfirm
                "X" -> colorCancel
                else -> colorText
            }
            
                "NUM" -> "NUM"
                "⟲" -> "RETURN"
                "X" -> "DELETE
            val textPaint = Paint(paintText).apply { color = textColor }"
                "✔" -> "CONFIRM"
                else -> ""
            }
            
            canvas.drawText(text, x, y + paintText.textSize / 3, textPaint)
        }
    
            val paint = Paint(paintRing).apply {
                color = getHighlightColor(counters[buttonKey] ?: 0)
            }
            }

    private fun drawCenterCircle(canvas: Canvas) {
        //
            // Draw button background
            canvas.draw Draw center circle background
        val centerPRect(
                x - buttonSize/2, y -aint = Paint(paintRing).apply {
            style = Paint.Style.FILL
            color = getHighlightColor(counters["CENTER"] ?: 0)
        }
        canvas.drawCircle( buttonSize/2,
                x + buttonSize/2, y + buttonSize/2,
                paint
            )
            
            // Draw button border
            canvas.drawcenterX, centerY, innerRadius, centerPaint)
        
        // Draw center circle borderRect(
                x - buttonSize/2, y - buttonSize/2,
                  
        canvas.drawCircle(centerXx + buttonSize/2, y + buttonSize/2,
                paintBorder
            ), centerY, innerRadius, paintBorder)
        
        // Draw text
        val displayText = getCenterCirc
            
            // Draw button text
            val textColor = when (text) {
                "leText()
        canvas.drawText(displayText, centerX, centerY + paintText✔" -> colorConfirm
                "X" -> colorCancel
                else -> colorText
            }
            
            val textPaint = Paint.textSize / 3, paintText)
    }

    private fun getHighlightColor(counter: Int): Int(paintText).apply { 
                color = textColor 
                textSize = {
        return when {
            counter == 0 -> colorRing
            counter >= paintText.textSize * 0.8f
            }
            canvas.drawText(text, x, y + textPaint.textSize / 3, textPaint) SELECTION_THRESHOLD -> colorBorder
            else -> {
                val alpha
        }
    }

    private fun draw = (counter.toFloat() / SELECTION_THRESHOLD * 255).toIntCenterCircle(canvas: Canvas) {
        // Draw center circle - EXACTLY like Python
        val centerP()
                Color.argb(alpha, 51, 136, 255)aint = Paint(paintRing).apply {
            color = getHighlightColor( // #3388ff with variable alpha
            }counters["CENTER"] ?: 0)
        }
        
        canvas
        }
    }

    private fun getCenterCircleText(): String {
        return.drawCircle(centerX, centerY if (currentState == "NUM") {
            ", innerRadius, centerPaint)
        canvas.drawCircle(centerX, centerY, innerRadius, paintBorder)
        
        // Draw center text
        val display." // Decimal point in NUM mode
        } else {Text = getCenterCircleText()
        
            if (currentText.length <= MAX_DISPLAY_CHARS) {
                canvas.drawText(displayText, centerX, centerY + paintText.textSize / 3, paintText)
    }currentText
            } else {
                currentText.takeLast(MAX_DISPLAY_CHARS)
            }
        }
    }

    private fun getHighlightColor(counter: Int): Int {
        return when {

    private fun processCommand(command: String) {
        try {
            val commandNum = command.to
            counter == 0 -> colorRing
            counter >= SELECTION_THRESHOLD -> colorBorder
            IntOrNull() ?: return
            
            when (commandNum) {
                in 1..20 -> processSectorInput(commandNum)else -> {
                val alpha = (counter.toFloat() /
                in 21..25 -> processButtonInput(commandNum)
            }
            
            invalidate() SELECTION_THRESHOLD * 255).toInt // Trigger redraw
        } catch()
                Color.argb(alpha, 51, 136, 255) (e: Exception) {
            e // #3388ff with variable.printStackTrace()
        }
    }

    private fun processSectorInput(sector alpha
            }
        }
    }: Int) {
        when (currentState) {
            "

    private fun getCenterCircleText(): String {
        return if (currentState == "NUM") {
            "."
        } else {MAIN" -> {
                sectorMappings["MAIN"]?.forEach { (section, sectors) ->
                    
            if (currentText.length <= MAX_DISPLAY_if (sector in sectors) {
                        counters[section] = (CHARS) {
                currentText
            } else {
                currentText.takeLast(MAX_DISPLAY_CHARS)
            }
        }
    }counters[section] ?: 0)

    private fun processCommand(command: String + 1
                        if ((counters[section] ?: 0) >= SELECTION_THRESHOLD) {
                ) {
        try {
            val commandNum = command.toIntOrNull() ?: return
            
            when (commandNum) {            resetAllCounters()
                            currentState = section
                        }
                        return
                    }
                }
            }
            "NUM" -> {
                
                in 1..20 -> processSectorInput(commandNum)
                in 21..25 -> processButtonInput(commandNum)sectorMappings["NUM"]?.forEach { (number, sectors) ->
                    if (sector
            }
            
            invalidate() // Trigger redraw
        } catch in sectors) {
                        val (e: Exception) {
            e counterKey = "NUM_$number"
                        secondaryCounters[counterKey] = (secondaryCounters[counter.printStackTrace()
        }
    }

    private fun processSectorInput(sectorKey] ?: 0) + 1
                        if ((secondaryCounters[counterKey] ?: 0) >= SELECTION_THRESHOLD) {
                            ad: Int) {
        when (currentdNumber(number)
                        }
                        return
                    }
                }
            State) {
            "MAIN" -> {
                sectorMappings["MAIN"]?.forEach { (section, sectors) ->
                    }
            in listOf("RIGHT", "TOP", "LEFTif (sector in sectors) {
                        counters[section] = (counters[section] ?: 0) + 1
                ", "BOTTOM") -> {
                val letters = when (currentState) {
                    "RIGHT" -> RIGHT
                    "TOP" -> TOP
                    "LEFT" -> LEFT
                    "BOTTOM" -> BOTTOM
                    else -> emptyList()
                }
                
                // Check character-specific mappings
                letters.forEachIndex        if ((counters[section] ?: 0) >= SELECTION_THRESHOLD) {
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
                ed { i, char ->
                    sectorMappings[char]?.get("0")?.let { sectors ->
                        if (sector in sectors) {
                            val        secondaryCounters[counterKey] = (secondaryCounters[counterKey] ?: 0) + 1
                        if ((secondaryCounters[counterKey] ?: counterKey = "${currentState}_$i"
                            secondaryCounters[counterKey] = (secon 0) >= SELECTION_THRESHOLD)daryCounters[counterKey] ?:  {
                            addNumber(number)
                        }
                        return
                    }0) + 1
                            if ((
                }
            }
            insecondaryCounters[counterKey] ?: 0) >= SELECTION_THRESHOLD) {
                                addCharacter(char)
                            }
                            return
                        }
                    }
                }
            } listOf("RIGHT", "TOP", "LEFT
        }
    }

    private fun processButtonInput(buttonCode: Int) {
        when (buttonCode) {
            21", "BOTTOM") -> {
                // Implement proper sector mapping for secondary -> { // NUM
                counters["NUM"] = panels
                val letters = when (current (counters["NUM"] ?: 0) + 1
                if ((countersState) {
                    "RIGHT" -> RIGHT
                    "TOP" -> TOP
                    "LEFT" -> LEFT
                    ["NUM"] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                    currentState = "NUM"
                }
            }
            22"BOTTOM" -> BOTTOM
                    else -> emptyList()
                }
                
                // For now, simplifie -> { // RETURN
                cound mapping - TODO: implement full sector mapping
                ifters["RETURN"] = (counters[" (sector <= letters.size) {
                    val charRETURN"] ?: 0) + 1
                if ((counters["RETURN = letters[sector - 1]
                "] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                    currentState = "    addCharacter(char)
                }
            }
        }
    }

    private fun processButtonInput(buttonCode: Int) {
        when (buttonCode) {
            21MAIN"
                }
            }
            23 -> { // DELETE
                if (currentState !in listOf("TOP -> { // NUM
                counters["NUM"] = (counters["NUM", "RIGHT", "BOTTOM","] ?: 0) + 1
                if ((counters["NUM"] ?: "LEFT")) {
                    counters[" 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()DELETE"] = (counters["DELETE"] ?: 0) + 1
                    
                    currentState = "NUM"
                }
            }
            22 -> {if ((counters["DELETE"] ?: 0) >= SELECTION_THRESHOLD) {
                        resetAllCounters()
                 // RETURN
                counters["RETURN"]        if (currentText.isNotEmpty()) {
                            currentText = currentText.drop = (counters["RETURN"] ?: 0) + 1
                if ((Last(1)
                        }counters["RETURN"] ?: 0) >= SELECTION_THRESHOLD) {
                    resetAllCounters()
                     else {
                            speakText("No")
                        }
                    }
                }
            }
            24 -> {currentState = "MAIN"
                } // CONFIRM
                if (currentState !
            }
            23 -> { // DELETE
                if (currentState !in listOf("TOPin listOf("TOP", "RIGHT", "BOTTOM", "LEFT")) {
                    counters["CONFIRM"] = (counters["CONFIRM"] ?: 0) +", "RIGHT", "BOTTOM", "LEFT")) 1
                    if ((counters["CONFIRM"] ?: 0) >= SELECTION_THRESHOLD) {
                        reset {
                    counters["DELETE"] = (counAllCounters()
                        ifters["DELETE"] ?: 0) + 1
                    if ((counters["DELETE"] ?: 0) >= SELECTION_THRESHOLD) {
                        resetAllCounters()
                        if (currentText.isNotEmpty()) (currentText.isNotEmpty()) {
                            confirmText()
                        } else {
                            speakText("Yes {
                            currentText = currentText.dropLast(1)
                        } else {
                            speakText("No")
                        }")
                        }
                    }
                }
            }
            25 ->
                    }
                }
            } { // CENTER
                coun
            24 -> { // CONFIRM
                if (currentState !in listOf("TOPters["CENTER"] = (counters["CENTER", "RIGHT", "BOTTOM", "LEFT")) {
                    counters["CONFIRM"] ?: 0) + 1
                if ((counters["CENTER"] ?: 0) >= SELECTION_THRESHOLD)"] = (counters["CONFIRM"] ?: 0) + 1
                    if ((counters["CONFIRM"] ?: 0) >= SELECTION_THRESHOLD) {
                        resetAllCounters() {
                    resetAllCounters()
                    if (currentState == "NUM") {
                        addDecimalPoint()
                    }
                        if (currentText.isNotEmpty()) {
                            confirmText()
                        } else {
                        addSpace()
                    }
                }
            }
        } else {
                            speakText("Yes")
                        }
                    }
    }

    private fun addCharacter(char: String) {
        currentText += char
        resetAllCounters()
        current
                }
            }
            25 ->State = "MAIN"
    }

    private fun addNumber(num: String) {
        currentText += num
        resetAllCounters()
        // { // CENTER
                counters["CENTER"] = Stay in NUM state
    }

    private fun addSpace() {
        currentText += " " (counters["CENTER"] ?: 0) + 1
                if ((counters
        resetAllCounters()
    }

    private fun addDecimalPoint() {
        currentText["CENTER"] ?: 0) >= SELECTION_THRESHOLD) {
                    reset += "."
        resetAllCounters()
    }

    private fun confirmText() {
        AllCounters()
                    if (currentState == "NUM") {if (currentText.isNotEmpty()) {
                        addDecimalPoint()
                    } else {
                        addSpace()
                    }
            speakText(currentText)
            
                }
            }
        }
    }

    private fun addCharacter(char: String) {
        currentText += char
        resetAllCounters()
        currentState = "MAIN"
    }

    private fun addNumber(numcurrentText = ""
            resetAllCounters()
            currentState = "MAIN"
        }
    }

    private fun speakText(text: String) {
        tts?.speak(text, TextToSpeech.QUEUE: String) {
        currentText += num
        resetAllCounters()
        //_FLUSH, null, null)
    } Stay in NUM state
    }

    private

    private fun resetAllCounters() {
        counters.keys.forEach { counters[it] = 0 }
        secondaryCounters.keys.forEach { secondaryCounters[it] = 0 fun addSpace() {
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
             }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        tts?.shutdownresetAllCounters()
            currentState = "MAIN"
        }
    }

    ()
        regionReceiver?.stop()
    }
}

// Regionprivate fun speakText(text: Receiver for socket communication (unchanged)
class RegionReceiver(private val callback: (String) -> String) {
        tts?.speak(text, TextToSpeech.QUEUE Unit) {
    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    _FLUSH, null, null)
    }

    private fun resetAllCounters() {
        counters.keys.forEach { counters[it] = 0 }private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun start()
        secondaryCounters.keys.forEach { secondaryCounters[it] = 0 {
        if (isRunning) return
        
        isRunning = true
        scope.launch {
            try {
                serverSocket = ServerSocket(5 }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        tts?.shutdown()
        region051)
                println("Listening on port 5051")
                
                while (isRunReceiver?.stop()
    }ning) {
                    try {
                        val clientSocket = serverSocket?.accept()
                        clientSocket?.let { socket ->
                            launch
}

// Region Receiver for socket communication - unchanged
class RegionReceiver(private val callback: (String) -> { handleClient(socket) }
                        }
                    } catch (e: Exception) {
                        if (isRunning) {
                            println Unit) {
    private var serverSocket: ServerSocket? = null
    private("Error accepting connection: ${e.message}")
                        }
                    } var isRunning = false
    private val scope = CoroutineScope(Dispatchers
                }
            } catch (e: Exception) {
                println("Error starting server:.IO + SupervisorJob()) ${e.message}")
            }
        }
    }

    private suspen

    fun start() {
        if (isRunning) return
        
        isRunning = true
        scope.d fun handleClient(socket: Socket) {
        withContext(Dispatcherslaunch {
            try {
                serverSocket = ServerSocket(5051)
                println(".IO) {
            try {
                val reader = BufferedReader(InputStreamReader(socketListening on port 5051")
                
                while (isRunning) {
                .getInputStream()))
                var line: String?    try {
                        val clientSocket = serverSocket?.accept()
                        
                
                while (reader.readLine().alsoclientSocket?.let { socket ->
                            launch { line = it } != null && isRunning) {
                    line?. { handleClient(socket) }
                        }
                    } catch (e: Exception) {
                        if (isRunning) {
                            printlntrim()?.let { command ->
                        if (command.isNotEmpty()) {
                            println("Received comman("Error accepting connection: ${e.message}")
                        }
                    }
                d: $command")
                            callback(command)
                        }
                    }
                }
            } catch (e: Exception}
            } catch (e: Exception) {
                println("Error starting) {
                println("Error handling client: ${e.message}")
            } server: ${e.message}")
            }
        }
    }

    private suspen finally {
                try {
                    socketd fun handleClient(socket: Socket) {
        withContext(Dispatchers.IO.close()
                } catch (e:) {
            try {
                val reader = BufferedReader(InputStreamReader(socket Exception) {
                    println("Error closing.getInputStream()))
                var line: String?
                
                while ( socket: ${e.message}")
                }
            }
        }
    }

    fun stop() {
        isRunningreader.readLine().also { line = it } = false
        scope.cancel()
         != null && isRunning) {try {
            serverSocket?.close()
        
                    line?.trim()?.let { command ->
                        if (command.isNotEmpty()) {
                            println("Received comman} catch (e: Exception) {
            d: $command")
                            callback(command)
                        }
                    }println("Error closing server socket: ${e.message}")
        }
    }
}
                }
            } catch (e: Exception) {
                println("Error handling client: ${e.message}")
            }
