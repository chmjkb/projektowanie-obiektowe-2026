import Fluent
import Vapor

struct ProductController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        let products = routes.grouped("products")
        products.get(use: index)
        products.get("new", use: newForm)
        products.post(use: create)
        products.group(":productID") { product in
            product.get(use: show)
            product.get("edit", use: editForm)
            product.post(use: update)
            product.post("delete", use: delete)
        }
    }

    struct IndexContext: Content {
        let products: [Product]
    }

    struct ShowContext: Content {
        let product: Product
    }

    struct FormContext: Content {
        let product: Product?
        let action: String
        let title: String
    }

    func index(req: Request) async throws -> View {
        let products = try await Product.query(on: req.db).all()
        return try await req.view.render("products/index", IndexContext(products: products))
    }

    func newForm(req: Request) async throws -> View {
        let ctx = FormContext(product: nil, action: "/products", title: "Nowy produkt")
        return try await req.view.render("products/form", ctx)
    }

    func show(req: Request) async throws -> View {
        guard let product = try await Product.find(req.parameters.get("productID"), on: req.db) else {
            throw Abort(.notFound)
        }
        return try await req.view.render("products/show", ShowContext(product: product))
    }

    func editForm(req: Request) async throws -> View {
        guard let product = try await Product.find(req.parameters.get("productID"), on: req.db) else {
            throw Abort(.notFound)
        }
        let ctx = FormContext(product: product, action: "/products/\(product.id!)", title: "Edycja produktu")
        return try await req.view.render("products/form", ctx)
    }

    func create(req: Request) async throws -> Response {
        let dto = try req.content.decode(ProductDTO.self)
        let product = dto.toModel()
        try await product.save(on: req.db)
        return req.redirect(to: "/products")
    }

    func update(req: Request) async throws -> Response {
        guard let product = try await Product.find(req.parameters.get("productID"), on: req.db) else {
            throw Abort(.notFound)
        }
        let dto = try req.content.decode(ProductDTO.self)
        product.name = dto.name
        product.price = dto.price
        product.description = dto.description
        try await product.save(on: req.db)
        return req.redirect(to: "/products/\(product.id!)")
    }

    func delete(req: Request) async throws -> Response {
        guard let product = try await Product.find(req.parameters.get("productID"), on: req.db) else {
            throw Abort(.notFound)
        }
        try await product.delete(on: req.db)
        return req.redirect(to: "/products")
    }
}
