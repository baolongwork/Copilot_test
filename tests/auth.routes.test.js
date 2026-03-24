const request = require("supertest");
const app = require("../server");

describe("Auth routes", () => {
	describe("GET /login", () => {
		it("returns 200 and serves the login page", async () => {
			const res = await request(app).get("/login");
			expect(res.statusCode).toBe(200);
		});
	});

	describe("GET /register", () => {
		it("returns 200 and serves the register page", async () => {
			const res = await request(app).get("/register");
			expect(res.statusCode).toBe(200);
		});
	});

	describe("GET /dashboard (unauthenticated)", () => {
		it("redirects to /login when not logged in", async () => {
			const res = await request(app).get("/dashboard");
			expect(res.statusCode).toBe(302);
			expect(res.headers.location).toBe("/login");
		});
	});

	describe("POST /register", () => {
		it("returns 400 when fields are missing", async () => {
			const res = await request(app)
				.post("/register")
				.send({ name: "Alice" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(400);
			expect(res.body.error).toBeDefined();
		});

		it("returns 400 when email is invalid", async () => {
			const res = await request(app)
				.post("/register")
				.send({ name: "Alice", email: "not-an-email", password: "secret123" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(400);
			expect(res.body.error).toMatch(/email/i);
		});

		it("returns 400 when password is too short", async () => {
			const res = await request(app)
				.post("/register")
				.send({ name: "Alice", email: "alice@example.com", password: "abc" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(400);
			expect(res.body.error).toMatch(/password/i);
		});

		it("creates an account and returns 201", async () => {
			const res = await request(app)
				.post("/register")
				.send({ name: "Alice", email: "alice_route@example.com", password: "secret123" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(201);
			expect(res.body.redirect).toBe("/dashboard");
		});

		it("returns 409 when email is already registered", async () => {
			const payload = { name: "Alice", email: "dup_route@example.com", password: "secret123" };
			await request(app)
				.post("/register")
				.send(payload)
				.set("Content-Type", "application/json");

			const res = await request(app)
				.post("/register")
				.send(payload)
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(409);
		});
	});

	describe("POST /login", () => {
		it("returns 400 when fields are missing", async () => {
			const res = await request(app)
				.post("/login")
				.send({ email: "test@example.com" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(400);
		});

		it("returns 401 for unknown email", async () => {
			const res = await request(app)
				.post("/login")
				.send({ email: "nobody@example.com", password: "password" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(401);
		});

		it("returns 401 for wrong password", async () => {
			await request(app)
				.post("/register")
				.send({ name: "Bob", email: "bob_login@example.com", password: "correctpass" })
				.set("Content-Type", "application/json");

			const res = await request(app)
				.post("/login")
				.send({ email: "bob_login@example.com", password: "wrongpass" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(401);
		});

		it("logs in with correct credentials", async () => {
			await request(app)
				.post("/register")
				.send({ name: "Carol", email: "carol_login@example.com", password: "mypassword" })
				.set("Content-Type", "application/json");

			const res = await request(app)
				.post("/login")
				.send({ email: "carol_login@example.com", password: "mypassword" })
				.set("Content-Type", "application/json");
			expect(res.statusCode).toBe(200);
			expect(res.body.redirect).toBe("/dashboard");
		});
	});
});
