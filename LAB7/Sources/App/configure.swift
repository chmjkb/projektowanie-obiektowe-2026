import Fluent
import FluentSQLiteDriver
import Leaf
import Redis
import Vapor

public func configure(_ app: Application) async throws {
    app.databases.use(.sqlite(.file("db.sqlite")), as: .sqlite)

    app.migrations.add(CreateProduct())
    app.migrations.add(CreateCategory())
    app.migrations.add(AddCategoryToProduct())
    try await app.autoMigrate()

    app.views.use(.leaf)

    let redisURL = Environment.get("REDIS_URL") ?? "redis://localhost:6379"
    app.redis.configuration = try RedisConfiguration(url: redisURL)
    app.caches.use(.redis)

    try routes(app)
}
