package com.example.demo

class AuthService private constructor() {

    fun authenticate(username: String, password: String): Boolean {
        // Mock: always returns true for non-blank credentials
        return username.isNotBlank() && password.isNotBlank()
    }

    companion object {
        val instance: AuthService = AuthService()
    }
}
