describe("userServersion", () => {
	let service;

	beforeEach(() => {
		jest.resetModules();
		service = require("../userService");
	});

	describe("addUser", () => {
		it("adds a new user and returns it", () => {
			const user = service.addUser({ name: "Alice", email: "alice@example.com" });
			expect(user).toMatchObject({ name: "Alice", email: "alice@example.com" });
			expect(user.id).toBeDefined();
			expect(user.createdAt).toBeDefined();
		});

		it("trims whitespace from name", () => {
			const user = service.addUser({ name: "  Bob  ", email: "bob@example.com" });
			expect(user.name).toBe("Bob");
		});

		it("throws when name is missing", () => {
			expect(() => service.addUser({ email: "a@b.com" })).toThrow("Name is required.");
		});

		it("throws when name is blank", () => {
			expect(() => service.addUser({ name: "   ", email: "a@b.com" })).toThrow("Name is required.");
		});

		it("throws when email is invalid", () => {
			expect(() => service.addUser({ name: "Alice", email: "not-an-email" })).toThrow("Email is invalid.");
		});

		it("throws when email is duplicated", () => {
			service.addUser({ name: "Alice", email: "alice@example.com" });
			expect(() => service.addUser({ name: "Alice2", email: "alice@example.com" })).toThrow("Email already exists.");
		});

		it("is case-insensitive for duplicate email check", () => {
			service.addUser({ name: "Alice", email: "alice@example.com" });
			expect(() =>
				service.addUser({ name: "Alice2", email: "ALICE@EXAMPLE.COM" })
			).toThrow("Email already exists.");
		});
	});

	describe("getUsers", () => {
		it("returns an empty array when no users exist", () => {
			expect(service.getUsers()).toEqual([]);
		});

		it("returns all added users", () => {
			service.addUser({ name: "Alice", email: "alice@example.com" });
			service.addUser({ name: "Bob", email: "bob@example.com" });
			expect(service.getUsers()).toHaveLength(2);
		});

		it("returns a copy so mutations do not affect the store", () => {
			service.addUser({ name: "Alice", email: "alice@example.com" });
			const users = service.getUsers();
			users.pop();
			expect(service.getUsers()).toHaveLength(1);
		});
	});

	describe("getUserById", () => {
		it("returns the user with the matching id", () => {
			const added = service.addUser({ name: "Alice", email: "alice@example.com" });
			expect(service.getUserById(added.id)).toMatchObject({ name: "Alice" });
		});

		it("returns null when no user matches", () => {
			expect(service.getUserById(9999)).toBeNull();
		});
	});

	describe("updateUser", () => {
		it("updates name and sets updatedAt", () => {
			const user = service.addUser({ name: "Alice", email: "alice@example.com" });
			const updated = service.updateUser(user.id, { name: "Alicia" });
			expect(updated.name).toBe("Alicia");
			expect(updated.updatedAt).toBeDefined();
		});

		it("updates email", () => {
			const user = service.addUser({ name: "Alice", email: "alice@example.com" });
			const updated = service.updateUser(user.id, { email: "newalice@example.com" });
			expect(updated.email).toBe("newalice@example.com");
		});

		it("throws when user not found", () => {
			expect(() => service.updateUser(9999, { name: "Ghost" })).toThrow("User not found.");
		});

		it("throws when new email conflicts with another user", () => {
			const u1 = service.addUser({ name: "Alice", email: "alice@example.com" });
			service.addUser({ name: "Bob", email: "bob@example.com" });
			expect(() =>
				service.updateUser(u1.id, { email: "bob@example.com" })
			).toThrow("Email already exists.");
		});

		it("allows updating email to the same value", () => {
			const user = service.addUser({ name: "Alice", email: "alice@example.com" });
			const updated = service.updateUser(user.id, { email: "alice@example.com" });
			expect(updated.email).toBe("alice@example.com");
		});
	});

	describe("deleteUser", () => {
		it("removes the user and returns it", () => {
			const user = service.addUser({ name: "Alice", email: "alice@example.com" });
			const deleted = service.deleteUser(user.id);
			expect(deleted.id).toBe(user.id);
			expect(service.getUsers()).toHaveLength(0);
		});

		it("throws when user not found", () => {
			expect(() => service.deleteUser(9999)).toThrow("User not found.");
		});
	});
});
