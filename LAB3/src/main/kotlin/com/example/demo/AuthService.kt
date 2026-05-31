package com.example.demo

object AuthService {

    fun authenticate(username: String, password: String): Boolean {
        return username.isNotBlank() && password.isNotBlank()
    }
}
