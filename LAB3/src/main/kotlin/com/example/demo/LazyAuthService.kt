package com.example.demo

class LazyAuthService private constructor() {

    fun authenticate(username: String, password: String): Boolean {
        return username.isNotBlank() && password.isNotBlank()
    }

    companion object {
        val instance: LazyAuthService by lazy { LazyAuthService() }
    }
}
