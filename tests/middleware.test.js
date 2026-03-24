const { requireAuth, requireGuest } = require("../middleware/auth");

function mockRes() {
	return {
		redirectTo: null,
		redirect(url) {
			this.redirectTo = url;
		},
	};
}

describe("middleware/auth", () => {
	describe("requireAuth", () => {
		it("calls next() when userId is in session", () => {
			const req = { session: { userId: 1 } };
			const res = mockRes();
			const next = jest.fn();

			requireAuth(req, res, next);

			expect(next).toHaveBeenCalledTimes(1);
			expect(res.redirectTo).toBeNull();
		});

		it("redirects to /login when userId is not in session", () => {
			const req = { session: {} };
			const res = mockRes();
			const next = jest.fn();

			requireAuth(req, res, next);

			expect(res.redirectTo).toBe("/login");
			expect(next).not.toHaveBeenCalled();
		});
	});

	describe("requireGuest", () => {
		it("calls next() when userId is not in session", () => {
			const req = { session: {} };
			const res = mockRes();
			const next = jest.fn();

			requireGuest(req, res, next);

			expect(next).toHaveBeenCalledTimes(1);
			expect(res.redirectTo).toBeNull();
		});

		it("redirects to /dashboard when userId is in session", () => {
			const req = { session: { userId: 1 } };
			const res = mockRes();
			const next = jest.fn();

			requireGuest(req, res, next);

			expect(res.redirectTo).toBe("/dashboard");
			expect(next).not.toHaveBeenCalled();
		});
	});
});
