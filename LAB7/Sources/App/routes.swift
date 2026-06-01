import Vapor

func routes(_ app: Application) throws {
    app.get { _ in
        "LAB7 — Vapor + Fluent + Leaf. Endpoints: /products, /categories"
    }

    try app.register(collection: ProductController())
    try app.register(collection: CategoryController())
}
