package com.example.glassgaze

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    
    private lateinit var aacKeyboardView: AACKeyboardView
    
    companion object {
        private const val PERMISSION_REQUEST_CODE = 100
        private val REQUIRED_PERMISSIONS = arrayOf(
            Manifest.permission.INTERNET,
            Manifest.permission.RECORD_AUDIO
        )
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Check permissions
        if (checkPermissions()) {
            initializeView()
        } else {
            requestPermissions()
        }
    }
    
    private fun checkPermissions(): Boolean {
        return REQUIRED_PERMISSIONS.all { permission ->
            ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED
        }
    }
    
    private fun requestPermissions() {
        ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, PERMISSION_REQUEST_CODE)
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                initializeView()
            } else {
                Toast.makeText(this, "Permissions required for AAC functionality", Toast.LENGTH_LONG).show()
                finish()
            }
        }
    }
    
    private fun initializeView() {
        aacKeyboardView = AACKeyboardView(this)
        setContentView(aacKeyboardView)
        
        // Make full screen for better experience on Glass
        supportActionBar?.hide()
    }
    
    override fun onDestroy() {
        super.onDestroy()
    }
}
