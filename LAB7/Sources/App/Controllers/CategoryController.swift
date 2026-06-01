import Fluent
import Vapor

struct CategoryController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        let categories = routes.grouped("categories")
        categories.get(use: index)
        categories.get("new", use: newForm)
        categories.post(use: create)
        categories.group(":categoryID") { category in
            category.get(use: show)
            category.get("edit", use: editForm)
            category.post(use: update)
            category.post("delete", use: delete)
        }
    }

    struct IndexContext: Content {
        let categories: [Category]
    }

    struct ShowContext: Content {
        let category: Category
        let products: [Product]
    }

    struct FormContext: Content {
        let category: Category?
        let action: String
        let title: String
    }

    func index(req: Request) async throws -> View {
        let categories = try await Category.query(on: req.db).all()
        return try await req.view.render("categories/index", IndexContext(categories: categories))
    }

    func newForm(req: Request) async throws -> View {
        let ctx = FormContext(category: nil, action: "/categories", title: "Nowa kategoria")
        return try await req.view.render("categories/form", ctx)
    }

    func show(req: Request) async throws -> View {
        guard let category = try await Category.query(on: req.db)
            .filter(\.$id == req.parameters.get("categoryID")!)
            .with(\.$products)
            .first()
        else {
            throw Abort(.notFound)
        }
        return try await req.view.render(
            "categories/show",
            ShowContext(category: category, products: category.products)
        )
    }

    func editForm(req: Request) async throws -> View {
        guard let category = try await Category.find(req.parameters.get("categoryID"), on: req.db) else {
            throw Abort(.notFound)
        }
        let ctx = FormContext(
            category: category,
            action: "/categories/\(category.id!)",
            title: "Edycja kategorii"
        )
        return try await req.view.render("categories/form", ctx)
    }

    func create(req: Request) async throws -> Response {
        let dto = try req.content.decode(CategoryDTO.self)
        let category = dto.toModel()
        try await category.save(on: req.db)
        return req.redirect(to: "/categories")
    }

    func update(req: Request) async throws -> Response {
        guard let category = try await Category.find(req.parameters.get("categoryID"), on: req.db) else {
            throw Abort(.notFound)
        }
        let dto = try req.content.decode(CategoryDTO.self)
        category.name = dto.name
        try await category.save(on: req.db)
        return req.redirect(to: "/categories/\(category.id!)")
    }

    func delete(req: Request) async throws -> Response {
        guard let category = try await Category.find(req.parameters.get("categoryID"), on: req.db) else {
            throw Abort(.notFound)
        }
        try await category.delete(on: req.db)
        return req.redirect(to: "/categories")
    }
}
