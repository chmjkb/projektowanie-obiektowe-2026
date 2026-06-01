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

    struct ProductRow: Content {
        let id: UUID
        let name: String
        let price: Double
        let description: String
        let categoryID: UUID?
        let categoryName: String?
    }

    struct IndexContext: Content {
        let products: [ProductRow]
    }

    struct ShowContext: Content {
        let product: ProductRow
    }

    struct FormContext: Content {
        let product: ProductRow?
        let action: String
        let title: String
        let categories: [Category]
    }

    private func row(from product: Product) -> ProductRow {
        ProductRow(
            id: product.id!,
            name: product.name,
            price: product.price,
            description: product.description,
            categoryID: product.$category.id,
            categoryName: product.category?.name
        )
    }

    private static let listCacheKey = "products:list"
    private static let cacheTTL: CacheExpirationTime = .seconds(60)

    func index(req: Request) async throws -> View {
        if let cached = try? await req.cache.get(Self.listCacheKey, as: [ProductRow].self) {
            req.logger.debug("products:list served from Redis cache")
            return try await req.view.render("products/index", IndexContext(products: cached))
        }

        let products = try await Product.query(on: req.db)
            .with(\.$category)
            .all()
        let rows = products.map(row)
        try? await req.cache.set(Self.listCacheKey, to: rows, expiresIn: Self.cacheTTL)
        return try await req.view.render("products/index", IndexContext(products: rows))
    }

    private func invalidateListCache(req: Request) async {
        try? await req.cache.delete(Self.listCacheKey)
    }

    func newForm(req: Request) async throws -> View {
        let categories = try await Category.query(on: req.db).all()
        let ctx = FormContext(
            product: nil,
            action: "/products",
            title: "Nowy produkt",
            categories: categories
        )
        return try await req.view.render("products/form", ctx)
    }

    func show(req: Request) async throws -> View {
        guard let product = try await Product.query(on: req.db)
            .filter(\.$id == req.parameters.get("productID")!)
            .with(\.$category)
            .first()
        else {
            throw Abort(.notFound)
        }
        return try await req.view.render("products/show", ShowContext(product: row(from: product)))
    }

    func editForm(req: Request) async throws -> View {
        guard let product = try await Product.query(on: req.db)
            .filter(\.$id == req.parameters.get("productID")!)
            .with(\.$category)
            .first()
        else {
            throw Abort(.notFound)
        }
        let categories = try await Category.query(on: req.db).all()
        let ctx = FormContext(
            product: row(from: product),
            action: "/products/\(product.id!)",
            title: "Edycja produktu",
            categories: categories
        )
        return try await req.view.render("products/form", ctx)
    }

    func create(req: Request) async throws -> Response {
        let dto = try req.content.decode(ProductDTO.self)
        let product = dto.toModel()
        try await product.save(on: req.db)
        await invalidateListCache(req: req)
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
        product.$category.id = dto.categoryID
        try await product.save(on: req.db)
        await invalidateListCache(req: req)
        return req.redirect(to: "/products/\(product.id!)")
    }

    func delete(req: Request) async throws -> Response {
        guard let product = try await Product.find(req.parameters.get("productID"), on: req.db) else {
            throw Abort(.notFound)
        }
        try await product.delete(on: req.db)
        await invalidateListCache(req: req)
        return req.redirect(to: "/products")
    }
}
