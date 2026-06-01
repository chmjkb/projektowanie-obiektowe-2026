import Fluent

struct AddCategoryToProduct: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema("products")
            .field("category_id", .uuid, .references("categories", "id", onDelete: .setNull))
            .update()
    }

    func revert(on database: Database) async throws {
        try await database.schema("products")
            .deleteField("category_id")
            .update()
    }
}
