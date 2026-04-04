package com.example.demo

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class User(val id: Int, val username: String, val email: String)

@RestController
@RequestMapping("/users")
class UserController {

    private val users = listOf(
        User(1, "alice", "alice@example.com"),
        User(2, "bob", "bob@example.com"),
        User(3, "charlie", "charlie@example.com")
    )

    @GetMapping
    fun getUsers(): List<User> = users
}
