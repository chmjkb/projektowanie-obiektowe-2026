package com.example.demo

import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class LoginRequest(val username: String, val password: String)
data class LoginResponse(val success: Boolean, val message: String)

@RestController
@RequestMapping("/auth")
class AuthController {

    @PostMapping("/login")
    fun login(@RequestBody request: LoginRequest): LoginResponse {
        val authenticated = AuthService.instance.authenticate(request.username, request.password)
        return if (authenticated) {
            LoginResponse(success = true, message = "Authentication successful")
        } else {
            LoginResponse(success = false, message = "Invalid credentials")
        }
    }
}
