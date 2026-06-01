import Vapor

func routes(_ app: Application) throws {
    app.get { _ in
        "LAB7 — Vapor + Fluent. Endpoints: /products"
    }

    try app.register(collection: ProductController())
}
