package com.example.demo

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class AppConfig {

    @Bean("eagerAuthService")
    fun authService(): AuthService = AuthService

    @Bean("lazyAuthService")
    fun lazyAuthService(): LazyAuthService = LazyAuthService.instance
}
